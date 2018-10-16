import unittest

from lxml import etree
from nameko.testing.services import worker_factory

from crawl_service import CrawlService


class CrawlServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = worker_factory(CrawlService)

    def test_discovering_root_paths(self):
        html_content = '<div><ul><li><a href="/abc">foo</a></li></ul></div>'
        tree = etree.fromstring(html_content).getroottree()
        expected_results = [ '/div/ul' ]
        self.assertEqual(self.service.discover_paths(tree), expected_results)

    def test_assemble_paths(self):
        html_content = '<div><ul><li><a href="/abc">foo</a></li></ul></div>'
        tree = etree.fromstring(html_content).getroottree()
        expected_results = { 'ul_3bff4e27': [ { 'text': 'foo', 'href': '/abc' } ] }
        self.assertEqual(self.service.assemble_paths(tree, [ '/div/ul' ]), expected_results)


if __name__ == '__main__':
    unittest.main()
