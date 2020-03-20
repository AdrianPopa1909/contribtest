from unittest import TestCase
import generate

class Tests(TestCase):
    def test_list_no_rst_file(self):
        expected = [('test/source/index.rst', 'index'), ('test/source/contact.rst', 'contact')]
        result = []

        for files in generate.list_files('test/source'):
            result.append(files)

        self.assertEqual(result, expected)

    def test_correct_read(self):
        expected = ({"title": "My awesome site", "layout": "home.html"},
                    "\nblah blah\n")
        result = generate.read_file('test/source/index.rst')

        self.assertEqual(result, expected)
