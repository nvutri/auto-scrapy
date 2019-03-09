import React from 'react';
import ReactDOM from 'react-dom';
import thunkMiddleware from 'redux-thunk';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';

import { loadData } from './actions';
import { reducer, initialState } from './reducers'
import App from './app';

const store = createStore(
  reducer,
  initialState,
  applyMiddleware(thunkMiddleware),
);

ReactDOM.render(
  <Provider store={ store }>
    <App/>
  </Provider>,
  document.getElementById('root')
);
