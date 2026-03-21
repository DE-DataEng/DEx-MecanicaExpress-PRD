from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class PostgresConfig:
    host: str = os.getenv("DB_HOST", os.getenv("MECEXP_DB_HOST", "localhost"))
    port: int = int(os.getenv("DB_PORT", os.getenv("MECEXP_DB_PORT", "5432")))
    database: str = os.getenv("DB_NAME", os.getenv("MECEXP_DB_NAME", "postgres"))
    user: str = os.getenv("DB_USER", os.getenv("MECEXP_DB_USER", "postgres"))
    password: str = os.getenv("DB_PASSWORD", os.getenv("MECEXP_DB_PASSWORD", "postgres"))
    sslmode: str = os.getenv("DB_SSLMODE", "prefer")
