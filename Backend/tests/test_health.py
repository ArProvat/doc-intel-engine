import os
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from psycopg import OperationalError

os.environ.setdefault("POSTGRES_PASSWORD", "test-only")

from app.main import live, ready  # noqa: E402


class HealthTests(unittest.IsolatedAsyncioTestCase):
    async def test_live(self) -> None:
        self.assertEqual(await live(), {"status": "ok"})

    async def test_ready_reports_database_failure(self) -> None:
        with patch("app.main.AsyncConnection.connect", side_effect=OperationalError("down")):
            with self.assertRaises(HTTPException) as raised:
                await ready()
        self.assertEqual(raised.exception.status_code, 503)
