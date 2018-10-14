from nameko.rpc import rpc


class TemplatesService:
    name = "templates_service"

    @rpc
    def create(self, page_url):
        # TODO (tri): run a template creation process for the given page url
        pass

    @rpc
    def create_from_diff(self, url1, url2):
        # TODO (tri): run a template creation from HTML diffing.
        pass
