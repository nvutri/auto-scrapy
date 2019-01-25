import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { crawlUrl, setUrl } from './actions';
import CrawlTable from './crawl_table';
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
            placeholder="Enter URL"
            onChange={ (e) => { dispatch(setUrl(e.target.value)) } }
          />
        </Col>
        <Col md={2}>
          <Button bsStyle="primary" onClick={ (e) => { dispatch(crawlUrl(url)) } }>Go!</Button>
        </Col>
      </Row>
      <Row>
        <Col md={1}/>
        <Col md={10}>
          <Well>
            <CrawlTable/>
          </Well>
        </Col>
      </Row>
    </Jumbotron>
  )
}

export default connect( mapStateToProps )( App );
