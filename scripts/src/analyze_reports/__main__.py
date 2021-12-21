import logging
import os.path

from scripts.src.report_parsers import ClangTidyParser
from scripts.src.report_parsers import PolystatParser
from pylatex import Document, Command, Tabular
from scripts.src.analyze_reports.report import AnalyzerReport


def generate_report(analyzer_reports):
    tests_count = 5
    doc = Document()
    doc.append(Command("huge"))
    doc.append("Tests count: " + str(tests_count) + "\n\n")

    with doc.create(Tabular("l l l")) as table:
        table.add_hline()
        table.add_row(
            (
                "Analyzer",
                "Hits",
                "Misses",
            )
        )
        table.add_hline()

        for analyzer in analyzer_reports:
            hit_rate = round(analyzer.hits * 100 / tests_count, 2)
            miss_rate = round(analyzer.misses * 100 / tests_count, 2)
            table.add_row(
                [
                    analyzer.analyzer,
                    f"{analyzer.hits} ({hit_rate}%)",
                    f"{analyzer.misses} ({miss_rate}%)",
                ]
            )
    doc.generate_tex(os.path.join("results", "report"))


def run():
    logging.basicConfig(level=logging.DEBUG)

    parsers = {
        ClangTidyParser(): [lambda row: row.error_type != "note"],
        PolystatParser(): [],
    }
    analyzer_reports: list[AnalyzerReport] = []

    for parser, preds in parsers.items():
        report = parser.parse()
        for pred in preds:
            report = report.filter(pred)
        analyzer_reports.append(report)

    for analyzer in analyzer_reports:
        for result in analyzer.results:
            if result.file.find("-good") != -1:
                analyzer.misses += 1
            if result.file.find("-bad") != -1:
                analyzer.hits += 1

    generate_report(analyzer_reports)

    print("Done!")


if __name__ == "__main__":
    run()
