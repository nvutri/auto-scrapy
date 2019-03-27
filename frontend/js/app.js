import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { crawlUrl, setUrl, discoverUrl, setDiscoverData, setIsCrawling } from './actions';
import CrawlTable from './components/CrawlTable';
import DiscoverTable from './components/DiscoverTable';

import { Jumbotron, Well, Button, Row, Col, FormControl } from 'react-bootstrap';

const mapStateToProps =({ url, crawl_data, is_crawling }) => ({ url, crawl_data, is_crawling });

const App = ({ url, crawl_data, is_crawling, dispatch, }) => {
  return (
    <Jumbotron style={{height: '100%'}}>
      <Col md={1}/>
      <Col md={10}>
      <Row>
        <Col md={3}/>
        <Col md={6}>
          <FormControl
            type="text"
            value={ url }
            placeholder="Enter Directory URL"
            disabled={ is_crawling }
            onChange={ (e) => { dispatch(setUrl(e.target.value)) } }
          />
        </Col>
        <Col md={2}>
          <Button
            bsStyle={ is_crawling ? 'primary' : 'info' }
            disabled={ is_crawling }
            onClick={ (e) => {
              dispatch(setIsCrawling(true));
              dispatch(setDiscoverData({}));
              dispatch(discoverUrl(url));
            }
          }>{ is_crawling ? 'Discovering...' : 'Discover' }</Button>
          </Col>
        </Row>
        <br/>
        <Row>
          <Well>
            <CrawlTable/>
          </Well>
        </Row>
        <br/>
        <Row>
          <DiscoverTable/>
        </Row>
      </Col>
    </Jumbotron>
  )
}

export default connect( mapStateToProps )( App );
