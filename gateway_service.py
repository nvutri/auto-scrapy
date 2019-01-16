import json
import logging

from jinja2 import Environment, FileSystemLoader
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from os import path
from werkzeug.wrappers import Response


TEMPLATE_PATH = path.join(path.dirname(__file__), 'templates')
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))


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
        result = self.crawl_rpc.crawl(url=data.get('url'))
        return json.dumps(result)

    @http('GET', '/')
    def index(self, request):
        webpack = json.loads(open('frontend/webpack-stats.json').read())
        if webpack['status'] == 'done':
            context = { 'webpack': webpack['chunks']['main'][0]['publicPath'] }
            return Response(
                jinja_env.get_template('index.html').render(**context),
                mimetype='text/html'
            )
        return Response()
