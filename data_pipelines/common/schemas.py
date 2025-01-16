from typing import Any

from pydantic import BaseModel


class GETResponseModel(BaseModel):
    """
    Base class for all GET response models.
    This class defines the structure of the response from GET requests.
    """

    data: list[Any]
    message: str
    status_code: int
