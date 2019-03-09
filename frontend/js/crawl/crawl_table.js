import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import ShowMore from 'react-show-more';

import { loadData } from './actions';

const FIRST_PAGE = 1;
const DOMAIN_REGEX = /http[s]?:\/\/[\w\.]+[\:\d]+\//

const mapStateToProps = ({ crawl_data }) => ({ crawl_data });

const CrawlTable = ({ crawl_data, dispatch, }) => {
  const valueFormatter = (cell, row) => {
    return <ShowMore
      lines={ 3 }
      more='more'
      less='less'
      anchorClass=''>
      {cell.map( (item) => <span>{ item }<br/><br/></span>)}
    </ShowMore>
  }
  const tdStyle = { whiteSpace: 'normal' };

  return <BootstrapTable data={crawl_data}>
    <TableHeaderColumn isKey dataField='id' hidden={true}>ID</TableHeaderColumn>
    <TableHeaderColumn dataField='name'>Name</TableHeaderColumn>
    <TableHeaderColumn dataField='value' tdStyle={ tdStyle } dataFormat={ valueFormatter }>Value</TableHeaderColumn>
  </BootstrapTable>
};

export default connect( mapStateToProps )( CrawlTable );
