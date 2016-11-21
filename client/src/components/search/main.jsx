import React from 'react';

import SearchBar from './searchbar.jsx';
import SearchResults from './results.jsx';

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
    if (this.commitQuery === undefined) {
      this.commitQuery = debounce(this.context.router.push, 200);
    }

    // TODO: de-dupe, don't do more work than we have to, etc.

    newString = newString || '';
    if (newString === '') {
      var newArgs = {};
    } else {
      var newArgs = { query: { q: newString} };
    }

    this.commitQuery(newArgs);
    this.setState({ query: newString, start: 0 });
  }

  updateQueryStart(newStart) {
    if (newStart === this.state.start) {
      return;
    }

    this.context.router.push({ query: { q: this.state.query, start: newStart }});
    this.setState({ start:newStart });
  }

  componentWillReceiveProps(nextProps) {
    let newQuery = nextProps.location.query.q || '';
    let newStart = nextProps.location.query.start || 0;

    var updates = {};
    var haveUpdate = false;

    if (newQuery.q !== this.state.query) {
      var cleanup = function(s) {
        return s.toLowerCase().trim();
      }

      if (cleanup(newQuery) !== cleanup(this.state.query)) {
        updates.query = newQuery;
        haveUpdate = true;
      }
    }

    if (newStart !== this.state.start) {
      updates.start = newStart;
      haveUpdate = true;
    }

    if (haveUpdate) {
      this.setState(updates);
    }
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
          changeStart={this.updateQueryStart}  
        />
      </div>
    );
  }
}

MainSearch.contextTypes = {
  router: React.PropTypes.object.isRequired,
};
