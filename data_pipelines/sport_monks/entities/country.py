import attr
from common.entity import EntityBase


@attr.s(auto_attribs=True)
class Country(EntityBase):
    """
    Entity that represents a country in sportmonks API
    """

    id: int
    continent_id: int
    name: str
    official_name: str
    fifa_name: str
    iso2: str
    iso3: str
    latitude: str
    longitude: str
    borders: list[str]
    image_path: str
