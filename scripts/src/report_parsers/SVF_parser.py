import os
from functools import reduce

from parsy import string, regex, seq
from scripts.src.analyze_reports import AnalyzerReport, AnalyzerReportRow
from scripts.src.report_parsers.base_parser import Parser


def get_analyze_report_rows(row) -> list[AnalyzerReportRow]:
    # For now, only one error message expected
    path, message = row
    path = path.replace("temp/bc", "temp/sources/cpp").replace(".bc", "")
    results = []
    if message is not None:
        results = [
            AnalyzerReportRow(
                file_path=path,
                error_type="warning",
                error_message=message[0],
                error_position=(message[1], message[2]),
            )
        ]
    return results


class SVFParser(Parser):
    SOURCE_PATH = os.path.join("temp", "sources", "cpp")
    REPORT_PATH = os.path.join("results", "SVF-out.txt")
    ANALYZER_NAME = "SVF"

    def parse(self) -> AnalyzerReport:
        newline = string("\n")
        tab = string("\t")
        colon = string(":")
        space = string(" ")
        line_number = regex(r"[0-9]+").map(int)
        column_number = regex(r"[0-9]+").map(int)
        ob = string(" ({ ")
        line_caption = string("ln: ")
        column_caption = string("cl: ")
        error_message = regex(r"[a-zA-Z\s]+")
        text = regex(r"[a-zA-Z\s]+")
        stuff = regex(".*")

        filename = regex(r"[a-zA-Z0-9_\+\-\.\[\]]+")
        rel_path = filename.sep_by(sep=string("/"), min=1)
        abs_path = rel_path.map(
            lambda parsed: "/".join(parsed[parsed.index("temp"):])
        )

        analyzer_error = (
            seq(
                tab >> space >> error_message << colon,
                text >> colon >> ob >> line_caption >> line_number << space,
                space >> column_caption >> column_number << stuff,
            )
            << newline.at_least(1)
            << (
                tab << tab << text << colon << space << newline.at_least(2)
            ).optional()
        )
        svf_error = seq(abs_path << newline, analyzer_error.optional()).many()

        with open(self.REPORT_PATH) as file:
            file_content = file.read().strip() + "\n"
            parsed_output = svf_error.parse(file_content)

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
    pprint(SVFParser().parse(), width=140)
