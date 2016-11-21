import React from 'react';
import CompactCard from './card.jsx';
import MultiCardResult from './MultiCardResult.jsx';


function buildQueryString(query, start) {
  var queryString = 'q=' + encodeURIComponent(query);
  if (start !== 0) {
    queryString += '&start=' + encodeURIComponent(start);
  }

  return queryString;
}

function debounce(fn, interval) {
  var timeout;

  return function () {
    clearTimeout(timeout);
    timeout = setTimeout(fn.apply.bind(fn, this, arguments), interval);
  }
}

export default class SearchResults extends React.Component {
  constructor(props) {
    super(props);

    this.state = { 
      results:[],   // array of objects holding card data
      count:0,      // count of *all* cards matching the query
      start:0,      // index of first returned card; think: "{start} to {start+results.length} of {count}".
      waiting:false // are we currently waiting results to come in?
    };

    this.refreshResults = debounce(this.refreshResults.bind(this), 200);
  }

  refreshResults(props) {
    let query = props.query || '';
    let start = props.start || 0;

    // If the query is empty, we know what the results will be without asking.
    if (query === '') {
      this.setState({ count:0, results:[], start:0 });
      return;
    }

    // If not, we need to ask the server
    var me = this;
    fetch('/query?' + buildQueryString(query, start))
    .then(function(response) {
      return response.json();
    }).then(function(response) {
      me.setState({ results: response.cards, count: response.count, start: response.start, waiting: false });
    });
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ waiting: true });
    this.refreshResults(nextProps);
  }

  componentDidMount() {
    this.setState({ waiting: true });
    this.refreshResults(this.props);
  }

  render() {
    if (this.state.count > 1)
    {
      return <MultiCardResult
        cards={this.state.results}
        count={this.state.count}
        start={this.state.start}
        changeStart={this.props.changeStart}
      />;
    }
    else if (this.state.results.length === 1)
    {
      return <SingleCardResult card={this.state.results[0]} />;
    }
    else if (this.state.results.length === 0 && this.props.query !== '' && !this.state.waiting)
    {
      return <EmptyResult />
    }
    else
    {
      // No query was entered (so obviously no cards were returned)
      return <div className="col-sm-10 col-sm-offset-1"></div>;
    }
  }
}


class SingleCardResult extends React.Component {
  render() {
    // TODO: include more details when displaying a single card

    return (
      <div className="list-group col-sm-10 col-sm-offset-1">
        <CompactCard {...this.props.card} />
      </div>
    );
  }
}

class EmptyResult extends React.Component {
  render() {
      // TODO: make this look nicer
      return <div className="col-sm-10 col-sm-offset-1">No cards returned!</div>;
  }
}
