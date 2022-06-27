import os
from functools import reduce

from parsy import string, regex, seq
from scripts.src.analyze_reports import AnalyzerReport, AnalyzerReportRow
from scripts.src.report_parsers.base_parser import Parser
import json


def get_analyze_report_rows(row) -> list[AnalyzerReportRow]:
    path, results_json = row
    results = json.loads(results_json)["runs"][0]

    for result in results["results"]:
        err = result["locations"][0]["physicalLocation"]["region"]["startLine"]
        return [
            AnalyzerReportRow(
                file_path=path,
                error_type=result["ruleId"],
                error_position=err,
                error_message=result["message"]["text"],
            )
        ]
    return []


class SpotbugsParser(Parser):
    SOURCE_PATH = os.path.join("temp", "sources", "java")
    REPORT_PATH = os.path.join("results", "spotbugs-out.txt")
    ANALYZER_NAME = "Spotbugs"

    def parse(self) -> AnalyzerReport:
        newline = string("\n")
        error_message = regex(".*")
        left_brace = string("{")

        filename = regex(r"[a-zA-Z0-9_\+\-\.\[\]]+")
        rel_path = filename.sep_by(sep=string("/"), min=1)
        abs_path = rel_path.map(
            lambda parsed: "/".join(parsed[parsed.index("temp"):])
        )

        json_row = left_brace + error_message << newline.at_least(1)
        spotbugs_error = seq(abs_path << newline, json_row.optional()).many()

        with open(self.REPORT_PATH) as report:
            file_content = report.read().strip() + "\n"
            parsed_output = spotbugs_error.parse(file_content)

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

    pprint(SpotbugsParser().parse(), width=140)
