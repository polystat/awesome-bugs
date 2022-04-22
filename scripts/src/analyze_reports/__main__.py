import logging
import os.path

from pylatex.base_classes import Options
from pylatex.utils import bold
from scripts.src.report_parsers import ClangTidyParser
from scripts.src.report_parsers import PolystatParser
from scripts.src.report_parsers import PolystatJavaParser
from scripts.src.report_parsers import SVFParser
from scripts.src.report_parsers import CppcheckParser
from pylatex import (
    Document,
    Tabular,
    Itemize,
    NewPage,
    MultiColumn,
    Section,
    Subsection,
    Enumerate,
    escape_latex,
    NoEscape,
    Package,
    Command,
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
        table = Tabular("|l|l|" + "r|" * 9, row_height=1.25)
        # Head
        table.add_hline()
        table.add_row(
            "Analyzer",
            "Defect title",
            "TP",
            "TN",
            "FP",
            "FN",
            "ERR",
            "Accuracy",
            "Precision",
            "Recall",
            "F1 score",
        )
        table.add_hline()

        # Body
        def get_row(analyzer_name, err, s):
            return [
                analyzer_name,
                err,
                s.true_positive,
                s.true_negative,
                s.false_positive,
                s.false_negative,
                s.exceptions,
                f"{100*s.accuracy:.1f}%",
                f"{100*s.precision:.1f}%",
                f"{100*s.recall:.1f}%",
                f"{100*s.F1:.1f}%",
            ]

        for analyzer, report in analyzer_reports.items():
            table.add_hline()
            for error, stat in report.error_statistics.items():
                table.add_row(get_row(analyzer, error, stat))
                table.add_hline()
            # total results for analyzer
            stat = report.statistic
            table.add_row(get_row(analyzer, "All", stat), mapper=bold)
            table.add_hline()
        doc.append(table)

    def generate_details_table():
        repo_url = "https://github.com/Polystat/awesome-bugs/blob/master/"
        test_paths = sorted(get_test_files_paths("tests"))
        table = Tabular("|l|" + "c|" * len(analyzer_reports), row_height=1.25)
        # table head
        table.add_hline()
        table.add_row(
            MultiColumn(size=1, data="File", align="|c|"),
            *[ar for ar in analyzer_reports.keys()],
        )
        table.add_hline()

        # table body
        results = {}
        for analyzer, report in analyzer_reports.items():
            # split error messages and exceptions
            expts, result_paths = [], []
            for ar in report.results:
                (expts, result_paths)[ar.error_type != "Exception"].append(
                    os.path.basename(
                        ar.file_path
                        if Path(ar.file_path).is_dir()
                        else os.path.dirname(ar.file_path)
                    )
                )
            results[analyzer] = [result_paths, expts]

        for test in test_paths:
            url = os.path.join(repo_url, test.replace("\\", "/"))
            txt = hyperlink(url, test.replace("tests/", ""))
            table.add_row(
                txt,
                *[
                    get_test_case_result(test, *results[ar])
                    for ar in analyzer_reports.keys()
                ],
            )
            table.add_hline()
        doc.append(table)

    def extract_error_messages():
        for analyzer, report in analyzer_reports.items():
            if len(report.results) != 0:
                with doc.create(Subsection(analyzer, numbering=False)):
                    with doc.create(Enumerate()) as en:
                        for result in report.results:
                            en.add_item(str(result))

    def get_template():
        temp_path = os.path.join("results", "report", "report-template.tex")
        with open(temp_path, "r") as r:
            file = r.read()

        results_list = list(analyzer_reports.values())
        number_of_tests = results_list[0].statistic.number_of_tests
        # c - stands for Clang-Tidy
        c = analyzer_reports["Clang-Tidy"]
        c_div_by_zero = c.error_statistics["division-by-zero"]
        # p - stands for Polystat for EO
        p = analyzer_reports["Polystat (EO)"]
        p_div_by_zero = p.error_statistics["division-by-zero"]
        p_mutual_recursion = p.error_statistics["mutual-recursion"]
        # pj - stands for Polystat for Java
        pj = analyzer_reports["Polystat (Java)"]
        pj_div_by_zero = p.error_statistics["division-by-zero"]
        pj_mutual_recursion = p.error_statistics["mutual-recursion"]

        c_p_div_by_zero = p_mutual_recursion.accuracy - c_div_by_zero.accuracy
        # With an assumption that clang will not find any mutual recursion
        c_p_mutual_recursion = p_mutual_recursion.accuracy - 0.5

        # Shorten formatting
        def f(n):
            return str(round(n * 100))

        file = (
            file.replace("#number_of_tests", str(number_of_tests))
            .replace("#c_div_by_zero", f(c_div_by_zero.accuracy))
            .replace("#p_mutual_recursion", f(p_mutual_recursion.accuracy))
            .replace("#p_div_by_zero", f(p_div_by_zero.accuracy))
            .replace("#pj_mutual_recursion", f(pj_mutual_recursion.accuracy))
            .replace("#pj_div_by_zero", f(pj_div_by_zero.accuracy))
            .replace("#c_p_div_by_zero", f(c_p_div_by_zero))
            .replace("#c_p_mutual_recursion", f(c_p_mutual_recursion))
        )
        return file

    # Create latex document
    doc = Document(
        documentclass=Command(
            "documentclass", options=Options("journal"), arguments="IEEEtran"
        )
    )
    doc.packages.append(Package(NoEscape("href-ul")))
    doc.packages.append(Package(NoEscape("minted")))
    doc.packages.append(Package(NoEscape("ffcode")))
    doc.packages.append(Package(NoEscape("mdframed")))
    doc.packages.append(Package(NoEscape("float")))
    doc.packages.append(Package(NoEscape("graphicx")))
    doc.packages.append(Package(NoEscape("biblatex")))
    doc.packages.append(Package(NoEscape("amsmath")))

    doc.packages.append(NoEscape("\\bibliography{references.bib}"))
    doc.append(NoEscape("\\usemintedstyle{bw}"))

    # Append the template
    doc.append(NoEscape(get_template()))

    with doc.create(Section("Statistic table", numbering=False)):
        generate_statistic_table()
        doc.append(NoEscape("\\vspace{0.5cm} Description"))
        ls = Itemize()
        ls.add_item("True Positive(TP) - warnings exist and should be")
        ls.add_item("True Negative(TN) - no warnings and shouldn't be")
        ls.add_item("False Negative(FN) - no warnings, but they should be")
        ls.add_item("False Positive(FP) - warnings exist but shouldn't be")
        ls.add_item("Errors(ERR) - errors/exceptions during analysis")
        doc.append(ls)

    doc.append(NewPage())
    with doc.create(Section("Details table", numbering=False)):
        generate_details_table()
        doc.append(NoEscape("\\vspace{0.5cm} Description"))
        ls = Itemize()
        ls.add_item("OK = TP and PN")
        ls.add_item("FN = FN and TP")
        ls.add_item("FP = FP and TN")
        ls.add_item("FF = FP and FN")
        ls.add_item("E - errors/exceptions during analysis")
        doc.append(ls)

    with doc.create(Section("Detected defect details", numbering=False)):
        extract_error_messages()

    # Generate final .tex file
    doc.generate_tex(os.path.join("results", "report", "report"))


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
        PolystatParser(): [],
        PolystatJavaParser(): [],
        ClangTidyParser(): [lambda row: row.error_type != "note"],
        SVFParser(): [],
        CppcheckParser(): [lambda row: row.error_type != "note"],
    }
    analyzer_reports: dict[AnalyzerReport] = {}

    for parser, predicates in parsers.items():
        report = parser.parse()
        for predicate in predicates:
            report = report.filter(predicate)
        analyzer_reports[parser.ANALYZER_NAME] = report

    for analyzer, report in analyzer_reports.items():
        report.update_statistic()

    generate_report(analyzer_reports)
    print("Done!")


if __name__ == "__main__":
    run()
