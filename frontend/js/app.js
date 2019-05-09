import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { crawlUrl, setUrl, discoverUrl, setDiscoverData, setIsCrawling, setRequestMode } from './actions';
import DiscoverTable from './components/DiscoverTable';

import { Jumbotron, Well, Button, Row, Col, FormControl, Checkbox } from 'react-bootstrap';

const mapStateToProps = ({ url, crawl_data, is_crawling, request_mode }) => ({ url, crawl_data, is_crawling, request_mode });

const App = ({ url, crawl_data, is_crawling, request_mode, dispatch, }) => {
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
          <Checkbox checked={request_mode.browser} onClick={ (e) => { dispatch(setRequestMode({ browser: !request_mode.browser })) } }>
            Use Headless Browser
          </Checkbox>
        </Col>
        <Col md={2}>
          <Button
            bsStyle={ is_crawling ? 'primary' : 'info' }
            disabled={ is_crawling }
            onClick={ (e) => {
              dispatch(setIsCrawling(true));
              dispatch(setDiscoverData({}));
              dispatch(discoverUrl(url, request_mode.browser));
            }
          }>{ is_crawling ? 'Discovering...' : 'Discover' }</Button>
          </Col>
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
