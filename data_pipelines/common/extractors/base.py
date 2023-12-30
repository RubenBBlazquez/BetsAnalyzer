import attr
import pandas as pd


@attr.s(auto_attribs=True)
class ExtractorConfig:
    """
    Configuration needed by an extractor to get data from a db

    Attributes
    ----------
    collection: str
        Name of collection/table to read data
    query: Optional[dict]
        Query to filter data
    sort: Optional[dict]
        Sort data
    limit: Optional[int]
        Limit data
    offset: Optional[int]
        Offset data
    """

    collection: str
    query: dict = attr.ib(factory=lambda: {})
    sort: dict = attr.ib(factory=lambda: {"_id": -1})
    limit: int = attr.ib(default=0)
    offset: int = attr.ib(default=0)

    def __str__(self):
        return (
            f" query: {self.query},"
            f" sort: {self.sort},"
            f" limit: {self.limit},"
            f" offset: {self.offset}"
        )


@attr.s(auto_attribs=True)
class BaseExtractor:
    """
    Base Reader class
    """

    _extractors_config: list[ExtractorConfig]

    def extract(self) -> dict[str, pd.DataFrame]:
        """
        method to extract data
        """
        raise NotImplementedError()
