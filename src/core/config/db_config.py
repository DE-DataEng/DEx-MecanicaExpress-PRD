from dataclasses import dataclass
import os
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class PostgresConfig:
    _db_url = os.getenv("DATABASE_URL")
    if _db_url:
        _parsed = urlparse(_db_url)
        _query = parse_qs(_parsed.query)
        host: str = _parsed.hostname or "localhost"
        port: int = _parsed.port or 5432
        database: str = (_parsed.path or "").lstrip("/") or "postgres"
        user: str = _parsed.username or "postgres"
        password: str = _parsed.password or "postgres"
        sslmode: str = _query.get("sslmode", [os.getenv("DB_SSLMODE", "require")])[0]
    else:
        host: str = os.getenv("DB_HOST", os.getenv("MECEXP_DB_HOST", "localhost"))
        port: int = int(os.getenv("DB_PORT", os.getenv("MECEXP_DB_PORT", "5432")))
        database: str = os.getenv("DB_NAME", os.getenv("MECEXP_DB_NAME", "postgres"))
        user: str = os.getenv("DB_USER", os.getenv("MECEXP_DB_USER", "postgres"))
        password: str = os.getenv("DB_PASSWORD", os.getenv("MECEXP_DB_PASSWORD", "postgres"))
        sslmode: str = os.getenv("DB_SSLMODE", "prefer")

    def safe_info(self) -> str:
        return (
            f"host={self.host} port={self.port} "
            f"db={self.database} user={self.user} sslmode={self.sslmode}"
        )
