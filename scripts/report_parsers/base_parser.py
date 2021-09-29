from abc import abstractmethod
from analyzer_report import AnalyzerReport


class Parser:
    ANALYZER_NAME: str
    REPORT_PATH: str

    @abstractmethod
    def parse(self) -> AnalyzerReport:
        raise NotImplemented()
