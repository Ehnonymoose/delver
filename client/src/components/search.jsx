import React from 'react';

function debounce(fn, interval) {
  var timeout;

  return function () {
    clearTimeout(timeout);
    timeout = setTimeout(fn.apply.bind(fn, this, arguments), interval);
  }
}

export default class MainSearch extends React.Component {
  constructor(props) {
    super(props);

    this.updateQuery = this.updateQuery.bind(this);
    this.submitQuery = debounce(this.submitQuery.bind(this), 1000);
  }

  updateQuery(evt) {
    this.submitQuery(evt.target.value);
  }

  submitQuery(query) {
    console.log('submitted query: ' + query);
    if (query === '') {
      this.context.router.push({});
    } else {
      this.context.router.push({ query: { q: query } });
    }
  }

  render() {
    return (
      <div className="voffset">
        <form className="form" onSubmit={this.searchAll}>
          <div className="row">
            <div className="form-group col-sm-8 col-sm-offset-2">
              <label className="sr-only" htmlFor="input-query">Search terms</label>
              <input
                type="search"
                className="form-control input-lg"
                name="q"
                placeholder="Query..."
                autoFocus="true"
                onChange={this.updateQuery}
              />
            </div>
          </div>
        </form>
      </div>
    );
  }
}

MainSearch.contextTypes = {
  router: React.PropTypes.object.isRequired,
};
