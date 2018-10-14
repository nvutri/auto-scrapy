import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
    name = 'gateway'

    templates_rpc = RpcProxy('templates_service')

    @http('POST', '/directory/<string:airport_id>')
    def discover(self, request, airport_id):
        airport = self.airports_rpc.get(airport_id)
        return json.dumps({'airport': airport})

    @http('POST', '/airport')
    def directory(self, request):
        data = json.loads(request.get_data(as_text=True))
        airport_id = self.templates_rpc.create(data['url'])

        return airport_id
