from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CONTROLLER_URL: str = "http://localhost:8000"
    AGENT_HOST: str = "localhost"
    AGENT_PORT: int = 8001
    AGENT_NAME: str = "default-agent"
    DATABASE_URL: str = "postgresql://user:password@localhost/iptables_agent"
    
    class Config:
        env_file = ".env"


settings = Settings()
