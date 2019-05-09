import requests
import logging
import selenium

from lxml import html
from nameko.rpc import rpc
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


class TemplatesService:
    name = "templates_service"

    MAX_COMPARE = 5
    EXCLUDING_TAGS = ['script', 'style']
    driver = webdriver.Remote(SELENIUM_SERVER, DesiredCapabilities.CHROME, options=option_set)

    @rpc
    def create_from_urls(self, urls, main_url=None, browser=False):
        """Create template from URLs comparison."""
        if main_url is None:
            main_url = urls[ 0 ]
        # Compare potential templates to find the one with maximum diff values.
        diff_templates = [ ]
        root_page_content = self._get_content(main_url, browser=browser)
        for similar_url in urls[:self.MAX_COMPARE]:
            diff_templates.append(self.create_from_diff(main_url, similar_url, page_content_1=root_page_content))
        # Search for the maximum diff xpaths.
        diff_templates_length = [ len(diff) for diff in diff_templates ]
        logging.info('MAX_DIFF: %s' % diff_templates_length)
        max_diff = max(diff_templates_length)
        # Select the maximum diff xpaths.
        for diff_template in diff_templates:
            if len(diff_template) == max_diff:
                return diff_template
        return [ ]

    @rpc
    def create(self, url):
        """Create template from a single URL."""
        link_urls = self.find_link_urls(root_url=url)
        link_urls = list(set(link_urls))
        similar_links = self.search_similar_links(root_url=url, urls=link_urls)
        similar_urls = list(map(lambda x: x[ 0 ], similar_links))
        similar_urls = list(set(similar_urls))
        similar_urls = sorted(similar_urls, reverse=True, key=lambda x: len(x))
        return self.create_from_urls(similar_urls, main_url=url)

    @rpc
    def create_from_diff(self, url1, url2, page_content_1=None):
        tree1 = html.fromstring( page_content_1 or self._get_content(url1) )
        tree2 = html.fromstring( self._get_content(url2))
        xpaths = self.diff_html(tree1, tree2)
        unique_xpaths = list(set(xpaths))
        return unique_xpaths

    def diff_html(self, elem1, elem2, paths=[]):
        """Run a diff on 2 element trees."""
        result = []
        # Check to see if this is the diff xpath.
        if paths and elem1.text and elem1.text != elem2.text and elem1.tag not in self.EXCLUDING_TAGS:
            result.append('/'.join(paths))
        # Search for similar sub elements to take a diff over 2 trees.
        for idx1, child1 in enumerate(elem1.getchildren()):
            # Skip searching for comment elements.
            if isinstance(child1, html.HtmlComment):
                continue
            # Search for matching element for recursive comparison.
            child2 = self.search_child2(elem2[ idx1:], child1)
            if child2 is None:
                # Relax search condition to tag only.
                child2 = self.search_child2(elem2[ idx1: ], child1, require_attrib=False)
            # Recursive compare if found a matching element.
            if child2 is not None:
                result += self.diff_html(child1, child2, paths + [ child1.tag ])
        return result

    def search_child2(self, elems, child1, require_attrib=True):
        """Search for a relevant matching tag and attributes."""
        for child2 in elems:
            if child1.tag == child2.tag:
                if ( not require_attrib ) or ( require_attrib and child1.attrib == child2.attrib ):
                    return child2

    def search_similar_links(self, root_url, urls):
        """Search URL that are similar to root_urls."""
        scores = [ (url, self.score_url_similarity( root_url, url )) for url in urls ]
        logging.info(scores)
        max_score = max(scores, key=lambda x: x[1])
        logging.info(max_score)
        return list(filter(lambda x: x[1] == max_score[1], scores))

    def score_url_similarity(self, url1, url2):
        """Calculate a score that represent how closely the 2 URLs are matching."""
        parse1 = urlparse(url1)
        parse2 = urlparse(url2)
        if parse1.netloc != parse2.netloc:
            return 0
        num_same = 0
        path1 = parse1.path.split('/')
        path2 = parse2.path.split('/')
        path1 = list(filter(lambda x: x != '', path1))
        path2 = list(filter(lambda x: x != '', path2))
        if path1 and path2:
            for p1, p2 in zip(path1, path2):
                if p1 == p2:
                    num_same += 1
            return num_same / len(path1)
        return 0

    def find_link_urls(self, root_url):
        page_content = requests.get(root_url).content
        return self._find_link_urls(root_url=root_url, page_content=page_content)

    def _get_content(self, url, browser=False):
        if browser:
            return self._get_content_by_browser(url)
        else:
            response = requests.get(url)
            return response.content

    def _get_content_by_browser(self, url):
        try:
            self.driver.get(url)
        except selenium.common.exceptions.WebDriverException as e:
            logging.error(e)
            self.driver = webdriver.Remote(SELENIUM_SERVER, DesiredCapabilities.CHROME, options=option_set)
            self.driver.get(url)
        body_element = self.driver.find_element_by_xpath('/html')
        return body_element.get_attribute('innerHTML')

    def _find_link_urls(self, root_url, page_content):
        tree = html.fromstring(page_content)
        url_parse = urlparse( root_url )
        url_domain = '%s://%s' % (url_parse.scheme, url_parse.netloc)
        link_urls = []
        for elem in tree.xpath('//a'):
            href = elem.get('href')
            # Skip if this does not have a link.
            if not href:
                continue
            elem_url_parse = urlparse(href)
            # Skip the URL if it does not belong to the same domain.
            if elem_url_parse.netloc and elem_url_parse.netloc != url_parse.netloc:
                continue
            # Update the href, only include the path.
            elem_path = elem_url_parse.path
            if elem_path:
                if elem_path[ 0 ] != '/':
                    elem_path = '/%s' % elem_path
                href = '%s%s' % (url_domain, elem_path)
                if href.strip('/') != root_url.strip('/'):
                    link_urls.append(href)
        return link_urls
