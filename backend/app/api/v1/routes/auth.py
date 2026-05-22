from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserLogin,UserRegister
from app.core.security import hash_password,verify_password,create_access_token

router = APIRouter()

@router.post("/register")
def register_user(user:UserRegister,db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already Registered"
        )
    hashed_pw = hash_password(user.password)

    new_user = User(
        email=user.email,
        hashed_password = hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "success":True,
        "message":"User Registered Successfully"
    }

@router.post("/login")
def login_user(user:UserLogin,db:Session=Depends(get_db)):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )
    
    valid_password = verify_password(user.password,db_user.hashed_password)

    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )
    access_token = create_access_token(
        data = {
            "sub":str(db_user.id),
            "role": db_user.role
        }
    )

    return {
        "success":True,
        "access_token":access_token,
        "token_type":"bearer"
    }