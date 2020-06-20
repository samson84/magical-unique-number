from typing import Optional

def get_postgres_dsn(
        password: str, 
        db_name: str, 
        host: Optional[str] = 'localhost', 
        port: Optional[int] = 5432,         
        user: Optional[str] = 'postgres') -> str:
    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
