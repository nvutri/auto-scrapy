import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import ShowMore from 'react-show-more';
import CrawlDetailTable from './CrawlDetailTable';

const mapStateToProps = ({ crawl_data }) => ({ crawl_data });
const ELEM_ORDER = ['title', 'h1', 'h2', 'p', 'span']

const compareElement = ( x, y ) => {
  const xKey = x.split('_')[ 0 ];
  const yKey = y.split('_')[ 0 ];
  if (ELEM_ORDER.indexOf(xKey) == -1) {
    return 1
  }
  if (ELEM_ORDER.indexOf(yKey) == -1) {
    return -1
  }
  return ELEM_ORDER.indexOf(xKey) < ELEM_ORDER.indexOf(yKey) ? -1 : 1;
}

const CrawlTable = ({ crawl_data, dispatch, }) => {
  const urlFormatter = (cell, row) => <a href={ cell } target="_blank">{ cell }</a>;
  const tdStyle = { whiteSpace: 'normal' };
  if (crawl_data.length > 0) {
    var tableKeys = crawl_data[ 0 ] ? Object.keys(crawl_data[ 0 ]).filter( (key) => key[0] !== 'a' ) : [];
    tableKeys = tableKeys.sort(compareElement);
    tableKeys = tableKeys.slice(0, 5);
    if (tableKeys.indexOf('url') < 0) {
      tableKeys.push('url');
    }
    const expandComponent = (data) => <CrawlDetailTable data={ data }/>
    if (tableKeys.length > 0) {
      return <BootstrapTable
          data={ crawl_data }
          expandableRow={ () => true }
          expandComponent={ expandComponent }>
          {
            tableKeys.map( (key) => key === 'url' ?
              <TableHeaderColumn isKey key={ key } dataField={ key } dataFormat={ urlFormatter }>{ key }</TableHeaderColumn> :
              <TableHeaderColumn key={ key } dataField={ key }>{ key }</TableHeaderColumn> )
          }
        </BootstrapTable>
    }
  }
  return <div/>
};

export default connect( mapStateToProps )( CrawlTable );
