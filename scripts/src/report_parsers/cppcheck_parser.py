import os

from parsy import string, regex, seq
from scripts.src.analyze_reports import AnalyzerReport, AnalyzerReportRow
from scripts.src.report_parsers.base_parser import Parser


class CppcheckParser(Parser):
    SOURCE_PATH = os.path.join("temp", "sources", "cpp")
    REPORT_PATH = os.path.join("results", "cppcheck-out.txt")
    ANALYZER_NAME = "Cppcheck"

    def parse(self) -> AnalyzerReport:
        newline = string("\n")
        comma = string(",")
        line_number = regex(r"[0-9]+").map(int)
        column_number = regex(r"[0-9]+").map(int)
        error_type = string("warning") | string("note") | string("error")
        error_message = regex(".*")

        filename = regex(r"[a-zA-Z0-9_\+\-\.]+")
        rel_path = filename.sep_by(sep=string("/"), min=1)
        abs_path = rel_path.map(
            lambda parsed: "/".join(parsed[parsed.index("temp"):])
        )

        analyzer_error = (
            seq(
                abs_path,
                comma >> line_number,
                comma >> column_number,
                comma >> error_type,
                comma >> error_message,
            )
            << newline
        ).map(
            lambda lst: AnalyzerReportRow(
                file_path=lst[0],
                error_position=(lst[1], lst[2]),
                error_type=lst[3],
                error_message=lst[4],
            )
        )
        error = analyzer_error.many()

        with open(self.REPORT_PATH) as report:
            file_content = report.read().strip() + "\n"
            parsed_output = error.parse(file_content)
            return AnalyzerReport(
                parsed_output,
                self.ANALYZER_NAME,
                self.SOURCE_PATH,
                self.REPORT_PATH,
            )


if __name__ == "__main__":
    from pprint import pprint

    pprint(CppcheckParser().parse(), width=140)
