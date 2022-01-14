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
    escape_latex,
    NoEscape,
    Package,
)
from scripts.src.analyze_reports.report import AnalyzerReport
from pathlib import Path


# Makes correct hyperlink in pylatex
def hyperlink(url, text):
    text = escape_latex(text)
    return NoEscape(r"\href{" + url + "}{" + text + "}")


# Searching for YAML files in the given path
def get_test_files_paths(code_path):
    test_case_paths = []
    for root, dirs, files in os.walk(code_path):
        for file in files:
            if file.endswith(".yml") or file.endswith(".yaml"):
                test_case_paths.append(os.path.join(root, file))
    return test_case_paths


# Generation latex report according to analyzers results
def generate_report(analyzer_reports):
    def generate_statistic_table():
        table = Tabular("|l|" + "r|" * 9, row_height=1.25)
        # Head
        table.add_hline()
        table.add_row(
            MultiColumn(
                size=1, data=MultiRow(size=2, data="Analyzer"), align="|c|"
            ),
            MultiColumn(size=2, data="True", align="c|"),
            MultiColumn(size=2, data="False", align="c|"),
            MultiRow(size=2, data="Errors"),
            MultiRow(size=2, data="Accuracy"),
            MultiRow(size=2, data="Precision"),
            MultiRow(size=2, data="Recall"),
            MultiRow(size=2, data="TPR"),
        )
        table.add_hline(2, 5)
        table.add_row(
            "",
            "Pos",
            "Neg",
            "Pos",
            "Neg",
            "",
            "",
            "",
            "",
            "",
        )
        table.add_hline()

        # Body
        for analyzer in analyzer_reports:
            stat = analyzer.statistic
            table.add_row(
                analyzer.analyzer,
                stat.true_positive,
                stat.true_negative,
                stat.false_positive,
                stat.false_negative,
                stat.exceptions,
                f"{stat.accuracy:.2f}",
                f"{stat.precision:.2f}",
                f"{stat.recall:.2f}",
                f"{stat.true_positives_rate:.2f}",
            )
            table.add_hline()
        doc.append(table)

    def generate_details_table():
        repo_url = "https://github.com/Polystat/awesome-bugs/blob/master/"
        test_paths = sorted(get_test_files_paths("tests"))
        table = Tabular("|l|c|c|", row_height=1.25)
        # table head
        table.add_hline()
        table.add_row(
            MultiColumn(size=1, data="File", align="|c|"),
            *[ar.analyzer for ar in analyzer_reports],
        )
        table.add_hline()

        # table body
        results = {}
        for analyzer in analyzer_reports:
            # split error messages and exceptions
            expts, result_paths = [], []
            for ar in analyzer.results:
                (expts, result_paths)[ar.error_type != "Exception"].append(
                    os.path.basename(
                        ar.file_path
                        if Path(ar.file_path).is_dir()
                        else os.path.dirname(ar.file)
                    )
                )
            results[analyzer.analyzer] = [result_paths, expts]

        for test in test_paths:
            url = os.path.join(repo_url, test.replace("\\", "/"))
            txt = hyperlink(url, test)
            table.add_row(
                txt,
                *[
                    get_test_case_result(test, *results[ar.analyzer])
                    for ar in analyzer_reports
                ],
            )
            table.add_hline()
        doc.append(table)

    def extract_error_messages():
        for analyzer in analyzer_reports:
            if len(analyzer.results) != 0:
                with doc.create(
                    Subsection(analyzer.analyzer, numbering=False)
                ):
                    with doc.create(Enumerate()) as en:
                        for result in analyzer.results:
                            en.add_item(str(result))

    # Create latex document
    geometry_options = {
        "margin": "0.5in",
        "top": "1in",
        "bottom": "1in",
    }
    doc = Document(geometry_options=geometry_options)
    doc.packages.append(Package(NoEscape("href-ul")))
    doc.append(Command("large"))

    with doc.create(Section("Statistic table", numbering=False)):
        generate_statistic_table()
        with doc.create(Subsection("Description", numbering=False)):
            with doc.create(Itemize()) as ls:
                ls.add_item("True Positive - warnings exist and should be")
                ls.add_item("True Negative - no warnings and shouldn't be")
                ls.add_item("False Negative - no warnings, but they should be")
                ls.add_item("False Positive - warnings exist but shouldn't be")
                ls.add_item("TPR - true positives rate")

    doc.append(NewPage())
    with doc.create(Section("Details table", numbering=False)):
        generate_details_table()
        with doc.create(Subsection("Description", numbering=False)):
            with doc.create(Itemize()) as ls:
                ls.add_item("OK = TP and PN")
                ls.add_item("FN = FN and TP")
                ls.add_item("FP = FP and TN")
                ls.add_item("E - an exception was thrown during analysis")

    doc.append(NewPage())
    with doc.create(Section("Error messages", numbering=False)):
        extract_error_messages()

    doc.generate_tex(os.path.join("results", "report"))


# Determines how the analyzer worked
def get_test_case_result(path, results, exceptions):
    case = os.path.basename(os.path.splitext(path)[0])
    # Name of test case which doesn't contain an error
    good = case + "-good"
    # Name of test case which contains an error
    bad = case + "-bad"
    if (good or bad) in exceptions:
        return "E"
    if bad in results and good not in results:
        return "OK"
    if bad not in results and good in results:
        return "FF"
    if bad not in results:
        return "FN"
    if good in results:
        return "FP"


def run():
    logging.basicConfig(level=logging.DEBUG)

    parsers = {
        ClangTidyParser(): [lambda row: row.error_type != "note"],
        PolystatParser(): [],
    }
    analyzer_reports: list[AnalyzerReport] = []

    for parser, predicates in parsers.items():
        report = parser.parse()
        for predicate in predicates:
            report = report.filter(predicate)
        analyzer_reports.append(report)

    for analyzer in analyzer_reports:
        analyzer.calculate_statistic()

    generate_report(analyzer_reports)
    print("Done!")


if __name__ == "__main__":
    run()
