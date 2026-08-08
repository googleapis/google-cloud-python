import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from google.cloud.sqlalchemy_spanner.sqlalchemy_spanner_asyncio import (
    SpannerDialect_asyncio,
)
from sqlalchemy.testing.plugin.plugin_base import fixtures

class AsyncioTest(fixtures.TestBase):
    @pytest.mark.asyncio
    async def test_async_engine_creation(self):
        assert os.environ.get("SPANNER_EMULATOR_HOST") is not None
        engine = create_async_engine("spanner+spanner_asyncio:///projects/p/instances/i/databases/d")
        assert engine.dialect.is_async
        assert isinstance(engine.dialect, SpannerDialect_asyncio)

    @pytest.mark.asyncio
    async def test_async_connection(self, mocker):
        from sqlalchemy import text
        from sqlalchemy.pool import NullPool
        assert os.environ.get("SPANNER_EMULATOR_HOST") is not None
        engine = create_async_engine(
            "spanner+spanner_asyncio:///projects/p/instances/i/databases/d",
            poolclass=NullPool
        )
        
        # We need to mock the underlying sync connect
        mock_connect = mocker.patch("google.cloud.spanner_dbapi.connect")
        mock_sync_conn = mock_connect.return_value
        mock_sync_cursor = mock_sync_conn.cursor.return_value
        
        # When we call execute, it should work through the async adapter
        async with engine.connect() as conn:
            assert conn.dialect == engine.dialect
            # This will eventually call cursor.execute in a thread
            await conn.execute(text("SELECT 1"))
            
        mock_connect.assert_called_once()
        mock_sync_conn.close.assert_called_once()
        mock_sync_cursor.execute.assert_called_once()
