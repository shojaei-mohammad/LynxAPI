from typing import Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    username: str = Field(
        description="The username of the account associated with the token."
    )
    access_token: Optional[str] = Field(
        default=None,
        description="The generated access token for the user. This token is used for authentication and authorization "
        "purposes.",
    )
    token_type: Optional[str] = Field(
        default=None,
        description="The type of the access token. Common types include 'Bearer', 'OAuth2', etc.",
    )
