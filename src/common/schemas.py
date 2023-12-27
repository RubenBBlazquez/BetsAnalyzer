from typing import Any

from pydantic import BaseModel


class GETResponseModel(BaseModel):
    """
    Base class for all GET response models
    """

    data: list[Any]
    message: str
    status_code: int
