from fastapi import APIRouter

router = APIRouter(prefix="/user")

@router.post("/signup")
def user_signup_handler():
    return  True

