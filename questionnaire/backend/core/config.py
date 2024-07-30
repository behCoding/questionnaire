import os
from dotenv import load_dotenv
from pydantic import BaseSettings  #Install pydantic v.1.*


# Load environment variables from the .env file
load_dotenv()

# set SECRET_KEY='81d909e92278c05e87a48c2853d8bbd1a3cc2cb950f67bd409be55e7c3d7c6fa'
# set DATABASE_URL=
# set ALGORITHM= "HS256" or export for linux


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

    class Config:
        case_sensitive = True


settings = Settings()
