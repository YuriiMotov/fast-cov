from typing import Annotated

from pydantic import AliasPath, BaseModel, Field


class GhCommit(BaseModel):
    sha: str
    message: Annotated[str, Field(validation_alias=AliasPath("commit", "message"))]


class GhCommitStatus(BaseModel):
    state: str
    description: str
    target_url: str
    context: str


class AWSUploadSessionResponse(BaseModel):
    site_id: str
    bucket: str
    region: str
    access_key_id: str
    secret_access_key: str
    session_token: str
