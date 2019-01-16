import React from 'react';
import ReactDOM from 'react-dom';
import thunkMiddleware from 'redux-thunk';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';

import { loadData } from './actions';
import { reducer, initialState } from './reducers'
import CrawlTable from './crawl_table';

const store = createStore(
  reducer,
  initialState,
  applyMiddleware(thunkMiddleware),
);

const CaseCrawl = ( ) => {
  store.dispatch(loadData(initialState.page, initialState.sizePerPage));
  ReactDOM.render(
    <Provider store={ store }>
      <CrawlTable/>
    </Provider>,
    document.getElementById('crawl-table')
  );
};


export default CaseCrawl;
