import { SET_URL, SET_CRAWL_DATA, SET_DISCOVER_DATA } from './actions';

const initialState = {
  crawl_data: [],
  table: {
    data: [ ],
    page: 1,
    sizePerPage: 10,
  },
  url: ''
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_URL:
      return Object.assign({}, state, {
        url: action.url
      });
    case SET_CRAWL_DATA:
      const crawl_data = []
      Object.keys(action.data).forEach( (key) => {
        const values = action.data[key].map( (entry) => entry.text ? entry.text : entry );
        crawl_data.push({
          id: key,
          name: key,
          value: values
        })
      });
      return Object.assign({}, state, {
        crawl_data: crawl_data
      });
    case SET_DISCOVER_DATA:
      const discover_data = []
      Object.keys(action.data).forEach( (key) => {
        const values = action.data[key].map( (entry) => entry.text ? entry.text : entry );
        discover_data.push({
          id: key,
          title: values,
          value: action.data[key]
        })
      });
      return Object.assign({}, state, {
        discover_data: discover_data
      });
    default: {
      return state;
    }
  }
};

export { initialState, reducer }
