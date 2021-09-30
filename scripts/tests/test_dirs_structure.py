import unittest
from check_format.parameters_parser import analyze_dirs


class TestStringMethods(unittest.TestCase):

    def test_ok(self):
        ok_input = [
            ("/", ["a", "b"], ["d.txt"]),
            ("/a/s_1", [], ["s.cc", "README.md"]),
            ("/a/s_2", [], ["s.cc", "README.md", "s.eo"]),
            ("/a/s_3", [], ["s.cc", "README.md", "s1.eo", "s2.eo"]),
            ("/a/s_4", [], ["s.java", "README.md"]),
            ("/a/s_5", [], ["s.java", "README.md", "filters.txt"]),
            ("/b", ["d", "e"], []),
            ("/b/d", [], ["s.java", "README.md"]),
            ("/b/e", [], ["s.java", "README.md"]),
        ]
        self.assertIsNotNone(analyze_dirs(ok_input))

    def test_no_readme(self):
        test_input = [
            ("/", [], ["s.cc"])
        ]
        self.assertIsNone(analyze_dirs(test_input))

    def test_no_source_file(self):
        test_input = [
            ("/", [], ["README.md"])
        ]
        self.assertIsNone(analyze_dirs(test_input))

    def test_multiple_source_file(self):
        test_input = [
            ("/", [], ["s1.cc", "s2.cc", "README.md"])
        ]
        self.assertIsNone(analyze_dirs(test_input))

    def test_unnecessary_file(self):
        test_input = [
            ("/", [], ["s1.cc", "README.md", "hello.txt"])
        ]
        self.assertIsNone(analyze_dirs(test_input))


if __name__ == '__main__':
    unittest.main()
