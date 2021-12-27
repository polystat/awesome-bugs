import logging
import os.path

from scripts.src.report_parsers import ClangTidyParser
from scripts.src.report_parsers import PolystatParser
from pylatex import (
    Document,
    Command,
    Tabular,
    Itemize,
    NewPage,
    MultiRow,
    MultiColumn,
    Section,
    Subsection,
    Enumerate,
)
from scripts.src.analyze_reports.report import AnalyzerReport


def generate_report(analyzer_reports):
    geometry_options = {
        "margin": "0.5in",
        "top": "1in",
        "bottom": "1in",
    }
    doc = Document(geometry_options=geometry_options)
    doc.append(Command("large"))

    with doc.create(Section("Report", numbering=False)):
        with doc.create(Tabular("|l|c|c|c|c|c|", row_height=1.25)) as table:
            table.add_hline()
            table.add_row(
                MultiRow(size=2, data="Analyzer"),
                MultiColumn(size=2, data="Positive", align="c|"),
                MultiColumn(size=2, data="Negative", align="c|"),
                MultiRow(size=2, data="Errors"),
            )
            table.add_hline(2, 5)
            table.add_row(
                "",
                "True",
                "False",
                "True",
                "False",
                "",
            )
            table.add_hline()

            for analyzer in analyzer_reports:
                stat = analyzer.statistic
                neg = stat.true_negative + stat.false_positive
                pos = stat.true_positive + stat.false_negative
                table.add_row(
                    analyzer.analyzer,
                    f"{stat.true_positive}/{pos}",
                    f"{stat.false_positive}/{neg}",
                    f"{stat.true_negative}/{neg}",
                    f"{stat.false_negative}/{pos}",
                    0,
                )
                table.add_hline()

    with doc.create(Subsection("Description", numbering=False)):
        with doc.create(Itemize()) as ls:
            ls.add_item("True Positive - warnings exist and should be")
            ls.add_item("True Negative - no warnings and shouldn't be")
            ls.add_item("False Negative - no warnings, but they should be")
            ls.add_item("False Positive - warnings exist but shouldn't be")

    doc.append(NewPage())
    with doc.create(Section("Details", numbering=False)):
        for analyzer in analyzer_reports:
            if len(analyzer.results) == 0:
                break
            with doc.create(Subsection(analyzer.analyzer, numbering=False)):
                with doc.create(Enumerate()) as ls:
                    for result in analyzer.results:
                        ls.add_item(str(result))

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
        analyzer.calculate_statistic()

    generate_report(analyzer_reports)

    print("Done!")


if __name__ == "__main__":
    run()
