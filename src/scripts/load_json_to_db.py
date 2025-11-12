
from __future__ import annotations
"""python -m src.scripts.load_json_to_db --generate sample.json --products 200 --receipts 20
python -m src.scripts.load_json_to_db sample.json
"""

"""
Script: load_json_to_db.py
Purpose:
  1) Load master data and receipts from a JSON file into the database
  2) (Optional) Generate a synthetic JSON dataset (e.g., 200 products, 20 receipts)

Example JSON structure (keys optional except where noted):
{
  "categories": [{"name": "Fruit"}],
  "measurement_units": [{"name": "Kilogram", "abbreviation": "kg"}],
  "product_list": [{
    "name": "Madeira Banana",
    "barcode": "5601234567890",
    "category": "Fruit",
    "measurement_unit": "kg"
  }],
  "merchants": [{"name": "SuperMart", "location": "Lisbon"}],
  "receipts": [{
    "merchant": "SuperMart",
    "purchase_date": "2025-11-10",   
    "barcode": null,
    "products": [{
      "product_list": "Madeira Banana",
      "price": "1.2500",
      "quantity": "0.5000",
      "description": "on sale"
    }]
  }]
}

CLI Usage:
  # Load existing JSON into DB
  python -m load_json_to_db /path/to/data.json

  # Generate synthetic dataset (200 products, 20 receipts) to a file
  python -m load_json_to_db --generate sample.json --products 200 --receipts 20

Notes:
- Script assumes SessionLocal is available from src.database.
- Adjust model import paths if needed.
- Receipt items reference ProductList by name or by "barcode_product_list".
- When generating, the script creates realistic-ish data with unique names & barcodes.
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Iterable, Optional
import random
import itertools

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# --- Adjust these imports to match your project layout ---
from src.database import SessionLocal
from src.models.category import Category
from src.models.measurement_unit import MeasurementUnit
from src.models.merchant import Merchant
from src.models.receipt_product import Product
from src.models.product import ProductList
from src.models.receipt import Receipt
# --------------------------------------------------------


# ----------------------- Helpers -----------------------
class LoaderError(RuntimeError):
    pass


def _as_decimal(value: Any, field: str) -> Decimal:
    try:
        if isinstance(value, Decimal):
            return value
        if isinstance(value, (int, float)):
            return Decimal(str(value))
        if isinstance(value, str):
            return Decimal(value)
    except (InvalidOperation, ValueError):
        pass
    raise LoaderError(f"Invalid decimal for {field}: {value!r}")


def _as_date(value: Any) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError as e:
            raise LoaderError(f"Invalid ISO date: {value!r}") from e
    raise LoaderError(f"Invalid date: {value!r}")


# Simple in-memory caches to minimize DB lookups
class Cache:
    def __init__(self) -> None:
        self.categories: Dict[str, Category] = {}
        self.units_by_abbrev: Dict[str, MeasurementUnit] = {}
        self.units_by_name: Dict[str, MeasurementUnit] = {}
        self.product_lists_by_name: Dict[str, ProductList] = {}
        self.product_lists_by_barcode: Dict[str, ProductList] = {}
        self.merchants_by_name: Dict[str, Merchant] = {}


# -------------------- Get or create --------------------

def get_or_create_category(db: Session, cache: Cache, name: str) -> Category:
    key = name.strip()
    if key in cache.categories:
        return cache.categories[key]
    obj = db.query(Category).filter_by(name=key).one_or_none()
    if obj is None:
        obj = Category(name=key)
        db.add(obj)
        db.flush()  # assign id
    cache.categories[key] = obj
    return obj


def get_or_create_unit(
    db: Session, cache: Cache, *, name: str, abbreviation: str
) -> MeasurementUnit:
    abbr = abbreviation.strip()
    if abbr in cache.units_by_abbrev:
        return cache.units_by_abbrev[abbr]
    obj = (
        db.query(MeasurementUnit)
        .filter((MeasurementUnit.abbreviation == abbr) | (MeasurementUnit.name == name))
        .one_or_none()
    )
    if obj is None:
        obj = MeasurementUnit(name=name.strip(), abbreviation=abbr)
        db.add(obj)
        db.flush()
    cache.units_by_abbrev[abbr] = obj
    cache.units_by_name[obj.name] = obj
    return obj


def get_or_create_product_list(
    db: Session,
    cache: Cache,
    *,
    name: str,
    category_name: Optional[str],
    unit_abbrev: Optional[str],
    barcode: Optional[str] = None,
) -> ProductList:
    key = name.strip()
    if key in cache.product_lists_by_name:
        return cache.product_lists_by_name[key]

    q = db.query(ProductList).filter(ProductList.name == key)
    obj = q.one_or_none()

    if obj is None:
        # To create, we need enough context
        if not category_name or not unit_abbrev:
            raise LoaderError(
                "Cannot create ProductList without category and measurement_unit: "
                f"name={name!r} category={category_name!r} unit={unit_abbrev!r}"
            )
        cat = get_or_create_category(db, cache, category_name)
        unit = cache.units_by_abbrev.get(unit_abbrev)
        if unit is None:
            unit = (
                db.query(MeasurementUnit)
                .filter(MeasurementUnit.abbreviation == unit_abbrev)
                .one_or_none()
            )
            if unit is None:
                raise LoaderError(
                    f"MeasurementUnit with abbreviation {unit_abbrev!r} does not exist. "
                    "Define it in 'measurement_units' first."
                )
        obj = ProductList(
            name=key, barcode=(barcode or None), category=cat, measurement_unit=unit
        )
        db.add(obj)
        db.flush()

    cache.product_lists_by_name[key] = obj
    if obj.barcode:
        cache.product_lists_by_barcode[obj.barcode] = obj
    return obj


def get_or_create_merchant(
    db: Session, cache: Cache, *, name: str, location: Optional[str] = None
) -> Merchant:
    key = name.strip()
    if key in cache.merchants_by_name:
        return cache.merchants_by_name[key]
    obj = db.query(Merchant).filter_by(name=key).one_or_none()
    if obj is None:
        obj = Merchant(name=key, location=location)
        db.add(obj)
        db.flush()
    cache.merchants_by_name[key] = obj
    return obj


# ------------------ Load sections ------------------

def load_categories(db: Session, cache: Cache, items: Iterable[Dict[str, Any]]) -> int:
    count = 0
    for rec in items or []:
        name = (rec or {}).get("name")
        if not name:
            raise LoaderError("Category requires a 'name'")
        get_or_create_category(db, cache, name)
        count += 1
    return count


def load_units(db: Session, cache: Cache, items: Iterable[Dict[str, Any]]) -> int:
    count = 0
    for rec in items or []:
        if not rec:
            continue
        name = rec.get("name")
        abbr = rec.get("abbreviation")
        if not name or not abbr:
            raise LoaderError("MeasurementUnit requires 'name' and 'abbreviation'")
        get_or_create_unit(db, cache, name=name, abbreviation=abbr)
        count += 1
    return count


def load_product_list(db: Session, cache: Cache, items: Iterable[Dict[str, Any]]) -> int:
    count = 0
    for rec in items or []:
        if not rec:
            continue
        name = rec.get("name")
        if not name:
            raise LoaderError("ProductList requires 'name'")
        barcode = rec.get("barcode")
        category = rec.get("category")
        unit_abbrev = rec.get("measurement_unit")
        get_or_create_product_list(
            db, cache, name=name, category_name=category, unit_abbrev=unit_abbrev, barcode=barcode
        )
        count += 1
    return count


def load_merchants(db: Session, cache: Cache, items: Iterable[Dict[str, Any]]) -> int:
    count = 0
    for rec in items or []:
        if not rec:
            continue
        name = rec.get("name")
        if not name:
            raise LoaderError("Merchant requires 'name'")
        get_or_create_merchant(db, cache, name=name, location=rec.get("location"))
        count += 1
    return count


def load_receipts(db: Session, cache: Cache, items: Iterable[Dict[str, Any]]) -> int:
    count = 0
    for rec in items or []:
        if not rec:
            continue
        merchant_name = rec.get("merchant")
        if not merchant_name:
            raise LoaderError("Receipt requires 'merchant'")
        # Accept either 'purchase_date' (preferred) or legacy 'date' key
        r_date = _as_date(rec.get("purchase_date") or rec.get("date"))
        barcode = rec.get("barcode")

        merchant = get_or_create_merchant(db, cache, name=merchant_name)
        receipt = Receipt(merchant=merchant, purchase_date=r_date, barcode=barcode)
        db.add(receipt)
        db.flush()

        products = rec.get("products") or []
        for p in products:
            # Resolve ProductList by name or barcode
            pl_name = p.get("product_list")
            pl_barcode = p.get("barcode_product_list")
            pl: Optional[ProductList] = None

            if pl_barcode:
                pl = cache.product_lists_by_barcode.get(pl_barcode)
                if pl is None:
                    pl = (
                        db.query(ProductList)
                        .filter(ProductList.barcode == pl_barcode)
                        .one_or_none()
                    )
                if pl is None:
                    raise LoaderError(
                        f"ProductList with barcode {pl_barcode!r} not found. "
                        "Define it in 'product_list' first."
                    )
            else:
                if not pl_name:
                    raise LoaderError("Each product requires 'product_list' (name) or 'barcode_product_list'")
                pl = get_or_create_product_list(
                    db,
                    cache,
                    name=pl_name,
                    category_name=p.get("category"),
                    unit_abbrev=p.get("measurement_unit"),
                )

            price = _as_decimal(p.get("price"), "price")
            quantity = _as_decimal(p.get("quantity"), "quantity")
            description = p.get("description")

            product = Product(
                price=price,
                quantity=quantity,
                description=description,
                receipt=receipt,
                product_list=pl,
            )
            db.add(product)

        count += 1
    return count


# ------------------ Synthetic data gen ------------------

_DEFAULT_CATEGORIES = [
    "Fruit", "Vegetable", "Dairy", "Bakery", "Meat", "Fish", "Beverages",
    "Pantry", "Snacks", "Frozen", "Household", "Personal Care"
]

_DEFAULT_UNITS = [
    {"name": "Kilogram", "abbreviation": "kg"},
    {"name": "Gram", "abbreviation": "g"},
    {"name": "Liter", "abbreviation": "L"},
    {"name": "Milliliter", "abbreviation": "mL"},
    {"name": "Unit", "abbreviation": "u"},
    {"name": "Pack", "abbreviation": "pk"}
]

_PRODUCT_BASES = [
    "Apple", "Banana", "Orange", "Tomato", "Cucumber", "Milk", "Yogurt",
    "Bread", "Baguette", "Chicken Breast", "Pork Loin", "Salmon Fillet",
    "Sparkling Water", "Olive Oil", "Rice", "Pasta", "Chips", "Chocolate",
    "Ice Cream", "Laundry Detergent", "Toothpaste", "Shampoo", "Coffee",
    "Tea", "Cheese", "Butter", "Eggs", "Flour", "Sugar", "Salt"
]

_ADJECTIVES = [
    "Organic", "Premium", "Local", "Imported", "Classic", "Fresh",
    "Family", "Extra", "Light", "Whole", "Gluten-Free", "Vegan"
]

_MERCHANTS = [
    {"name": "SuperMart", "location": "Lisbon"},
    {"name": "Mercado Azul", "location": "Porto"},
    {"name": "MiniPreço", "location": "Coimbra"},
    {"name": "HiperBom", "location": "Braga"},
    {"name": "EcoFoods", "location": "Faro"}
]


def _unique_product_names(n: int) -> list[str]:
    # Create a pool of unique product names from adjectives x bases
    pool = [f"{a} {b}" for a, b in itertools.product(_ADJECTIVES, _PRODUCT_BASES)]
    random.shuffle(pool)
    # If we still need more, append numbered variants
    while len(pool) < n:
        base = random.choice(_PRODUCT_BASES)
        adj = random.choice(_ADJECTIVES)
        pool.append(f"{adj} {base} {len(pool)+1}")
    return pool[:n]


def _random_barcode(i: int) -> str:
    # 13-digit-like string; keep unique by index
    root = 560000000000 + i  # PT-ish prefix 560 + zeros
    return str(root)


def generate_sample_data(n_products: int = 200, n_receipts: int = 20) -> Dict[str, Any]:
    today = date.today()
    rng = random.Random(42)  # deterministic for reproducibility

    categories = [{"name": c} for c in _DEFAULT_CATEGORIES]
    units = list(_DEFAULT_UNITS)

    names = _unique_product_names(n_products)

    # Map categories to plausible units
    cat_to_units = {
        "Fruit": ["kg", "g"],
        "Vegetable": ["kg", "g"],
        "Dairy": ["L", "mL", "u"],
        "Bakery": ["u", "pk"],
        "Meat": ["kg", "g"],
        "Fish": ["kg", "g"],
        "Beverages": ["L", "mL"],
        "Pantry": ["u", "pk", "kg", "g"],
        "Snacks": ["u", "pk"],
        "Frozen": ["u", "kg"],
        "Household": ["u", "pk"],
        "Personal Care": ["u", "pk"],
    }

    product_list = []
    for i, name in enumerate(names, start=1):
        category = rng.choice(_DEFAULT_CATEGORIES)
        unit_abbrev = rng.choice(cat_to_units[category])
        barcode = _random_barcode(i) if rng.random() < 0.65 else None
        product_list.append({
            "name": name,
            "barcode": barcode,
            "category": category,
            "measurement_unit": unit_abbrev,
        })

    merchants = list(_MERCHANTS)

    # Build receipts over the last ~90 days
    receipts = []
    for r in range(n_receipts):
        m = rng.choice(merchants)
        r_date = today - timedelta(days=rng.randint(0, 90))
        n_lines = rng.randint(5, 15)
        chosen_products = rng.sample(product_list, k=min(n_lines, len(product_list)))
        lines = []
        for pl in chosen_products:
            unit = pl["measurement_unit"]
            # Quantity distribution per unit
            if unit in ("kg", "L"):
                qty = Decimal(str(rng.uniform(0.2, 3.0))).quantize(Decimal("0.0001"))
            elif unit in ("g", "mL"):
                qty = Decimal(str(rng.randint(100, 2000))).quantize(Decimal("0.0001"))
            else:  # u, pk
                qty = Decimal(str(rng.randint(1, 6))).quantize(Decimal("0.0001"))
            price = (Decimal(str(rng.uniform(0.3, 20.0))) * qty).quantize(Decimal("0.0001"))
            lines.append({
                "product_list": pl["name"],
                "price": str(price),
                "quantity": str(qty),
                "description": rng.choice([None, "promo", "coupon", ""]),
            })
        receipts.append({
            "merchant": m["name"],
            "purchase_date": r_date.isoformat(),
            "barcode": None,
            "products": lines,
        })

    return {
        "categories": categories,
        "measurement_units": units,
        "product_list": product_list,
        "merchants": merchants,
        "receipts": receipts,
    }


# ----------------------- Runner -----------------------

def load_from_json(db: Session, payload: Dict[str, Any]) -> Dict[str, int]:
    cache = Cache()
    summary = {"categories": 0, "measurement_units": 0, "product_list": 0, "merchants": 0, "receipts": 0}

    with db.begin():  # single transaction
        summary["categories"] = load_categories(db, cache, payload.get("categories", []))
        summary["measurement_units"] = load_units(db, cache, payload.get("measurement_units", []))
        summary["product_list"] = load_product_list(db, cache, payload.get("product_list", []))
        summary["merchants"] = load_merchants(db, cache, payload.get("merchants", []))
        summary["receipts"] = load_receipts(db, cache, payload.get("receipts", []))

    return summary


def main(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(description="Load or generate grocery receipts dataset")
    parser.add_argument("json_path", nargs="?", help="Path to JSON file to load")
    parser.add_argument("--generate", dest="gen_path", help="Write a generated dataset to this JSON path and exit")
    parser.add_argument("--products", type=int, default=200, help="Number of product definitions to generate")
    parser.add_argument("--receipts", type=int, default=20, help="Number of receipts to generate")
    args = parser.parse_args(argv[1:])

    # Generation mode
    if args.gen_path:
        payload = generate_sample_data(n_products=args.products, n_receipts=args.receipts)
        out = Path(args.gen_path).expanduser().resolve()
        out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Wrote generated dataset to {out}")
        return

    # Load mode
    if not args.json_path:
        print("Usage: python -m load_json_to_db /path/to/data.json  OR  python -m load_json_to_db --generate sample.json --products 200 --receipts 20", file=sys.stderr)


    json_path = Path(args.json_path).expanduser().resolve()
    if not json_path.exists():
        print(f"File not found: {json_path}", file=sys.stderr)
        sys.exit(2)

    data = json.loads(json_path.read_text(encoding="utf-8"))

    try:
        with SessionLocal() as db:
            summary = load_from_json(db, data)
    except IntegrityError as ie:
        print("IntegrityError:", getattr(ie, "orig", ie), file=sys.stderr)
        sys.exit(1)
    except LoaderError as le:
        print("Error:", le, file=sys.stderr)
        sys.exit(1)

    print("Import complete:")
    for k, v in summary.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main(sys.argv)
