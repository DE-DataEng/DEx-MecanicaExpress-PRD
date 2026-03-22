from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional
import logging

import psycopg2
from psycopg2 import sql
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerificationError, VerifyMismatchError

from src.core.config import PostgresConfig


@dataclass(frozen=True)
class AuthTableConfig:
    schema: str
    table: str
    password_column: str
    search_column: str


class PostgresAuthenticator:
    def __init__(
        self,
        db_config: PostgresConfig,
        table_config: AuthTableConfig,
        verify_func: Optional[Callable[[str, str], bool]] = None,
    ) -> None:
        self._db_config = db_config
        self._table_config = table_config
        self._verify_func = verify_func

    def authenticate(self, search_value: str, password_value: str) -> bool:
        query = sql.SQL(
            "SELECT {pwd} FROM {schema}.{table} WHERE {search} = %s LIMIT 1"
        ).format(
            pwd=sql.Identifier(self._table_config.password_column),
            schema=sql.Identifier(self._table_config.schema),
            table=sql.Identifier(self._table_config.table),
            search=sql.Identifier(self._table_config.search_column),
        )

        logging.getLogger(__name__).info("Postgres connect: %s", self._db_config.safe_info())

        with psycopg2.connect(
            host=self._db_config.host,
            port=self._db_config.port,
            dbname=self._db_config.database,
            user=self._db_config.user,
            password=self._db_config.password,
            sslmode=self._db_config.sslmode,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (search_value,))
                row = cur.fetchone()

        if not row:
            return False

        stored_password = row[0]
        if stored_password is None:
            return False

        if self._verify_func:
            return bool(self._verify_func(password_value, str(stored_password)))

        return str(stored_password) == password_value


def verify_argon2(plain_password: str, stored_hash: str) -> bool:
    hasher = PasswordHasher()
    try:
        return hasher.verify(stored_hash, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHash):
        return False
