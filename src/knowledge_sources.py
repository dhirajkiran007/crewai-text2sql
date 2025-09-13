from src.base_knowledge_source import BaseCustomKnowledgeSource
import sqlite3
import psycopg
from typing import Dict, List, Optional
from pydantic import Field

class DatabaseKnowledgeSource(BaseCustomKnowledgeSource):
    """Knowledge source that fetches schema from SQLite or PostgreSQL."""
    
    db_path: Optional[str] = Field(default=None, description="Path to SQLite database")
    db_type: str = Field(description="Database type: 'sqlite' or 'postgres'")
    conn_string: Optional[str] = Field(default=None, description="Connection string for PostgreSQL")

    def load_content(self) -> Dict[str, Dict[str, List[str]]]:
        try:
            schema = self._fetch_schema()
            return self.format_schema(schema)
        except Exception as e:
            self.handle_connection_error(e)

    def _fetch_schema(self) -> Dict[str, List[str]]:
        """Fetch schema based on database type."""
        if self.db_type == 'sqlite':
            return self._fetch_sqlite_schema()
        elif self.db_type == 'postgres':
            return self._fetch_postgres_schema()
        else:
            raise ValueError("Unsupported db_type. Use 'sqlite' or 'postgres'.")

    def _fetch_sqlite_schema(self) -> Dict[str, List[str]]:
        """Fetch schema from SQLite database."""
        if not self.db_path:
            raise ValueError("SQLite requires db_path.")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        schema = {}
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = [col[1] for col in cursor.fetchall()]
            schema[table] = columns

        conn.close()
        return schema

    def _fetch_postgres_schema(self) -> Dict[str, List[str]]:
        """Fetch schema from PostgreSQL database."""
        if not self.conn_string:
            raise ValueError("PostgreSQL requires conn_string.")
        
        conn = psycopg.connect(self.conn_string)
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = [row[0] for row in cursor.fetchall()]

        schema = {}
        for table in tables:
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s;", (table,))
            columns = [col[0] for col in cursor.fetchall()]
            schema[table] = columns

        conn.close()
        return schema
