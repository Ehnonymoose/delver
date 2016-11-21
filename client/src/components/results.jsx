import React from 'react';
import CompactCard from './card.jsx';


function buildQueryString(query, start) {
  var queryString = 'q=' + encodeURIComponent(query);
  if (start !== 0) {
    queryString += '&start=' + encodeURIComponent(start);
  }

  return queryString;
}

export default class SearchResults extends React.Component {
  constructor(props) {
    super(props);

    this.state = { 
      results:[],   // array of objects holding card data
      count:0,      // count of *all* cards matching the query
      start:0       // index of first returned card; think: "{start} to {start+results.length} of {count}".
    };

    this.refreshResults = this.refreshResults.bind(this);
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
      me.setState({ results: response.cards, count: response.count, start: response.start });
    });
  }

  componentWillReceiveProps(nextProps) {
    this.refreshResults(nextProps);
  }

  componentDidMount() {
    this.refreshResults(this.props);
  }

  render() {
    // TODO: change ">=" to ">" once detailed single-card view is supported
    if (this.state.results.length >= 1)
    {
      return (
        <div>
          <CustomCardList cards={this.state.results} />
        </div>
      );
    }
    else if (this.state.results.length === 1)
    {
      // TODO: more-detailed view for single-card results
      return (
        <div className="col-sm-10 col-sm-offset-1">
          Unfortunately, we don't yet support single-card display :(
        </div>
      );
    }
    else if (this.state.results.length === 0 && this.props.query !== '')
    {
      // TODO: make this look nicer
      return <div className="col-sm-10 col-sm-offset-1">No cards returned!</div>;
    }
    else
    {
      // No query was entered (so obviously no cards were returned)
      return <div className="col-sm-10 col-sm-offset-1"></div>;
    }
  }
}


class CustomCardList extends React.Component {
  render() {
    let cardList = this.props.cards.map( function(card, idx) {
      return (
        <CompactCard {...card} key={idx} />
      );
    });

    return (
      <div className="list-group col-sm-10 col-sm-offset-1">
        {cardList}
      </div>
    );
  }
}
