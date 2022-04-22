import os
from functools import reduce

from parsy import string, regex, seq
from scripts.src.analyze_reports import (
    AnalyzerReport,
    AnalyzerReportRow,
    AnalyzerReportExceptionRow,
)
from scripts.src.report_parsers.base_parser import Parser
import json


def get_analyze_report_rows(row) -> list[AnalyzerReportRow]:
    path, results_json = row
    results = json.loads(results_json)["runs"][0]

    for result in results["results"]:
        if result["kind"] != "pass":
            return [
                AnalyzerReportRow(
                    file_path=path,
                    error_type=result["ruleId"],
                    error_message=result["message"]["text"],
                )
            ]

    exceptions = []
    for invocation in results["invocations"]:
        if not invocation["executionSuccessful"]:
            notification = invocation["toolExecutionNotifications"][0]
            message = notification["message"]["text"]
            rule = notification["associatedRule"]["id"]
            defect = rule.split("/")[1].lower().replace(" ", "-")
            if defect in path:
                exceptions.append(
                    AnalyzerReportExceptionRow(
                        file_path=path,
                        error_message=f"An exception by {rule}: [{message}]",
                    )
                )
    return exceptions


class PolystatJavaParser(Parser):
    SOURCE_PATH = os.path.join("temp", "sources", "j2eo")
    REPORT_PATH = os.path.join("results", "polystat-j2eo-out.txt")
    ANALYZER_NAME = "Polystat (Java)"

    def parse(self) -> AnalyzerReport:
        newline = string("\n")
        error_message = regex(".*")
        left_brace = string("{")

        filename = regex(r"[a-zA-Z0-9_\+\-\.]+")
        rel_path = filename.sep_by(sep=string("/"), min=1)
        abs_path = rel_path.map(
            lambda parsed: "/".join(parsed[parsed.index("temp"):])
        )

        json_row = left_brace + error_message << newline.at_least(1)
        polystat_error = seq(abs_path << newline, json_row.optional()).many()

        with open(self.REPORT_PATH) as report:
            file_content = report.read().strip() + "\n"
            parsed_output = polystat_error.parse(file_content)

            # join error info and path
            analyzer_results = reduce(
                lambda x, y: x + get_analyze_report_rows(y), parsed_output, []
            )

            return AnalyzerReport(
                analyzer_results,
                self.ANALYZER_NAME,
                self.SOURCE_PATH,
                self.REPORT_PATH,
            )


if __name__ == "__main__":
    from pprint import pprint

    pprint(PolystatJavaParser().parse(), width=140)
