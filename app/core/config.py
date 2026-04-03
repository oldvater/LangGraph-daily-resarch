from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "LangGraph"
    API_V1_STR: str = "/api/v1"
    
    # LLM API Keys
    OPENAI_API_KEY: str | None = None
    DEEPSEEK_API_KEY: str = "" # 增加这一行，让 pydantic 自动从 .env 读取
    GITHUB_TOKEN: str = "" # 让 pydantic 自动读取你在 .env 里的 GITHUB_TOKEN
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_HOST: str = ""
    LANGFUSE_HOST: str = ""
    TAVILY_API_KEY: str = ""
    
    # Database / Vector DB Settings (For Future)
    VECTOR_DB_URL: str = "localhost"



    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
