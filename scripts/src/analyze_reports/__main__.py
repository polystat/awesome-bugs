import os
import sys

from scripts.src.report_parsers import ClangTidyParser
from scripts.src.report_parsers import PolystatParser
from scripts.src.report_parsers import SVFParser
from scripts.src.report_parsers import CppcheckParser
from scripts.src.report_parsers import SpotbugsParser
from scripts.src.analyze_reports.report import AnalyzerReport
from scripts.src.analyze_reports.report_generator import ReportGenerator


def run():
    # Read arguments
    if len(sys.argv) == 2:
        based_on_template = sys.argv[1].lower() == "true"
    else:
        print("Wrong number of arguments")
        return

    spotbugs_exclude_list = [
        "SIC_INNER_SHOULD_BE_STATIC",
        "UC_USELESS_OBJECT",
        "URF_UNREAD_PUBLIC_OR_PROTECTED_FIELD",
        "RV_RETURN_VALUE_IGNORED_NO_SIDE_EFFECT",
    ]

    parsers = {
        PolystatParser("eo", "polystat-eo-out.txt", "EO"): [],
        PolystatParser("j2eo", "polystat-j2eo-out.txt", "Java"): [],
        ClangTidyParser(): [lambda row: row.error_type != "note"],
        SVFParser(): [],
        CppcheckParser(): [lambda row: row.error_type != "note"],
        SpotbugsParser(): [
            lambda row: row.error_type not in spotbugs_exclude_list
        ],
    }
    analyzer_reports: dict[AnalyzerReport] = {}

    for parser, predicates in parsers.items():
        report = parser.parse()
        for predicate in predicates:
            report = report.filter(predicate)
        analyzer_reports[parser.ANALYZER_NAME] = report

    for analyzer, report in analyzer_reports.items():
        report.update_statistic()

    rg = ReportGenerator(analyzer_reports, based_on_template)
    rg.generate_report(os.path.join("results", "report", "report"))
    print("Done!")


if __name__ == "__main__":
    run()
