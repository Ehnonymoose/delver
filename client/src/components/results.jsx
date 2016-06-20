import React from 'react';
import CompactCard from './card.jsx';

export default class SearchResults extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      results: [{
        name: 'Counterspell',
        mana: 'UU',
        rules: 'Counter target spell.'
      }, {
        name: 'Infinite Obliteration',
        mana: '1BB',
        rules: 'Name a creature card. Search target opponent\'s graveyard, hand, and library for any number of cards with that name and exile them. Then that player shuffles his or her library.'
      }]
    };
  }

  render() {
    let cardList = this.state.results.map( function(card, idx) {
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
