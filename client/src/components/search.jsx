import React from 'react';
import SearchResults from './results.jsx';

function debounce(fn, interval) {
  var timeout;

  return function () {
    clearTimeout(timeout);
    timeout = setTimeout(fn.apply.bind(fn, this, arguments), interval);
  }
}

class SearchBar extends React.Component {
  constructor(props) {
    super(props);

    this.updateQuery = this.updateQuery.bind(this);
    this.submitQuery = this.submitQuery.bind(this);
  }

  updateQuery(evt) {
    this.submitQuery(evt.target.value);
  }

  submitQuery(query) {
    if (query === '') {
      this.context.router.push({});
    } else {
      this.context.router.push({ query: { q: query } });
    }
  }

  render() {
    var currentQuery = "";
    if (this.props.query) {
      currentQuery = this.props.query.q || "";
    }

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
                value={currentQuery}
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

export default class MainSearch extends React.Component {
  render() {
    return (
      <div>
        <SearchBar query={this.props.location.query} />
        <SearchResults query={this.props.location.query} />
      </div>
    );
  }
}

SearchBar.contextTypes = {
  router: React.PropTypes.object.isRequired,
};

MainSearch.contextTypes = {
  router: React.PropTypes.object.isRequired,
};
