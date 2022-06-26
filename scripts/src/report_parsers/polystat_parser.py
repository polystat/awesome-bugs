import os
from functools import reduce
import urllib.parse

from scripts.src.analyze_reports import (
    AnalyzerReport,
    AnalyzerReportRow,
    AnalyzerReportExceptionRow,
)
from scripts.src.report_parsers.base_parser import Parser
import json


def get_analyze_report_rows(row) -> list[AnalyzerReportRow]:
    path = urllib.parse.unquote(row["artifacts"][0]["location"]["uri"])
    path = path.split("file://")[1].replace(os.path.abspath(os.curdir)+"/", "")

    for result in row["results"]:
        # Need to add ruleId
        if result["kind"] != "pass":
            return [
                AnalyzerReportRow(
                    file_path=path,
                    error_type=result["ruleId"],
                    error_message=result["message"]["text"],
                )
            ]

    exceptions = []
    for invocation in row["invocations"]:
        if not invocation["executionSuccessful"]:
            notification = invocation["toolExecutionNotifications"][0]
            message = notification["message"]["text"]
            rule = notification["associatedRule"]["id"]
            defect = rule.lower().replace(" ", "-")
            if defect in path:
                exceptions.append(
                    AnalyzerReportExceptionRow(
                        file_path=path,
                        error_message=f"An exception by {rule}: [{message}]",
                    )
                )
    return exceptions


class PolystatParser(Parser):
    # Since Polystat can work with different languages, the parser
    # can be parameterized through the constructor (with EO by default)
    def __init__(
        self,
        sources=os.path.join("temp", "sources", "eo"),
        result_file=os.path.join("results", "polystat-eo-out.txt"),
        language="Polystat (EO)",
    ):
        self.SOURCE_PATH = os.path.join("temp", "sources", sources)
        self.REPORT_PATH = os.path.join("results", result_file)
        self.ANALYZER_NAME = f"Polystat ({language})"

    def parse(self) -> AnalyzerReport:

        with open(self.REPORT_PATH) as report:
            file_content = report.read()
            results = json.loads(file_content)["runs"]

        analyzer_results = reduce(
            lambda x, y: x + get_analyze_report_rows(y),
            results,
            [],
        )

        return AnalyzerReport(
            analyzer_results,
            self.ANALYZER_NAME,
            self.SOURCE_PATH,
            self.REPORT_PATH,
        )


if __name__ == "__main__":
    from pprint import pprint

    pprint(PolystatParser().parse(), width=140)
