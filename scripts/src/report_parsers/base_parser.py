from abc import abstractmethod
from scripts.src.analyze_reports import AnalyzerReport


class Parser:
    ANALYZER_NAME: str
    SOURCE_PATH: str
    REPORT_PATH: str

    @abstractmethod
    def parse(self) -> AnalyzerReport:
        raise NotImplementedError()
