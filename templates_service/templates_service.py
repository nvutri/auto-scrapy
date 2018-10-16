import requests

from lxml import html
from nameko.rpc import rpc


class TemplatesService:
    name = "templates_service"

    @rpc
    def create(self, page_url):
        # TODO (tri): run a template creation process for the given page url
        pass

    @rpc
    def create_from_diff(self, url1, url2):
        tree1 = html.fromstring(requests.get(url1).content)
        tree2 = html.fromstring(requests.get(url2).content)
        xpaths = self.diff_html(tree1, tree2)
        return xpaths

    def diff_html(self, elem1, elem2, paths=[]):
        """Run a diff on 2 element trees."""
        result = []
        # Check to see if this is the diff xpath.
        if elem1.text and elem1.text != elem2.text and elem1.tag != 'script':
            paths.append(elem1.tag)
            result.append('/'.join(paths))
            return result
        # Search for similar sub elements to take a diff over 2 trees.
        for idx1, child1 in enumerate(elem1.getchildren()):
            # Skip searching for comment elements.
            if isinstance(child1, html.HtmlComment):
                continue
            # Search for matching element for recursive comparison.
            child2 = self.search_child2(elem2[ idx1:], child1)
            if child2 is None:
                # Relax search condition to tag only.
                child2 = self.search_child2(elem2[ idx1:], child1, require_attrib=False)
            # Recursive compare if found a matching element.
            if child2 is not None:
                result += self.diff_html(child1, child2, paths + [ elem1.tag ])
        return result

    def search_child2(self, elems, child1, require_attrib=True):
        """Search for a relevant matching tag and attributes."""
        for child2 in elems:
            if child1.tag == child2.tag and child1.attrib == child2.attrib:
                return child2
