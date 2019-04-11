import hashlib
import logging
import requests

from lxml import html
from nameko.rpc import rpc
from nameko.rpc import RpcProxy
from selenium.webdriver.chrome import options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from urllib.parse import urlparse

SELENIUM_SERVER = 'http://selenium:4444/wd/hub'
option_set = options.Options()
option_set.add_argument('headless')
option_set.add_argument('disable-notifications')
option_set.add_argument('disable-gpu')
option_set.add_argument('disable-infobars')


class CrawlService:
    name = "crawl_service"

    templates_rpc = RpcProxy('templates_service')
    driver = webdriver.Remote(SELENIUM_SERVER, DesiredCapabilities.CHROME, options=option_set)

    FORBIDDEN_LINKS = [ '/' ]
    PATH_ID_DIGEST_SIZE = 4

    @rpc
    def discover(self, root_url):
        html_content = self._get_content(root_url)
        html_tree = html.fromstring(html_content)
        tree = html_tree.getroottree()
        paths = self.discover_paths(html_tree)
        url_results = self.assemble_paths(html_tree, paths, root_url)
        page_id = CrawlService.generate_path_id(root_url)
        return {
            'status': 'done',
            'url': root_url,
            'page_id': page_id,
            'results': url_results
        }

    @rpc
    def crawl_urls(self, urls):
        """Crawl multiple urls into data."""
        # Get the right template for the template service.
        template = self.templates_rpc.create_from_urls(urls)
        # Crawl the page to acquire the data.
        results = []
        for url in urls:
            html_content = self._get_content(url)
            crawl_content = self._crawl_content(
                page_content=html_content,
                template=template,
            )
            crawl_content['url'] = url
            results.append(crawl_content)
        return {
            'status': 'done',
            'results': results
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

    def assemble_paths(self, tree, paths, root_url):
        """Assemble paths results to a structured format."""
        results = dict()
        for path in paths:
            if tree.xpath(path):
                tag = tree.xpath(path)[ 0 ].tag
                path_id = CrawlService.generate_path_id(path)
                tag_key = '%s_%s' % (tag, path_id)
                # Find <a> element.
                link_xpath = '%s//a' % path
                elem_results = []
                # Gather the <a> element values.
                for elem in tree.xpath(link_xpath):
                    href = elem.get('href')
                    if elem.text and href and href not in self.FORBIDDEN_LINKS:
                        href = self._get_clean_url(href, root_url)
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
        paths = CrawlService._find_repeat(tree, '/')
        return sorted(list(set(paths)))

    def _get_clean_url(self, href, root_url):
        url_parse = urlparse( root_url )
        domain = url_parse.netloc or url_parse.path
        scheme = url_parse.scheme or 'http'
        full_domain = '%s://%s' % ( scheme, domain )
        href = href.lstrip('/')
        if domain not in href:
            href = '%s/%s' % (full_domain, href)
        href_parse = urlparse( href )
        if not href_parse.scheme:
            href = '%s://%s' % (scheme, href)
        return href

    def _get_content(self, url):
        self.driver.get(url)
        body_element = self.driver.find_element_by_xpath('/html')
        return body_element.get_attribute('innerHTML')

    @staticmethod
    def _find_repeat(root, xpath):
        """Identify repeating elements in this HTML root."""
        children_elems = list(filter(lambda x: isinstance(x,html.HtmlElement) , root.getchildren()))
        children_elems = sorted(children_elems, key=lambda elem: '%s.%s' % (elem.tag, elem.classes._get_class_value()))
        xpath_results = []
        # Iterate over children already sorted by tags
        for first, second in zip(children_elems, children_elems[1:]):
            if first.tag == second.tag and first.classes == second.classes:
                new_xpath = CrawlService._get_xpath(first, xpath)
                xpath_results.append(new_xpath)
            first_xpath = '%s/%s' % (xpath, str(first.tag))
            xpath_results += CrawlService._find_repeat(first, first_xpath)
        # Search for the last element in the root children elements.
        if children_elems:
            last_elem = children_elems[ -1 ]
            last_xpath = '%s/%s' % (xpath, str(last_elem.tag))
            xpath_results += CrawlService._find_repeat(last_elem, last_xpath)
        return xpath_results

    @staticmethod
    def _get_xpath(elem, root_xpath):
        """Create a sensible xpath."""
        if elem.classes._get_class_value():
            return '//%s[@class="%s"]' % (elem.tag, elem.classes._get_class_value())
        else:
            return '%s/%s' % (root_xpath, str(elem.tag))

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
