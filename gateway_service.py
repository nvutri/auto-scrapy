import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
    name = 'gateway_service'

    templates_rpc = RpcProxy('templates_service')
    crawl_rpc = RpcProxy('crawl_service')

    @http('POST', '/discover')
    def discover(self, request):
        data = json.loads(request.get_data(as_text=True))
        result = self.crawl_rpc.discover(data.get('url'))
        return json.dumps(result)

    @http('POST', '/crawl')
    def crawl(self, request):
        data = json.loads(request.get_data(as_text=True))
        airport_id = self.templates_rpc.create(data['url'])
        return airport_id
