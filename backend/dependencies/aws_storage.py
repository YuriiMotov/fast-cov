from typing import cast

from fastapi import Request

from utils.aws_storage import AWSStorage


async def get_aws_storage(request: Request) -> AWSStorage:
    return cast(AWSStorage, request.state.aws_storage_client)
