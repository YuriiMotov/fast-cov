from contextlib import AsyncExitStack

import httpx
import stamina
from pydantic import SecretStr

from app.schemas import GhCommit, GhCommitStatus

BASE_URL = "https://api.github.com"


class GithubClientError(Exception):
    pass


class GithubClient:
    def __init__(self, token: SecretStr):
        self._token = token
        self._httpx_client: httpx.AsyncClient | None = None
        self._exit_stack = AsyncExitStack()

    def ensure_initialized(self) -> None:
        if self._httpx_client is None:
            raise GithubClientError("Client not initialized")

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"token {self._token.get_secret_value()}"}

    async def __aenter__(self):
        if self._httpx_client is not None:
            raise GithubClientError("Client already initialized")
        client = httpx.AsyncClient(base_url=BASE_URL, headers=self._headers())
        self._httpx_client = await self._exit_stack.enter_async_context(client)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.aclose()
        self._httpx_client = None

    async def _get(self, url: str, params: dict | None = None) -> httpx.Response:
        self.ensure_initialized()
        assert self._httpx_client is not None

        async for attempt in stamina.retry_context(
            on=(httpx.TransportError, httpx.HTTPStatusError),
            attempts=3,
            wait_jitter=2.0,
        ):
            with attempt:
                response = await self._httpx_client.get(url, params=params)
                if response.status_code >= 500:
                    response.raise_for_status()
        response.raise_for_status()
        return response

    async def get_latest_commits(
        self, owner: str, repo: str, limit: int = 5
    ) -> list[GhCommit]:
        response = await self._get(
            f"/repos/{owner}/{repo}/commits", params={"per_page": limit}
        )
        resp_json = response.json()
        assert isinstance(resp_json, list)
        return [GhCommit.model_validate(item) for item in resp_json]

    async def get_commit_statuses(
        self, owner: str, repo: str, sha: str
    ) -> list[GhCommitStatus]:
        response = await self._get(f"/repos/{owner}/{repo}/statuses/{sha}")
        resp_json = response.json()
        assert isinstance(resp_json, list)
        return [GhCommitStatus.model_validate(item) for item in resp_json]
