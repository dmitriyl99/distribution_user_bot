from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv('.env')


class Settings(BaseSettings):
    telegram_bot_token: str


settings = Settings()
