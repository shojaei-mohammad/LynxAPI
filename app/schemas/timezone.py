from pydantic import BaseModel, Field


class Timezone(BaseModel):
    timezone: str = Field(
        ...,  # This indicates that the field is required
        example="Asia/Tehran",
        description="Timezone in the format 'Region/City', e.g., 'Asia/Tehran'.",
    )
