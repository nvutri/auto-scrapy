import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { loadData } from './actions';
import { Jumbotron, Button, Row, Col, FormControl } from 'react-bootstrap';

const App = () => {
  return (
    <Jumbotron style={{height: '100%'}}>
      <Row>
        <Col md={3}/>
        <Col md={6}>
          <FormControl
            type="text"
            value=""
            placeholder="Enter text"
          />
        </Col>
        <Col md={2}>
          <Button bsStyle="primary">Go!</Button>
        </Col>
      </Row>
    </Jumbotron>
  )
}

export default App;
