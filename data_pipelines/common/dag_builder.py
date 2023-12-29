from abc import ABC, abstractmethod

import attr
from airflow import DAG


class IDagBuilder(ABC):
    """
    Interface for DAG builder
    """

    @abstractmethod
    def build(self) -> DAG:
        """
        Abstract method to build DAG
        """
        raise NotImplementedError()


@attr.s(auto_attribs=True)
class DagCollector:
    """
    Class for collecting DAG builders
    """

    _builders: list[IDagBuilder] = attr.ib(factory=lambda: [], init=False)

    def add_dag(self, dag_builder: IDagBuilder):
        """
        Method to add DAG to collector
        """
        self._builders.append(dag_builder)

    def collect(self) -> list[DAG]:
        """
        Method to collect DAGs
        """
        return [builder.build() for builder in self._builders]
