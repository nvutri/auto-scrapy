const SET_URL = 'SET_URL';
const SET_CRAWL_DATA = 'SET_CRAWL_DATA';
const SET_CRAWL_URLS = 'SET_CRAWL_URLS';
const SET_DISCOVER_DATA = 'SET_DISCOVER_DATA';
const SET_IS_CRAWLING = 'SET_IS_CRAWLING';
const SET_REQUEST_MODE = 'SET_REQUEST_MODE';

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

const setIsCrawling = (value) => ({
  type: SET_IS_CRAWLING,
  value
})

const setRequestMode = (value) => ({
  type: SET_REQUEST_MODE,
  value
})

const loadData = ( page, sizePerPage ) => {
  const caseId = document.getElementById('case-id').value;
  return dispatch => {
    var fetchUrl = `/crawl/?page=${ page }&page_size=${ sizePerPage }`;
    return fetch(fetchUrl)
      .then(response => response.json())
      .then(json => dispatch(setData(json, page, sizePerPage)))
  }
}

const crawlUrls = ( urls, browser=false ) => {
  return dispatch => {
    fetch(`/crawl`, {
      method: 'post',
      body: JSON.stringify({
        urls: urls,
        browser: browser
      })
    })
    .then(response => response.json())
    .then(function(response) {
      dispatch(setIsCrawling(false));
      dispatch(setCrawlData(response.results));
    });
  }
}

const discoverUrl = ( url, browser=false ) => {
  return dispatch => {
    fetch(`/discover`, {
      method: 'post',
      body: JSON.stringify({
        url: url,
        browser: browser
      })
    })
    .then(response => response.json())
    .then(function(response) {
      dispatch(setIsCrawling(false));
      dispatch(setDiscoverData(response.results));
    })
    .catch( () => {
      dispatch(setIsCrawling(false));
    });
  }
}

export {
  loadData,
  setIsCrawling, SET_IS_CRAWLING,
  crawlUrls, setCrawlData, SET_CRAWL_DATA, SET_CRAWL_URLS,
  discoverUrl, setDiscoverData,  SET_DISCOVER_DATA,
  setRequestMode, SET_REQUEST_MODE,
  setUrl, SET_URL,
}
