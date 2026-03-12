from typing import cast

from fastapi import Request

from utils.github_client import GithubClient


async def get_github_client(request: Request) -> GithubClient:
    return cast(GithubClient, request.state.gh_client)
