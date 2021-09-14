import unittest
from analyzer_report import AnalyzerReport

class TestStringMethods(unittest.TestCase):

    def test_ok(self):
        self.assertTrue(AnalyzerReport.validate_results([("a", "a.java", 1, "NPE", 3123), ("b", "b.java", 12, "NPE", 64321)]))

    def test_not_list(self):
        self.assertFalse(AnalyzerReport.validate_results("string"))

    def test_not_tuples(self):
        self.assertFalse(AnalyzerReport.validate_results(["string"]))

    def test_tuple_size(self):
        self.assertFalse(AnalyzerReport.validate_results([("string")]))
        self.assertFalse(AnalyzerReport.validate_results([(1, 2, 3, 4, 5, 6)]))

    def test_ok(self):
        self.assertFalse(AnalyzerReport.validate_results([("a", "a.java", 1, "NPE", "3123, oops")]))

if __name__ == '__main__':
    unittest.main()