import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import { Button, Row, Col } from 'react-bootstrap';
import ShowMore from 'react-show-more';

import { loadData } from './actions';

const FIRST_PAGE = 1;
const DOMAIN_REGEX = /http[s]?:\/\/[\w\.]+[\:\d]+\//

const mapStateToProps = ({ discover_data }) => ({ discover_data });


const selectRowProp = {
  mode: 'checkbox',
  clickToSelect: true
};

const valueFormatter = (value, cell) => {
  return <a href={ cell.href } target="_blank">{ value }</a>
}

const expandComponent = (row) => {
  return <BootstrapTable data={ row.value } selectRow={ selectRowProp }>
    <TableHeaderColumn isKey dataField='href' hidden={true}>ID</TableHeaderColumn>
    <TableHeaderColumn dataField='text' dataFormat={ valueFormatter }>Links</TableHeaderColumn>
  </BootstrapTable>
}

const DiscoverTable = ({ discover_data, dispatch, }) => {
  const titleFormatter = (cell, row) => {
    return <ShowMore
      lines={ 3 }
      more=''
      less='less'
      anchorClass=''>
      {cell.map( (item) => <span>{ item }<br/></span>)}
    </ShowMore>
  }


  const tdStyle = { whiteSpace: 'normal' };

  return <div>
    <BootstrapTable
      striped
      data={ discover_data }
      expandableRow={ () => true }
      expandComponent={ expandComponent }>
      <TableHeaderColumn isKey dataField='id' hidden={true}>ID</TableHeaderColumn>
      <TableHeaderColumn dataField='title' tdStyle={ tdStyle } dataFormat={ titleFormatter }>URL Groups</TableHeaderColumn>
    </BootstrapTable>
    <Button bsStyle="info" block>Go!</Button>
  </div>
};

export default connect( mapStateToProps )( DiscoverTable );
