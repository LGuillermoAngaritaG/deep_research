from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    MODEL_NAME: str
    CONTEXT7_API_KEY: str
    TAVILY_API_KEY: str
    class Config:
        #ignore extra fields
        extra = "ignore"
        env_file = ".env"