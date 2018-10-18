import requests

from lxml import html
from nameko.rpc import rpc
from urllib.parse import urlparse


class TemplatesService:
    name = "templates_service"

    @rpc
    def create(self, url):
        tree = html.fromstring(requests.get(url).content)
        link_urls = list(map(lambda elem: elem.get('href'), tree.xpath('//a')))
        similar_links = self.search_similar_links(root_url=url, urls=link_urls)
        similar_url = similar_links[ 0 ]
        return self.create_from_diff(url, similar_link)

    @rpc
    def create_from_diff(self, url1, url2):
        tree1 = html.fromstring(requests.get(url1).content)
        tree2 = html.fromstring(requests.get(url2).content)
        xpaths = self.diff_html(tree1, tree2)
        return list(set(xpaths))

    def diff_html(self, elem1, elem2, paths=None):
        """Run a diff on 2 element trees."""
        result = []
        if not paths:
            paths = [ elem1.tag ]
        # Check to see if this is the diff xpath.
        if elem1.text and elem1.text != elem2.text and elem1.tag != 'script':
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
        max_score = max(scores, key=lambda x: x[1])
        return list(filter(lambda x: x[1] == max_score[1], scores))

    def score_url_similarity(self, url1, url2):
        """Calculate a score that represent how closely the 2 URLs are matching."""
        parse1 = urlparse(url1)
        parse2 = urlparse(url2)
        if parse1.netloc != parse2.netloc:
            return 0
        num_same = 1
        path1 = parse1.path.split('/')
        path2 = parse2.path.split('/')
        path1 = list(filter(lambda x: x != '', path1))
        path2 = list(filter(lambda x: x != '', path2))
        if path1 and path2:
            for p1, p2 in zip(path1, path2):
                if p1 == p2:
                    num_same += 1
            return num_same / max(len(path1), len(path2))
        return 0
