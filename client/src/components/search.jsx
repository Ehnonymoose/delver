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
  }

  updateQuery(evt) {
    this.props.onUpdate(evt.target.value);
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
                value={this.props.query}
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
  constructor(props) {
    super(props);

    if (this.props.location.query) {
      this.state = {
        start: this.props.location.query.start || 0,
        query: this.props.location.query.q || ''
      };
    }
    else {
      this.state = { start:0, query:'' };
    }
    
    this.updateQueryString = this.updateQueryString.bind(this);
    this.updateQueryStart = this.updateQueryStart.bind(this);
  }

  updateQueryString(newString) {
    // TODO: de-dupe, don't do more work than we have to, etc.

    if (newString === '') {
      this.context.router.push({});
    } else {
      this.context.router.push({ query: { q: newString} });
    }

    this.setState({ query: newString, start: 0 });
  }

  updateQueryStart(newStart) {
    // TODO: de-dupe, don't do more work than we have to, etc.

    this.context.router.push({ query: { q: this.state.query, start: newStart }});

    this.setState({ start:newStart });
  }

  render() {
    return (
      <div>
        <SearchBar
          query={this.state.query}
          onUpdate={this.updateQueryString}
        />

        <SearchResults
          query={this.state.query}
          start={this.state.start}
          changeQuery={this.updateQueryString}
          changeStart={this.updateQueryStart}  
        />
      </div>
    );
  }
}

MainSearch.contextTypes = {
  router: React.PropTypes.object.isRequired,
};
