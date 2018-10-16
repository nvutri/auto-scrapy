import json
import pytest

from gateway_service import GatewayService
from crawl_service.crawl_service import CrawlService
from templates_service.templates_service import TemplatesService


@pytest.fixture
def web_session(container_factory, web_config, web_session):
    web_config[ 'AMQP_URI' ] = 'pyamqp://guest:guest@localhost'
    gateway_container = container_factory(GatewayService, web_config)
    gateway_container.start()
    crawl_container = container_factory(CrawlService, web_config)
    crawl_container.start()
    templates_container = container_factory(TemplatesService, web_config)
    templates_container.start()
    return web_session


def test_discover_api(web_session):
    rv = web_session.post('/discover', json.dumps({ 'url': 'http://vietnamnet.vn' }))
    result = rv.json()
    assert result['status'] == 'done'
    assert result['url'] == 'http://vietnamnet.vn'
    assert result['page_id'] == 'f9d3e245'
    assert 'ul_9cf75058' in result[ 'results' ]
    assert 'ul_fa5af060' in result[ 'results' ]


def test_crawl_api(web_session):
    url1 = 'http://vietnamnet.vn/vn/thoi-su/may-bay-roi-o-tam-dao-10-gio-bang-rung-tim-kiem-hai-cot-2-phi-cong-480584.html'
    url2 = 'http://vietnamnet.vn/vn/thoi-su/bao-ke-cho-long-bien-dinh-chi-pho-ban-quan-ly-dung-2-doi-boc-xep-480622.html'
    rv = web_session.post('/crawl', json.dumps({ 'urls': [ url1, url2 ] }))
    result = rv.json()
    assert result['status'] == 'done'
    assert len( result[ 'results' ] ) > 0
    assert 'title_4906f6d2' in result[ 'results' ][ 0 ][ 'data' ]


if __name__ == "__main__":
    import sys
    pytest.main(sys.argv)
