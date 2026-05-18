from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SafeHome ESP-NOW - Dashboard"
    PROJECT_OWNER: str = "Grupo 4"
    VERSION: str = "1.0.0"
    
    # SQLite optimizado para escritura frecuente (RPi)
    SQLITE_POOL_SIZE: int = 5
    SQLITE_TIMEOUT: int = 30
    SQLITE_JOURNAL_MODE: str = "WAL"  
    SQLITE_SYNCHRONOUS: str = "NORMAL"
    SQLITE_CACHE_SIZE: int = -32000  # 32MB cache en memoria
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/sistema_seguridad.db"
    
    # Optimizaciones Uvicorn
    UVICORN_WORKERS: int = 1
    UVICORN_LIMIT_CONCURRENCY: int = 50
    UVICORN_TIMEOUT_KEEP_ALIVE: int = 5
    
    # Configuración de Caché
    CACHE_PATH: str = "./cache/sistema_seguridad.cache"
    CACHE_MAX_SIZE_MB: int = 50
    DEFAULT_TTL: int = 300
    
    # Parámetros del Sistema
    SENSOR_READING_INTERVAL_SEC: int = 5
    ALERT_COOLDOWN_SEC: int = 60
    WS_HEARTBEAT_INTERVAL_SEC: int = 30
    
    # Seguridad
    API_KEY_HEADER: str = "X-API-Key"
    ESP32_SECRET_KEY: str = "esp32-secret-key"
    JWT_SECRET: str = "cambiar-en-produccion"
    JWT_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()