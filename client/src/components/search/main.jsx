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
