from fastapi import APIRouter

router = APIRouter()

# Suas rotas aqui
@router.get("/")
def get_receipts():
    return {"message": "receipts"}