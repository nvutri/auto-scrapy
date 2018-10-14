from nameko.rpc import rpc


class CrawlService:
    name = "crawl_service"

    @rpc
    def discover(self, url):
        # TODO (tri): return group of sub pages.
        pass

    @rpc
    def crawl(self, page_id, template_id):
        # TODO (tri): crawl a given page_id.
        pass

    @rpc
    def get(self, page_id):
        # TODO (tri): return data from a crawled page.
        pass
