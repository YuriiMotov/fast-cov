from pydantic import SecretStr
import pytest

from app.utils.aws_storage import AWSStorage, AWSStorageError


@pytest.mark.asyncio
async def test_init():
    async with AWSStorage(
        "a_key_id", SecretStr("a_secret_key"), "bucket", "region", "arn"
    ) as storage:
        assert storage._client is not None


@pytest.mark.asyncio
async def test_double_init():
    with pytest.raises(AWSStorageError, match="Client already initialized"):
        async with AWSStorage(
            "a_key_id", SecretStr("a_secret_key"), "bucket", "region", "arn"
        ) as storage:
            async with storage:
                pass  # pragma: no cover


@pytest.mark.asyncio
async def test_generate_site_id_not_initialized():
    storage = AWSStorage(
        "a_key_id", SecretStr("a_secret_key"), "bucket", "region", "arn"
    )
    with pytest.raises(AWSStorageError, match="Client not initialized"):
        await storage._generate_site_id()


@pytest.mark.asyncio
async def test_get_file_not_initialized():
    storage = AWSStorage(
        "a_key_id", SecretStr("a_secret_key"), "bucket", "region", "arn"
    )
    with pytest.raises(AWSStorageError, match="Client not initialized"):
        await storage.get_file("site_id", "file_name")