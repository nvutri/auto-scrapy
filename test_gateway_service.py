import json
import pytest

from gateway_service import GatewayService
from crawl_service.crawl_service import CrawlService


@pytest.fixture
def web_session(container_factory, web_config, web_session):
    web_config[ 'AMQP_URI' ] = 'pyamqp://guest:guest@localhost'
    gateway_container = container_factory(GatewayService, web_config)
    gateway_container.start()
    crawl_container = container_factory(CrawlService, web_config)
    crawl_container.start()
    return web_session


def test_discover_api(web_session):
    rv = web_session.post('/discover', json.dumps({ 'url': 'http://vietnamnet.vn' }))
    result = rv.json()
    assert result['status'] == 'done'
    assert result['url'] == 'http://vietnamnet.vn'
    assert result['page_id'] == 'f9d3e245'
    assert 'ul_9cf75058' in result[ 'results' ].keys()
    assert 'ul_fa5af060' in result[ 'results' ].keys()


if __name__ == "__main__":
    import sys
    pytest.main(sys.argv)
