import unittest

from lxml import html
from nameko.testing.services import worker_factory

from templates_service import TemplatesService


class TemplatesServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = worker_factory(TemplatesService)

    def test_diff_html_acquire_new_paths(self):
        html1_content = '<div><ul><li><a href="/abc">foo1</a></li></ul></div>'
        html2_content = '<div><ul><li><a href="/abc">foo2</a></li></ul></div>'
        tree1 = html.fromstring(html1_content)
        tree2 = html.fromstring(html2_content)
        expected_results = [ 'div/ul/li/a' ]
        self.assertEqual(self.service.diff_html(tree1, tree2), expected_results)

    def test_diff_html_ignore_redundant_paths(self):
        html1_content = '<div><ul><li><a href="/abc">foo</a></li><li><span>foo123</span></li></ul></div>'
        html2_content = '<div><ul><li><a href="/abc">foo</a></li><li><span>foo456</span></li></ul></div>'
        tree1 = html.fromstring(html1_content)
        tree2 = html.fromstring(html2_content)
        expected_results = [ 'div/ul/li/span' ]
        self.assertEqual(self.service.diff_html(tree1, tree2), expected_results)

if __name__ == '__main__':
    unittest.main()
