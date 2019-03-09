const SET_URL = 'SET_URL';
const SET_CRAWL_DATA = 'SET_CRAWL_DATA';
const SET_DISCOVER_DATA = 'SET_DISCOVER_DATA';

const setUrl = (url) => ({
  type: SET_URL,
  url
});

const setCrawlData = (data) => ({
  type: SET_CRAWL_DATA,
  data
});

const setDiscoverData = (data) => ({
  type: SET_DISCOVER_DATA,
  data
});

const loadData = ( page, sizePerPage ) => {
  const caseId = document.getElementById('case-id').value;
  return dispatch => {
    var fetchUrl = `/crawl/?page=${ page }&page_size=${ sizePerPage }`;
    return fetch(fetchUrl)
      .then(response => response.json())
      .then(json => dispatch(setData(json, page, sizePerPage)))
  }
}

const crawlUrl = ( url ) => {
  return dispatch => {
    fetch(`/crawl`, {
      method: 'post',
      body: JSON.stringify({'url': url})
    })
    .then(response => response.json())
    .then(function(response) {
      dispatch(setCrawlData(response.results));
    });
  }
}

const discoverUrl = ( url ) => {
  return dispatch => {
    fetch(`/discover`, {
      method: 'post',
      body: JSON.stringify({'url': url})
    })
    .then(response => response.json())
    .then(function(response) {
      dispatch(setDiscoverData(response.results));
    });
  }
}

export {
  loadData,
  crawlUrl, setCrawlData, SET_CRAWL_DATA,
  discoverUrl, setDiscoverData,  SET_DISCOVER_DATA,
  setUrl, SET_URL,
}
