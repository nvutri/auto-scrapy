import _ from 'lodash';
import React, { Component } from 'react';
import { connect } from 'react-redux';

import PropTypes from 'prop-types';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import ShowMore from 'react-show-more';

const ELEM_ORDER = ['title', 'h1', 'h2', 'p', 'span']
class CrawlDetailTable extends Component {

  constructor(props) {
    super(props);
  }

  valueFormatter(cell, row) {
    return Array.isArray(cell) ? <ShowMore
      lines={ 3 }
      more='more'
      less='less'
      anchorClass=''>
      {cell.map( (item, index) => <span key={`${ row.id }: ${ index }`}>{ item }<br/></span>)}
    </ShowMore> :
    cell
  }

  compareElement( x, y ) {
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

  render() {
    var dataKeys = Object.keys(this.props.data);
    dataKeys = dataKeys.sort( this.compareElement );
    const self = this;
    const data = dataKeys.map( (key) => {
      const values = Array.isArray(self.props.data[key]) ?
        self.props.data[key].map( (entry) => entry.text ? entry.text : entry ) :
        self.props.data[key]
      return {
        id: key,
        value: values
      }
    })
    return <BootstrapTable data={ data } pagination options={ { paginationPosition: 'top' } }>
        <TableHeaderColumn isKey dataField='id' width='10%'>Element</TableHeaderColumn>
        <TableHeaderColumn dataField='value' width='90%' dataFormat={ this.valueFormatter }>Value</TableHeaderColumn>
      </BootstrapTable>
  }
}

export default connect( )( CrawlDetailTable );
