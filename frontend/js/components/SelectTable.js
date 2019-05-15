import _ from 'lodash';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { crawlUrls, setCrawlData, setIsCrawling } from '../actions';
import CrawlTable from './CrawlTable';

import PropTypes from 'prop-types';
import { Button, Row, Col, Modal, Well } from 'react-bootstrap';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';

const MIN_CRAWL_ITEMS = 2
const mapStateToProps = ({ is_crawling, crawl_data, request_mode }) => ({ is_crawling, crawl_data, request_mode });

class SelectTable extends Component {

  constructor(props) {
    super(props);
    this.state = {
      numSelected: 0,
      showModal: false
    };
  }

  valueFormatter(value, cell) {
    return <a href={ cell.href } target="_blank">{ value }</a>
  }

  getSelected() {
    this.refs.table ? this.refs.table.state.selectedRowKeys : []
  }

  handleSelect(row, isSelected) {
    const newNumSelected =  isSelected ? this.state.numSelected + 1 : this.state.numSelected - 1;
    this.setState({ numSelected: newNumSelected })
  }

  handleSelectAll(isSelected, rows) {
    this.setState({ numSelected: isSelected ? rows.length : 0 });
  }

  handleClick() {
    const selectedUrls = this.refs.table.state.selectedRowKeys;
    this.setState({ showModal: true });
    this.props.dispatch(setIsCrawling(true));
    this.props.dispatch(setCrawlData([]));
    this.props.dispatch(crawlUrls(selectedUrls, this.props.request_mode.browser));
  }

  render() {
    const selectRowProp = {
      mode: 'checkbox',
      clickToSelect: true,
      onSelect: this.handleSelect.bind(this),
      onSelectAll: this.handleSelectAll.bind(this)
    }
    const canCrawl = this.state.numSelected >= MIN_CRAWL_ITEMS;
    const buttonTitle = canCrawl ?
      this.props.is_crawling ? 'Crawling...' : 'Get Data!' :
      `Please select at least ${ MIN_CRAWL_ITEMS } links`;
    return <Well>
      <Row>
        <Col md={2}/>
        <Col md={6}>
          <Button
            onClick={this.handleClick.bind(this)}
            bsStyle={canCrawl ? this.props.is_crawling ? 'primary' : 'info' : 'default' }
            disabled={!canCrawl || this.props.is_crawling }
            block>
            { buttonTitle }
          </Button>
        </Col>
        <Col md={2}>
          { this.props.crawl_data.length > 0 ? <Button onClick={ () => this.setState({showModal: true}) }>{`Show ${this.props.crawl_data.length} Results`}</Button> : '' }
        </Col>
      </Row>
      <br/>
      <BootstrapTable ref='table' data={ this.props.row.value } selectRow={ selectRowProp }>
        <TableHeaderColumn isKey dataField='href' hidden={true}>ID</TableHeaderColumn>
        <TableHeaderColumn dataField='text' dataFormat={ this.valueFormatter }>Links</TableHeaderColumn>
      </BootstrapTable>
      <Modal show={this.state.showModal} bsSize="large" onHide={ () => this.setState({showModal: false})}>
        <Modal.Header closeButton>
          <Modal.Title>Crawl Results</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {
            this.props.is_crawling ?
              'Crawling...' :
              <CrawlTable/>
          }
        </Modal.Body>
      </Modal>
    </Well>
  }
}

export default connect( mapStateToProps )( SelectTable );
