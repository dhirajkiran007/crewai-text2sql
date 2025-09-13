import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class DBTypeEnum(str, Enum):
    """Enum for supported database types."""
    SQLITE = 'sqlite'
    POSTGRES = 'postgres'

class Config:
    """Configuration class for environment variables."""
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DB_TYPE = os.getenv("DB_TYPE", DBTypeEnum.SQLITE.value)
    
    # SQLite Configuration
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH")
    
    # PostgreSQL Configuration
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    
    @classmethod
    def get_db_type_enum(cls) -> DBTypeEnum:
        """Get validated DB type as enum."""
        try:
            return DBTypeEnum(cls.DB_TYPE.lower())
        except ValueError:
            valid_options = [e.value for e in DBTypeEnum]
            raise ValueError(f"Invalid DB_TYPE: '{cls.DB_TYPE}'. Valid options: {valid_options}")
    
    @classmethod
    def get_postgres_connection_string(cls) -> str:
        """Build PostgreSQL connection string from individual parameters."""
        return f"host={cls.POSTGRES_HOST} port={cls.POSTGRES_PORT} dbname={cls.POSTGRES_DB} user={cls.POSTGRES_USER} password={cls.POSTGRES_PASSWORD}"
    
    @classmethod
    def get_db_config(cls) -> dict:
        """Get database configuration based on DB_TYPE."""
        db_type = cls.get_db_type_enum()
        
        if db_type == DBTypeEnum.SQLITE:
            return {
                'db_type': db_type.value,
                'db_path': cls.SQLITE_DB_PATH,
                'conn_string': None
            }
        elif db_type == DBTypeEnum.POSTGRES:
            return {
                'db_type': db_type.value,
                'db_path': None,
                'conn_string': cls.get_postgres_connection_string()
            }
    
    @classmethod
    def validate(cls):
        """Validate required environment variables."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Validate DB_TYPE using enum
        db_type = cls.get_db_type_enum()
        
        if db_type == DBTypeEnum.SQLITE and not cls.SQLITE_DB_PATH:
            raise ValueError("SQLITE_DB_PATH is required when DB_TYPE is 'sqlite'")
        
        if db_type == DBTypeEnum.POSTGRES:
            required_postgres_vars = [cls.POSTGRES_DB, cls.POSTGRES_USER, cls.POSTGRES_PASSWORD]
            if not all(required_postgres_vars):
                raise ValueError("POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD are required when DB_TYPE is 'postgres'")
