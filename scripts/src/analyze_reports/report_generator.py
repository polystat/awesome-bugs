import os.path

from pylatex.base_classes import Options
from scripts.src.utilities import get_test_files_paths
from pylatex import (
    Document,
    NewPage,
    MultiColumn,
    Section,
    escape_latex,
    NoEscape,
    Package,
    Command,
    LongTable,
    Tabularx,
    Table,
)
from scripts.src.analyze_reports.report import AnalyzerReport
from pathlib import Path


# Makes correct hyperlink in pylatex
def hyperlink(url, text):
    text = escape_latex(text)
    return NoEscape(r"\href{" + url + "}{" + text + "}")


class ReportGenerator:
    doc: Document
    results: dict[str, AnalyzerReport]

    def __init__(self, results, use_template):
        self.results = results

        if use_template:
            try:
                self.doc = self.get_doc_on_template()
            except KeyError:
                self.doc = self.get_doc()
                pass
        else:
            self.doc = self.get_doc()

        self.doc.packages.append(Package(NoEscape("href-ul")))
        self.doc.packages.append(Package(NoEscape("longtable")))
        self.doc.packages.append(Package(NoEscape("graphicx")))
        self.doc.packages.append(
            Package(NoEscape("cleveref"), options=["capitalize"])
        )
        self.doc.preamble.append(
            NoEscape(r"\newcommand{\rotate}{\rotatebox[origin=c]{90}}")
        )
        self.doc.preamble.append(
            NoEscape(r"\newcommand\polystat{{\scshape Polystat}}")
        )
        self.doc.preamble.append(NoEscape(r"\setlength\footskip{16pt}"))

    # Latex document based on an article template
    def get_doc_on_template(self):
        # Prepare template
        temp_path = os.path.join("results", "report", "report-template.tex")
        with open(temp_path, "r") as r:
            file = r.read()

        results_list = list(self.results.values())
        number_of_tests = results_list[0].statistic.number_of_tests
        # c - stands for Clang-Tidy
        c = self.results["Clang-Tidy"]
        c_div_by_zero = c.error_statistics["division-by-zero"]
        # p - stands for Polystat for EO
        p = self.results["Polystat (EO)"]
        p_div_by_zero = p.error_statistics["division-by-zero"]

        c_p_div_by_zero = c_div_by_zero.accuracy - p_div_by_zero.accuracy

        summary_table = self.generate_summary_statistic_table()

        # Shorten formatting
        def f(n):
            return str(round(n * 100))

        # Fill parameters
        file = (
            file.replace("#number_of_tests", str(number_of_tests))
            .replace("#c_div_by_zero", f(c_div_by_zero.accuracy))
            .replace("#c_p_div_by_zero", f(c_p_div_by_zero))
            .replace("#summary_table", summary_table.dumps())
        )

        # Create latex document
        d = Document(
            documentclass=Command(
                "documentclass",
                options=Options("11pt,sigplan,nonacm,natbib=false"),
                arguments="acmart",
            )
        )
        d.preamble.append(
            NoEscape(
                r"\settopmatter{printfolios=false,printccs=false,"
                + "printacmref=false}"
            )
        )
        d.packages.clear()
        d.packages.append(Package(NoEscape("paralist")))
        d.packages.append(Package(NoEscape("tabularx")))

        d.packages.append(Package(NoEscape("ffcode")))
        d.packages.append(
            Package(
                NoEscape("biblatex"),
                options=[
                    "maxnames=1,minnames=1,natbib=true,citestyle=authoryear,"
                    + "bibstyle=authoryear"
                ],
            )
        )
        d.packages.append(NoEscape("\\bibliography{references.bib}"))
        d.append(NoEscape("\\usemintedstyle{bw}"))

        # Append the template
        d.append(NoEscape(file))
        return d

    # A new Latex document without template
    def get_doc(self):
        geometry_options = {"margin": "0.5in", "top": "1in", "bottom": "1in"}
        return Document(geometry_options=geometry_options)

    def generate_report(self, report_path):
        with self.doc.create(Section("Statistic")):
            self.doc.append(
                NoEscape(
                    r"\Cref{tab:statistics} demonstrates detailed "
                    + "statistics collected for each static analyzer."
                )
            )
            self.doc.append(self.generate_statistic_table())

        self.doc.append(NewPage())
        with self.doc.create(Section("Details")):
            self.doc.append(
                NoEscape(
                    r"\Cref{tab:details} demonstrates detailed results for "
                    + "each test by each analyzer."
                )
            )
            self.doc.append(self.generate_details_table())

        # Generate final .tex file
        self.doc.generate_tex(report_path)

    def generate_summary_statistic_table(self):
        table = Table()
        table.append(Command("centering"))
        tabular = Tabularx("X|" + "r|" * 8 + "r")
        tabular.append(NoEscape("\\toprule"))
        # Head
        tabular.add_row(
            "Analyzer",
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

        # Body
        def get_row(analyzer_name, s):
            return [
                analyzer_name,
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

        tabular.append(NoEscape("\\midrule"))
        table._star_latex_name = True
        for analyzer, report in self.results.items():
            # total results for analyzer
            stat = report.statistic
            tabular.add_row(get_row(analyzer, stat))
        tabular.append(NoEscape("\\bottomrule"))
        table.append(tabular)
        table.add_caption(
            NoEscape(
                r"The comparison of performance metrics for \polystat{} "
                + "and other static analyzers"
            )
        )
        table.append(NoEscape(r"\label{tab:metrics}"))
        return table

    def generate_statistic_table(self):
        table = Table(position="ht")
        tabular = Tabularx("X|l|" + "r|" * 8 + "r", row_height=1.25)
        tabular.append(NoEscape("\\toprule"))
        # Head
        tabular.add_row(
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

        for analyzer, report in self.results.items():
            tabular.append(NoEscape("\\midrule"))
            for error, stat in report.error_statistics.items():
                tabular.add_row(get_row(analyzer, error, stat))
            # total results for analyzer
            stat = report.statistic
            tabular.add_row(get_row(analyzer, "All", stat))
        tabular.append(NoEscape("\\bottomrule"))
        table.append(tabular)
        table.add_caption(
            NoEscape(
                "Each analyzer has received the same set of tests and then "
                + r"its key metrics, which are explained in \cref{sec:metrics}"
                + ", have been collected: the left column includes the name "
                + "of the analyzer tested, the next one is the type of defect"
                + r" as explained in \cref{sec:types}, then one column per "
                + "each metric."
            )
        )
        table.append(NoEscape(r"\label{tab:statistics}"))
        return table

    def generate_details_table(self):
        repo_url = "https://github.com/Polystat/awesome-bugs/blob/master/"
        test_paths = sorted(get_test_files_paths("tests"))
        table = LongTable(
            "l|l|" + "c|" * (len(self.results) - 1) + "c", row_height=1.2
        )

        # table head
        table.append(NoEscape("\\toprule"))
        table.add_row(
            MultiColumn(size=1, data="Defect type", align="c|"),
            MultiColumn(size=1, data="File", align="c|"),
            *[Command("rotate", ar) for ar in self.results.keys()],
        )
        table.append(NoEscape("\\midrule"))

        # table body
        results = {}
        for analyzer, report in self.results.items():
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

        # Get all errors types
        temp_path = os.path.join("tests", "errors.txt")
        with open(temp_path, "r") as e:
            errors = e.read().splitlines()

        for test in test_paths:
            url = os.path.join(repo_url, test.replace("\\", "/"))
            label = os.path.basename(test)
            error_type = next(filter(lambda x: label.startswith(x), errors))
            label = label.replace(error_type + "-", "")
            error_type = error_type.replace("-", " ")

            table.add_row(
                error_type,
                hyperlink(url, label),
                *[
                    self.get_test_case_result(test, *results[ar])
                    for ar in self.results.keys()
                ],
            )
        table.append(NoEscape("\\bottomrule"))
        table.append(
            NoEscape(
                r"\caption{Here, ``P'' means pass for Bad and Good cases,"
                + "``PG'' means pass for Good cases,"
                + "``PB'' means pass for Bad cases,"
                + "``F'' means fails for Bad and Good cases,"
                + "and ``E'' means errors/exceptions during analysis}"
            )
        )

        table.append(NoEscape(r"\label{tab:details}"))
        return table

    def get_test_case_result(self, path, results, exceptions):
        case = os.path.basename(os.path.splitext(path)[0])
        # Name of test case which doesn't contain an error
        good = case + "-good"
        # Name of test case which contains an error
        bad = case + "-bad"
        if (good or bad) in exceptions:
            return "E"
        if bad in results and good not in results:
            return "P"
        if bad not in results and good in results:
            return "F"
        if bad not in results:
            return "PG"
        if good in results:
            return "PB"
