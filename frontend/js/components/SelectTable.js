import _ from 'lodash';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { crawlUrl } from '../actions';

import PropTypes from 'prop-types';
import { Button, Row, Col, Well } from 'react-bootstrap';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';

const MIN_CRAWL_ITEMS = 2

class SelectTable extends Component {

  constructor(props) {
    super(props);
    this.state = { numSelected: 0 };
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
    console.log(selectedUrls);
    this.props.dispatch(crawlUrl(selectedUrls[0]));
  }

  render() {
    const selectRowProp = {
      mode: 'checkbox',
      clickToSelect: true,
      onSelect: this.handleSelect.bind(this),
      onSelectAll: this.handleSelectAll.bind(this)
    }
    const canCrawl = this.state.numSelected >= MIN_CRAWL_ITEMS;
    return <Well>
      <Row>
        <Col md={2}/>
        <Col md={8}>
          <Button
            onClick={this.handleClick.bind(this)}
            bsStyle={canCrawl ? 'info' : 'default' }
            disabled={!canCrawl}
            block>
            { canCrawl ? 'Get Data!' : `Please select at least ${ MIN_CRAWL_ITEMS } links`}
          </Button>
        </Col>
      </Row>
      <br/>
      <BootstrapTable ref='table' data={ this.props.row.value } selectRow={ selectRowProp }>
        <TableHeaderColumn isKey dataField='href' hidden={true}>ID</TableHeaderColumn>
        <TableHeaderColumn dataField='text' dataFormat={ this.valueFormatter }>Links</TableHeaderColumn>
      </BootstrapTable>
    </Well>
  }
}

export default connect( )( SelectTable );
