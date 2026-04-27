from pydantic import SecretStr
import pytest

from app.utils.github_client import GithubClient, GithubClientError


@pytest.mark.asyncio
async def test_init():
    async with GithubClient(
        SecretStr("token")
    ) as client:
        assert client._httpx_client is not None


@pytest.mark.asyncio
async def test_double_init():
    with pytest.raises(GithubClientError, match="Client already initialized"):
        async with GithubClient(
            SecretStr("token")
        ) as client:
            async with client:
                pass  # pragma: no cover


@pytest.mark.asyncio
async def test_get_latest_commits_not_initialized():
    client = GithubClient(SecretStr("token"))
    with pytest.raises(GithubClientError, match="Client not initialized"):
        await client.get_latest_commits("owner", "repo")


@pytest.mark.asyncio
async def test_get_commit_statuses_not_initialized():
    client = GithubClient(SecretStr("token"))
    with pytest.raises(GithubClientError, match="Client not initialized"):
        await client.get_commit_statuses("owner", "repo", "sha")