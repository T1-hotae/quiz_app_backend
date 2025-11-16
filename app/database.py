# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

from pathlib import Path


load_dotenv()

# 1) .env에 없으면 기본값으로 SQLite 사용
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./quiz_ai.db")

# 2) SQLite일 때만 필요한 옵션 추가
if DB_URL.startswith("sqlite"):
    engine = create_engine(
        DB_URL,
        echo=True,
        connect_args={"check_same_thread": False},  # SQLite 전용
    )
else:
    engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("🔥 USING DB_URL =", DB_URL)
if DB_URL.startswith("sqlite:///"):
    db_path = DB_URL.replace("sqlite:///", "")
    print("🔥 절대 경로 DB 파일:", Path(db_path).resolve())