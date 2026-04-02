from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
def get_test():
    return {"Message": "Router funcionando"}
