from parsy import string, regex, seq

from scripts.src.analyze_reports import AnalyzerReport, AnalyzerReportRow
from scripts.src.report_parsers.base_parser import Parser
from itertools import chain


class ClangTidyParser(Parser):
    REPORT_PATH = "res/clang-out"
    ANALYZER_NAME = "clang-tidy"

    def parse(self) -> AnalyzerReport:
        newline = string("\n")
        indent = string(" " * 4)
        space = string(" ")
        check_value = regex(r'.*')
        check = indent >> check_value << newline
        checks = string("Enabled checks:") >> newline >> check.at_least(1)

        filename = regex(r"[a-zA-Z0-9_\+\-\.]+")
        rel_path = filename.sep_by(sep=string("/"), min=1)
        abs_path = (
                string("/") >>
                rel_path
        ).map(lambda parsed: "/".join(parsed[parsed.index("code"):]))
        command = (
                string("clang-tidy") >> space >>
                string("-p=") >> rel_path >> space
                >> abs_path << newline
        )
        colon = string(":")
        colon_space = seq(colon, space)
        line_number = regex(r"[0-9]+").map(int)
        column_number = regex(r"[0-9]+").map(int)
        error_type = string("warning") | string("note")
        error_message = regex(".*")
        code_snippet = regex(".*")
        highlighting = regex(".*")
        analyzer_error = (
                seq(
                    abs_path,
                    colon >> line_number,
                    colon >> column_number,
                    colon_space >> error_type,
                    colon_space >> error_message
                ) << newline <<
                (
                        string(" " * 8) << code_snippet << newline <<
                        string(" " * 8) << highlighting << newline
                ).optional()
        ).map(
            lambda lst: AnalyzerReportRow(
                file=lst[0],
                line_number=lst[1],
                column_number=lst[2],
                error_type=lst[3],
                error_message=lst[4]
            )
        )
        clang_tidy_error = seq(
            command >> analyzer_error.at_least(0))
        clang_tidy_report = seq(
            checks << newline,
            clang_tidy_error.at_least(0)
        ).map(
            lambda lst: {
                "checks": lst[0],
                "errors": list(chain.from_iterable(
                    [lst[0] for lst in lst[1]]
                ))
            }
        )
        with open(self.REPORT_PATH) as report:
            return AnalyzerReport(
                clang_tidy_report.parse(report.read().strip() + "\n")['errors'],
                self.ANALYZER_NAME,
                self.REPORT_PATH
            )


if __name__ == '__main__':
    from pprint import pprint

    pprint(ClangTidyParser().parse(), width=140)
