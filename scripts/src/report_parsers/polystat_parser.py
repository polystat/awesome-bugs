import os
from parsy import string, regex, seq
from scripts.src.analyze_reports import (
    AnalyzerReport,
    AnalyzerReportRow,
)
from scripts.src.report_parsers.base_parser import Parser


class PolystatParser(Parser):
    SOURCE_PATH = os.path.join("temp", "sources", "eo")
    REPORT_PATH = os.path.join("results", "eo-out.txt")
    ANALYZER_NAME = "Polystat"

    def parse(self) -> AnalyzerReport:
        newline = string("\n")
        space = string(" ")

        colon = string(":")
        colon_space = seq(colon, space)
        error_message = regex(".*")
        _path = regex(".*")
        r_chain = regex(".*")

        odin_error = (
            seq(
                string("AnOdin"),
                (colon_space >> error_message << newline)
                + (r_chain << newline),
            )
            << (
                string("AnOdin")
                << colon_space
                << error_message
                << newline
                << r_chain
                << newline
            ).optional()
        )
        far_error = seq(
            string("AnFaR"),
            colon_space >> error_message << newline,
        )
        _error = odin_error | far_error

        polystat_error = seq(_path << newline, _error.at_least(0))
        polystat_report = seq(polystat_error.at_least(0)).map(
            lambda lst: {
                "errors": list(lst[0]),
            }
        )

        with open(self.REPORT_PATH) as report:
            # rewrite this part, it can look better
            file_content = (report.read() + "\n").replace("No errors\n", "")
            res = polystat_report.parse(file_content)
            # filter from stuff
            res = list(filter(lambda x: (len(x[1]) > 0), res["errors"]))
            # join error info and path
            results = []
            for el in res:
                path = el[0].replace("temp/polystat", "temp/sources/eo")
                for in_el in el[1]:
                    results.append(
                        AnalyzerReportRow(
                            file=path,
                            error_position=(0, 0),
                            error_type=in_el[0],
                            error_message=in_el[1],
                        )
                    )

            return AnalyzerReport(
                results,
                self.ANALYZER_NAME,
                self.SOURCE_PATH,
                self.REPORT_PATH,
            )


if __name__ == "__main__":
    from pprint import pprint

    pprint(PolystatParser().parse(), width=140)
