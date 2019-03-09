import hashlib
import logging
import requests

from lxml import etree
from lxml import html
from nameko.rpc import rpc
from nameko.rpc import RpcProxy
from urllib.parse import urlparse


class CrawlService:
    name = "crawl_service"

    templates_rpc = RpcProxy('templates_service')

    FORBIDDEN_LINKS = [ '/' ]
    PATH_ID_DIGEST_SIZE = 4

    @rpc
    def discover(self, root_url):
        html_content = requests.get(root_url).content
        html_tree = html.fromstring(html_content)
        tree = html_tree.getroottree()
        paths = self.discover_paths(tree)
        url_parse = urlparse( root_url )
        url_domain = '%s://%s' % (url_parse.scheme, url_parse.netloc)
        url_results = self.assemble_paths(tree, paths, url_domain)
        page_id = CrawlService.generate_path_id(root_url)
        return {
            'status': 'done',
            'url': root_url,
            'domain': url_domain,
            'page_id': page_id,
            'results': url_results
        }

    @rpc
    def crawl(self, url):
        """Crawl a page into data."""
        # Get the right template for the template service.
        template = self.templates_rpc.create(url)
        logging.info(template)
        # Crawl the page to acquire the data.
        page_content = requests.get(url).content
        results = self._crawl_content(
            page_content=page_content,
            template=template,
        )
        return {
            'status': 'done',
            'url': url,
            'results': results
        }

    @rpc
    def get(self, page_id):
        # TODO (tri): return data from a crawled page.
        pass

    def assemble_paths(self, tree, paths, url_domain):
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
                    href = elem.get('href')
                    is_relative_path = len(href) > 0 and href[0] == '/'
                    if is_relative_path:
                        href = url_domain + href
                    elem_results.append({
                        'href': href,
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

    def _crawl_content(self, page_content, template):
        # Parse the page and follow the paths.
        tree = html.fromstring(page_content)
        results = dict()
        # Iterate through valuable paths and gather the right data.
        for path in template:
            values = []
            tag = None
            for elem in tree.xpath(path):
                tag = elem.tag
                if elem.text and elem.text.strip():
                    if tag == 'a':
                        values.append({
                            'href': elem.get('href'),
                            'text': elem.text_content().strip()
                        })
                    else:
                        values.append(elem.text_content().strip())
            if tag and values:
                path_id = CrawlService.generate_path_id(path)
                tag_key = '%s_%s' % (tag, path_id)
                results[ tag_key ] = values
        return results

    @staticmethod
    def generate_path_id(path):
        # Create a deterministic ID for the path.
        return hashlib.blake2s(path.encode('UTF-8'), digest_size=CrawlService.PATH_ID_DIGEST_SIZE).hexdigest()
