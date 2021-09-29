import logging
import os

from openpyxl import load_workbook

from analyzer_report import AnalyzerReport
from report_parsers.base_parser import Parser


class CoverityParser(Parser):
    ANALYZER_NAME = "coverity"

    COLUMNS_ORDER = (
        'CID',
        'Portal Url',
        'CodingStandards',
        'Checker',
        'Type',
        'Category',
        'File',
        'Line Number',
        'Function',
        'Occurance Count'
    )

    REPORT_PATH = "res/coverity.xlsx"

    def parse(self):

        wb = load_workbook(self.REPORT_PATH)
        ws = wb.active

        line_index = 0

        file_col = -1
        line_col = -1
        error_type_cols = []

        results = []

        for x in ws.values:

            if line_index == 0:  # columns names

                if not x == self.COLUMNS_ORDER:
                    logging.warning("Coverity report columns are in different order!")

                file_col = x.index("File")
                line_col = x.index("Line Number")
                error_type_cols = [
                    x.index("Checker"),
                    x.index("Type"),
                    x.index("Category"),
                ]

            else:

                file_val = x[file_col].strip("/\\")
                if not file_val.startswith("code"):
                    file_val = os.path.join("code", file_val)

                code_sample_val = os.path.dirname(file_val)
                line_val = x[line_col]
                error_type_val = "cov:" + ":".join([x[col] for col in error_type_cols])

                results.append((
                    code_sample_val,
                    file_val,
                    int(line_val),
                    error_type_val,
                    int(line_index)
                ))

            line_index += 1

        print(results[0])

        total_results = AnalyzerReport(results, self.ANALYZER_NAME, self.REPORT_PATH)

        return total_results
