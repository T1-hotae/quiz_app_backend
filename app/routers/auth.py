# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 체크
    exists = db.query(User).filter(User.email == user.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already exists")

    # 비밀번호 해시 + 유저 생성
    hashed = hash_password(user.password)
    new_user = User(
        email=user.email,
        name=user.name,
        department=user.department,  # ✅ 학과 저장
        password_hash=hashed,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserOut.model_validate(user),  # ✅ department도 포함됨
    }

@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    """
    내 프로필 조회: 이메일, 이름, 학과
    """
    return current_user