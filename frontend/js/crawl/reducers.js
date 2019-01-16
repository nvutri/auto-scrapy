import { SET_DATA } from './actions';

const initialState = {
  data: [ ],
  page: 1,
  sizePerPage: 10
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_DATA:
      return Object.assign({}, state, {
        data: action.data.results,
        page: action.page,
        sizePerPage: action.sizePerPage,
        count: action.data.count
      });
    default: {
      return state;
    }
  }
};

export { initialState, reducer }
