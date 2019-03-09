import moment from 'moment'

import { reducer } from './reducers';
import {
  setUrl, SET_URL,
  setData, SET_DATA,
  setPage, SET_PAGE,
  setSizePerPage, SET_SIZE_PER_PAGE
} from './actions'

describe('data reducer', () => {
  it('should return the initial state', () => {
    expect(reducer(undefined, {})).toEqual({
      data: [],
      page: 1,
      sizePerPage: 10
    });
  })
  it('should return the same as loaded data', () => {
    const rawData = {
      count: 1,
      results: [
        {
          id: 1,
          case: { id: 2 },
          user: { id: 1 }
        }
      ]
    };
    const expectedState = {
      count: 1,
      page: 1,
      sizePerPage: 10,
      data: rawData.results
    }
    expect(
      reducer(
        undefined,
        {
          type: SET_DATA,
          data: rawData,
          page: 1,
          sizePerPage: 10
        }
      )
    ).toEqual(expectedState);
  })
  it('should return the updated page', () => {
    const newPage = 3;
    const expectedState = {
      data: [],
      page: 3,
      sizePerPage: 10,
      count: 1
    }
    expect(
      reducer(
        undefined,
        {
          type: SET_DATA,
          page: 3,
          data: {
            count: 1,
            results: []
          },
          sizePerPage: 10
        }
      )
    ).toEqual(expectedState);
  })
});
