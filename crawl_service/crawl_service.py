import requests

from lxml import etree
from lxml import html
from nameko.rpc import rpc


class CrawlService:
    name = "crawl_service"

    @rpc
    def discover(self, url):
        html_content = requests.get(url).content
        html_tree = html.fromstring(html_content)
        tree = html_tree.getroottree()
        paths = self.discover_paths(tree)
        return self.assemble_paths(tree, paths)

    @rpc
    def crawl(self, page_id, template_id):
        # TODO (tri): crawl a given page_id.
        pass

    @rpc
    def get(self, page_id):
        # TODO (tri): return data from a crawled page.
        pass

    def assemble_paths(self, tree, paths):
        """Assemble paths results to a structured format."""
        results = dict()
        for path in paths:
            # Find <a> element.
            link_xpath = '%s//a' % path
            elem_results = []
            # Gather the <a> element values.
            for elem in tree.xpath(link_xpath):
                if elem.text and elem.get('href'):
                    elem_results.append({
                        'href': elem.get('href'),
                        'text': elem.text.strip()
                    })
            # Store results to return full values.
            if elem_results:
                tag = tree.xpath(path)[0].tag
                tag_index = len(results[ tag ]) if tag in results else 0
                tag_key = '%s_%s' % (tag, tag_index)
                results[tag_key] = elem_results
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
