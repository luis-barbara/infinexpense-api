from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from typing import List, Optional
from datetime import date
from src.models.receipt_product import Product
from src.models.product import ProductList
from src.models.category import Category
from src.models.receipt import Receipt
from src.schemas import category as category_schema


AVAILABLE_COLORS = [
                '#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', 
                '#14b8a6', '#ec4899', '#f97316', '#06b6d4', '#6366f1',
                '#84cc16', '#a855f7'
            ]


class CategoryService:
    @staticmethod
    def get_category(db: Session, category_id: int) -> Optional[Category]:
        """Get a category by ID."""
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def get_categories(db: Session, skip: int = 0, limit: int = 100, start_date: date = None, end_date: date = None) -> List[dict]:
        """Get all categories with pagination, aggregated data, and optional date filtering."""
        all_categories = db.query(Category).all()
        for idx, category in enumerate(all_categories):
            if not category.color or category.color == '#808080':
                category.color = AVAILABLE_COLORS[idx % len(AVAILABLE_COLORS)]
                db.add(category)
        
        db.commit()
        
        # Get total item count across ALL categories
        total_query = db.query(func.count(Product.id)).join(
            ProductList, Product.product_list_id == ProductList.id
        ).join(
            Receipt, Product.receipt_id == Receipt.id
        )
        
        # Apply date filter if provided
        if start_date:
            total_query = total_query.filter(Receipt.purchase_date >= start_date)
        if end_date:
            total_query = total_query.filter(Receipt.purchase_date <= end_date)
        
        total_items = total_query.scalar() or 1
        
        result = []
        for category in all_categories:
            # Build query for item count in this category
            item_query = db.query(func.count(Product.id)).join(
                ProductList, Product.product_list_id == ProductList.id
            ).join(
                Receipt, Product.receipt_id == Receipt.id
            ).filter(ProductList.category_id == category.id)
            
            # Apply date filter
            if start_date:
                item_query = item_query.filter(Receipt.purchase_date >= start_date)
            if end_date:
                item_query = item_query.filter(Receipt.purchase_date <= end_date)
            
            item_count = item_query.scalar() or 0
            
            # Build query for total spent in this category
            spent_query = db.query(func.sum(Product.price)).join(
                ProductList, Product.product_list_id == ProductList.id
            ).join(
                Receipt, Product.receipt_id == Receipt.id
            ).filter(ProductList.category_id == category.id)
            
            # Apply date filter
            if start_date:
                spent_query = spent_query.filter(Receipt.purchase_date >= start_date)
            if end_date:
                spent_query = spent_query.filter(Receipt.purchase_date <= end_date)
            
            total_spent = spent_query.scalar() or 0.0
            
            # Calculate percentage of total items
            item_percentage = (item_count / total_items * 100) if total_items > 0 else 0.0
            
            category_dict = {
                'id': category.id,
                'name': category.name,
                'color': category.color,
                'item_count': item_count,
                'item_percentage': round(item_percentage, 1),
                'total_spent': round(float(total_spent), 2)
            }
            
            result.append(category_dict)
        
        # Apply pagination to the result
        return result[skip:skip + limit]

    @staticmethod
    def create_category(db: Session, category_data: category_schema.CategoryCreate) -> Category:
        """Create a new category with auto-assigned color."""
        existing = db.query(Category).filter_by(name=category_data.name).first()
        if existing:
            raise ValueError("Category with this name already exists")

        db_category = Category(**category_data.model_dump())
        
        # Get the next available color
        existing_categories = db.query(Category).all()
        color_index = len(existing_categories) % len(AVAILABLE_COLORS)
        assigned_color = AVAILABLE_COLORS[color_index]
        
        db_category.color = assigned_color
        db.add(db_category)

        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("Error creating category")

        db.refresh(db_category)
        return db_category

    @staticmethod
    def update_category(db: Session, db_category: Category, update_data: category_schema.CategoryUpdate) -> Category:
        """Update a category."""
        update_dict = update_data.model_dump(exclude_unset=True)
        if 'name' in update_dict:
            existing = db.query(Category).filter(
                Category.name == update_dict['name'],
                Category.id != db_category.id
            ).first()
            if existing:
                raise ValueError("Category with this name already exists")

        for key, value in update_dict.items():
            setattr(db_category, key, value)

        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def delete_category(db: Session, db_category: Category) -> Category:
        """Delete a category."""
        db.delete(db_category)
        db.commit()
        return db_category