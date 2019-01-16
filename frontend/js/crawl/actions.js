const SET_DATA = 'SET_DATA';

const setData = (data, page, sizePerPage) => ({
  type: SET_DATA,
  data, page, sizePerPage
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

export {
  loadData,
  setData, SET_DATA,
}
