import React from 'react';
import CompactCard from './card.jsx';

export default class SearchResults extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      query: '',
      results: []
    };

    this.refreshResults = this.refreshResults.bind(this);
  }

  
  refreshResults() {
    let newQuery = this.props.query.q;
    if (newQuery === undefined) {
      this.setState({ results: [] });
      return;
    }

    if (newQuery.trim() === this.state.query.trim()) {
      return;
    }

    this.setState({query: newQuery});

    var me = this;
    fetch('/query?q=' + encodeURIComponent(newQuery))
    .then(function(response) {
      return response.json();
    }).then(function(response) {
      me.setState({ results: response });
    });
  }

  componentDidUpdate() {
    this.refreshResults();
  }

  componentDidMount() {
    this.refreshResults();
  }

  render() {
    if (this.state.results.length > 1)
    {
      let cardList = this.state.results.map( function(card, idx) {
        console.dir(card);
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
    else if (this.state.results.length == 1)
    {
      return (
        <div className="col-sm-10 col-sm-offset-1">
          Unfortunately, we don't yet support single-card display :(
        </div>
      );
    }
    else
    {
      return (
        <div className="col-sm-10 col-sm-offset-1">
          No cards found!
        </div>
      );
    }
  }
}
