import unittest

from lxml import html
from nameko.testing.services import worker_factory

from templates_service import TemplatesService


class TemplatesServiceTest(unittest.TestCase):

    def setUp(self):
        self.service = worker_factory(TemplatesService)
        self.maxDiff = None

    def test_diff_html_acquire_new_paths(self):
        html1_content = '<div><ul><li><a href="/abc">foo1</a></li></ul></div>'
        html2_content = '<div><ul><li><a href="/abc">foo2</a></li></ul></div>'
        tree1 = html.fromstring(html1_content)
        tree2 = html.fromstring(html2_content)
        expected_results = [ 'ul/li/a' ]
        self.assertEqual(self.service.diff_html(tree1, tree2), expected_results)

    def test_diff_html_ignore_redundant_paths(self):
        html1_content = '<div><ul><li><a href="/abc">foo</a></li><li><span>foo123</span></li></ul></div>'
        html2_content = '<div><ul><li><a href="/abc">foo</a></li><li><span>foo456</span></li></ul></div>'
        tree1 = html.fromstring(html1_content)
        tree2 = html.fromstring(html2_content)
        expected_results = [ 'ul/li/span' ]
        self.assertEqual(self.service.diff_html(tree1, tree2), expected_results)

    def test_score_url_similarity_zero_domain(self):
        url1 = 'http://vnn.vn/abc/def'
        url2 = 'http://abc.vn'
        self.assertEqual(self.service.score_url_similarity(url1, url2), 0)

    def test_score_url_similarity_invalid_path(self):
        url1 = 'http://vnn.vn/abc/def'
        url2 = '/'
        self.assertEqual(self.service.score_url_similarity(url1, url2), 0)

    def test_score_url_similarity_full(self):
        url1 = 'http://vnn.vn/abc/def/123'
        url2 = 'http://vnn.vn/abc/def/ghi/'
        self.assertEqual(self.service.score_url_similarity(url1, url2), 2/3)

    def test_score_url_similarity_partial(self):
        url1 = 'http://vnn.vn/abc/def/123'
        url2 = 'http://vnn.vn/abc/ikj/ghi/'
        self.assertEqual(self.service.score_url_similarity(url1, url2), 1/3)

    def test_search_similar_links(self):
        url = 'http://vnn.vn/abc/def/jkl/123'
        url1 = 'http://vnn.vn/abc/def/123'
        url2 = 'http://vnn.vn/abc/def/ghi/'
        url3 = 'http://vnn.vn/abc/def/jkl/abc/def'
        expected_results = [ (url3, 3/4) ]
        similar_links = self.service.search_similar_links(
            url,
            [ url1, url2, url3 ]
        )
        self.assertListEqual(similar_links, expected_results)

    def test_find_link_urls(self):
        root_url = 'http://vietnamnet.vn/vn/thoi-su/chinh-tri/vn'
        page_content = '''<div><ul>
            <li><a href="/thoi-su/van-hoa/">foo1</a></li>
            <li><a href="/thoi-su/chinh-tri/abc">foo2</a></li>
            <li><a href="/thoi-su/van-hoa/123">foo3</a></li>
        </ul></div>'''
        link_urls = self.service._find_link_urls(root_url, page_content)
        expected_results = [
            'http://vietnamnet.vn/thoi-su/van-hoa/',
            'http://vietnamnet.vn/thoi-su/chinh-tri/abc',
            'http://vietnamnet.vn/thoi-su/van-hoa/123'
        ]
        self.assertListEqual(link_urls, expected_results)


if __name__ == '__main__':
    unittest.main()
