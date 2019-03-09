import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import ShowMore from 'react-show-more';

import SelectTable from './SelectTable';

const mapStateToProps = ({ discover_data }) => ({ discover_data });

const DiscoverTable = ({ discover_data, dispatch, }) => {
  const titleFormatter = (cell, row) => {
    return <ShowMore
      lines={ 3 }
      more=''
      less='less'
      anchorClass=''>
      {cell.map( (item, index) => <span key={`${ row.id }: ${ index }`}>{ item }<br/></span>)}
    </ShowMore>
  }

  const expandComponent = (row) => {
    return <SelectTable row={ row }/>
  }

  const tdStyle = { whiteSpace: 'normal' };

  return <BootstrapTable
    striped
    data={ discover_data }
    expandableRow={ () => true }
    expandComponent={ expandComponent }>
    <TableHeaderColumn isKey dataField='id' hidden={true}>ID</TableHeaderColumn>
    <TableHeaderColumn dataField='title' tdStyle={ tdStyle } dataFormat={ titleFormatter }>URL Groups</TableHeaderColumn>
  </BootstrapTable>
};

export default connect( mapStateToProps )( DiscoverTable );
