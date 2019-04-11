import { SET_URL, SET_IS_CRAWLING, SET_CRAWL_DATA, SET_CRAWL_URLS, SET_DISCOVER_DATA } from './actions';

const initialState = {
  crawl_data: [],
  table: {
    data: [ ],
    page: 1,
    sizePerPage: 10,
  },
  is_crawling: false,
  url: ''
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_URL:
      return Object.assign({}, state, {
        url: action.url
      });
    case SET_IS_CRAWLING:
      return Object.assign({}, state, {
          is_crawling: action.value
        });
    case SET_CRAWL_URLS:
      return Object.assign({}, state, {
        urls: action.urls
      });
    case SET_CRAWL_DATA:
      return Object.assign({}, state, {
        crawl_data: action.data
      });
    case SET_DISCOVER_DATA:
      const discover_data = []
      Object.keys(action.data).forEach( (key) => {
        action.data[key] = action.data[key].filter( entry => entry.text && entry.text.trim().length > 0 )
        const values = action.data[key].map( entry => entry.text.trim() );
        if (values.length > 0) {
          discover_data.push({
            id: key,
            title: values,
            value: action.data[key]
          })
        }
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
