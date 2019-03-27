import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import ShowMore from 'react-show-more';
import CrawlDetailTable from './CrawlDetailTable';

const mapStateToProps = ({ crawl_data }) => ({ crawl_data });

const CrawlTable = ({ crawl_data, dispatch, }) => {
  const urlFormatter = (cell, row) => <a href={ cell } target="_blank">{ cell }</a>;
  const tdStyle = { whiteSpace: 'normal' };
  if (crawl_data.length > 0) {
    const tableKeys = crawl_data[ 0 ] ? Object.keys(crawl_data[ 0 ]).filter( (key) => key[ 0 ] !== 'a' ) : [];
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
