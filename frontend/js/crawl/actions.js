const SET_URL = 'SET_URL';
const SET_CRAWL_DATA = 'SET_CRAWL_DATA';

const setUrl = (url) => ({
  type: SET_URL,
  url
});

const setCrawlData = (data) => ({
  type: SET_CRAWL_DATA,
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

export {
  loadData,
  crawlUrl,
  setCrawlData, SET_CRAWL_DATA,
  setUrl, SET_URL,
}
