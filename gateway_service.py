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
        result = self.crawl_rpc.discover(data.get('url'), data.get('browser'))
        return json.dumps(result)

    @http('POST', '/crawl')
    def crawl(self, request):
        data = json.loads(request.get_data(as_text=True))
        result = {}
        if data.get('url'):
            result = self.crawl_rpc.crawl(url=data.get('url'), browser=data.get('browser'))
        elif data.get('urls'):
            result = self.crawl_rpc.crawl_urls(urls=data.get('urls'), browser=data.get('browser'))
        return json.dumps(result)

    @http('GET', '/')
    def index(self, request):
        webpack = json.loads(open('frontend/webpack-stats-prod.json').read())
        if webpack['status'] == 'done':
            context = { 'webpack': webpack['chunks']['main'][0]['path'] }
            return Response(
                jinja_env.get_template('index.html').render(**context),
                mimetype='text/html'
            )
        return Response()
