import hashlib
import logging
import requests

from lxml import etree
from lxml import html
from nameko.rpc import rpc
from nameko.rpc import RpcProxy


class CrawlService:
    name = "crawl_service"

    templates_rpc = RpcProxy('templates_service')

    FORBIDDEN_LINKS = [ '/' ]
    PATH_ID_DIGEST_SIZE = 4

    @rpc
    def discover(self, url):
        html_content = requests.get(url).content
        html_tree = html.fromstring(html_content)
        tree = html_tree.getroottree()
        paths = self.discover_paths(tree)
        results = self.assemble_paths(tree, paths)
        page_id = CrawlService.generate_path_id(url)
        return  {
            'status': 'done',
            'url': url,
            'page_id': page_id,
            'results': results
        }

    @rpc
    def crawl(self, urls):
        xpaths = self.templates_rpc.create_from_diff(urls[0], urls[1])
        logging.info(xpaths)
        results = list()
        for url in urls:
            logging.info(url)
            data = self.crawl_single(url, template)
            results.append({
                'url': url,
                'data': data
            })
        return {
            'status': 'done',
            'results': results
        }

    @rpc
    def crawl_single(self, url, template):
        tree = html.fromstring(requests.get(url).content)
        results = dict()
        for path in template:
            values = []
            tag = None
            for elem in tree.xpath(path):
                tag = elem.tag
                if elem.text and elem.text.strip():
                    values.append(elem.text_content().strip())
            if tag and values:
                path_id = CrawlService.generate_path_id(path)
                tag_key = '%s_%s' % (tag, path_id)
                results[ tag_key ] = values
        return results

    @rpc
    def get(self, page_id):
        # TODO (tri): return data from a crawled page.
        pass

    def assemble_paths(self, tree, paths):
        """Assemble paths results to a structured format."""
        results = dict()
        for path in paths:
            tag = tree.xpath(path)[0].tag
            path_id = CrawlService.generate_path_id(path)
            tag_key = '%s_%s' % (tag, path_id)
            # Find <a> element.
            link_xpath = '%s//a' % path
            elem_results = []
            # Gather the <a> element values.
            for elem in tree.xpath(link_xpath):
                href = elem.get('href')
                if elem.text and href and href not in self.FORBIDDEN_LINKS:
                    elem_results.append({
                        'href': elem.get('href'),
                        'text': elem.text.strip()
                    })
            # Store results to return full values.
            if elem_results:
                results[ tag_key ] = elem_results
        return results

    def discover_paths(self, tree):
        """Discover unique paths for searching sub pages."""
        # TODO (tri): search for repeating elements instead of searching for <ul>.
        # However, most of the sub pages will fall into this <ul> tag.
        ul_paths = []
        for elem in tree.xpath('//ul'):
            path = tree.getpath(elem)
            if self._is_unique(path, ul_paths):
                ul_paths.append(path)
        return ul_paths

    def _is_unique(self, new_path, existing_paths):
        for p in existing_paths:
            if p in new_path:
                return False
        return True

    @staticmethod
    def generate_path_id(path):
        # Create a deterministic ID for the path.
        return hashlib.blake2s(path.encode('UTF-8'), digest_size=CrawlService.PATH_ID_DIGEST_SIZE).hexdigest()
