import {
  setData, SET_DATA,
} from './actions'

describe('actions', () => {
  it('should create an action to set crawl', () => {
    const data = [ { 'a': 'b' } ];
    const expectedAction = {
      type: SET_DATA,
      data
    };
    expect(setData(data)).toEqual(expectedAction);
  });
})
