from src.base_tool import BaseCustomTool
import sqlite3
import psycopg
from typing import Dict, Any

class ExecuteSQLQuery(BaseCustomTool):
    def __init__(self):
        super().__init__(
            name="SQL Query Executor",
            description="This tool validates and executes SQL queries on the connected database (SQLite or PostgreSQL) to fetch data."
        )

    def _run(self, query: Dict[str, str], db_path: str = None, db_type: str = 'sqlite', conn_string: str = None) -> Dict[str, Any]:
        if not self.validate_input({'query': query, 'db_type': db_type}):
            return self.handle_error(ValueError("Invalid input parameters"))
            
        try:
            if db_type == 'sqlite':
                if not db_path:
                    raise ValueError("SQLite requires db_path.")
                conn = sqlite3.connect(db_path)
            elif db_type == 'postgres':
                if not conn_string:
                    raise ValueError("PostgreSQL requires conn_string.")
                conn = psycopg.connect(conn_string)
            else:
                raise ValueError("Unsupported db_type. Use 'sqlite' or 'postgres'.")

            with conn.cursor() as cursor:
                sql = query['sql']
                cursor.execute(sql)
                conn.commit()

                if sql.strip().lower().startswith("select"):
                    result = cursor.fetchall()
                    output = {'status': 'success', 'message': 'Query executed successfully', 'data': result}
                else:
                    output = {'status': 'success', 'message': 'Query executed successfully', 'data': None}
                
                return output if self.validate_output(output) else self.handle_error(ValueError("Invalid output"))

        except Exception as e:
            return self.handle_error(e)

execute_sql_query_tool = ExecuteSQLQuery()
