import unittest

from lxml import html
from nameko.testing.services import worker_factory

from crawl_service import CrawlService


class CrawlServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = worker_factory(CrawlService)

    def test_discovering_repeating_paths(self):
        html_content = '''<div>
        <ul>
            <li><a href="/abc">foo</a></li>
            <li><a href="/def">bar</a></li>
        </ul>
        </div>'''
        tree = html.fromstring(html_content)
        expected_results = [ '//ul/li' ]
        self.assertEqual(self.service.discover_paths(tree), expected_results)

    def test_using_class_paths(self):
        html_content = '''<div class="container">
            <div class="item"><a href="/abc">foo</a></div>
            <div class="item"><a href="/def">bar</a></div>
        </div>'''
        tree = html.fromstring(html_content)
        expected_results = ['//div[@class="item"]']
        self.assertEqual(self.service.discover_paths(tree), expected_results)

    def test_assemble_paths(self):
        html_content = '<div><ul><li><a href="/abc">foo</a></li></ul></div>'
        tree = html.fromstring(html_content).getroottree()
        expected_results = { 'ul_87144201': [ { 'text': 'foo', 'href': 'http://www.abc.vn/abc' } ] }
        self.assertEqual(self.service.assemble_paths(tree, [ '//div/ul' ], root_url='www.abc.vn'), expected_results)
        self.assertEqual(self.service.assemble_paths(tree, [ '//div/ul' ], root_url='http://www.abc.vn'), expected_results)
        html_content = '<div><ul><li><a href="//www.abc.vn/abc">foo</a></li></ul></div>'
        tree = html.fromstring(html_content).getroottree()
        expected_results = { 'ul_87144201': [ { 'text': 'foo', 'href': 'http://www.abc.vn/abc' } ] }
        self.assertEqual(self.service.assemble_paths(tree, [ '//div/ul' ], root_url='www.abc.vn'), expected_results)

    def test_crawl_content(self):
        html_content = '''
            <body>
                <div><ul><li><a href="/abc">foo</a></li></ul></div>
                <div><span>bar</span></div>
                <div><table></table></div>
            </body>
        '''
        templates = [
            'div/ul/li/a',
            'div/span'
        ]
        expected_results = {
            'a_88000be6': [ { 'text': 'foo', 'href': '/abc' } ],
            'span_6d02cf61': [ 'bar' ]
        }
        self.assertEqual(self.service._crawl_content(html_content, templates), expected_results)

if __name__ == '__main__':
    unittest.main()
