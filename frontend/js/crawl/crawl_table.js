import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';

import { loadData } from './actions';

const FIRST_PAGE = 1;
const DOMAIN_REGEX = /http[s]?:\/\/[\w\.]+[\:\d]+\//

const mapStateToProps =
  ({ data, count, page, sizePerPage }) =>
  ({ data, count, page, sizePerPage });

const CrawlTable = ({ data, count, page, sizePerPage, dispatch, }) => {
  const handlePageChange = (newPage) => {
    if ( newPage > 0 && newPage != page ) {
      dispatch(loadData(newPage, sizePerPage));
    }
  }

  const handleSizePerPageChange = (newSizePerPage) => {
    dispatch(loadData(FIRST_PAGE, newSizePerPage));
  }

  const options = {
    onPageChange: handlePageChange,
    onSizePerPageList: handleSizePerPageChange,
    page: page,
    sizePerPage: sizePerPage
  };

  return <BootstrapTable
      data={data}
      remote={true}
      pagination={true}
      fetchInfo={{dataTotalSize: count}}
      options={ options }
      bordered={ false }
      hover={ true }>
    <TableHeaderColumn isKey dataField='id' hidden={true}>ID</TableHeaderColumn>
    <TableHeaderColumn dataField='title'>Title</TableHeaderColumn>
  </BootstrapTable>
};

export default connect( mapStateToProps )( CrawlTable );
