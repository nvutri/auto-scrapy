import {
  setUrl, SET_URL,
} from './actions'

describe('actions', () => {
  it('should create an action to set crawl', () => {
    const data = [ { 'a': 'b' } ];
    const expectedAction = {
      type: SET_URL,
      data
    };
    expect(setData(data)).toEqual(expectedAction);
  });
})
