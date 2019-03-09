import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { crawlUrl, setUrl, discoverUrl } from './actions';
import CrawlTable from './crawl_table';
import DiscoverTable from './discover_table';

import { Jumbotron, Well, Button, Row, Col, FormControl } from 'react-bootstrap';

const mapStateToProps =({ url, crawl_data }) => ({ url, crawl_data });

const App = ({ url, crawl_data, dispatch, }) => {
  return (
    <Jumbotron style={{height: '100%'}}>
      <Row>
        <Col md={3}/>
        <Col md={6}>
          <FormControl
            type="text"
            value={ url }
            placeholder="Enter Directory URL"
            onChange={ (e) => { dispatch(setUrl(e.target.value)) } }
          />
        </Col>
        <Col md={2}>
          <Button bsStyle="primary" onClick={ (e) => { dispatch(discoverUrl(url)) } }>Discover</Button>
        </Col>
      </Row>
      <br/>
      <Row>
        <Col md={8}>
          <DiscoverTable/>
        </Col>
        <Col md={4}>
          <Well>
            <CrawlTable/>
          </Well>
        </Col>
      </Row>
    </Jumbotron>
  )
}

export default connect( mapStateToProps )( App );
