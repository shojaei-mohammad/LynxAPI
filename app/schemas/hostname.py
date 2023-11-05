from pydantic import BaseModel, Field


class Hostname(BaseModel):
    """
    Represents a schema for updating the system's hostname.

    The `Hostname` model is used to define the expected structure and validation
    for the hostname setting request. It contains a single field `hostname`
    which is a required string. An example and a description for the field are provided
    to aid in generating documentation and to provide context for the field's usage.

    Attributes:
        hostname (str): A string representing the new hostname to be set for the system.
    """

    # The `hostname` field is of type `str`. It is required (`...` means no default value
    # and the field is not optional). An example value "new-hostname" is provided,
    # which can be used in documentation or auto-generated example requests.
    # The description clearly states the purpose of the field.
    hostname: str = Field(
        ..., example="new-hostname", description="The desired hostname for the system."
    )
