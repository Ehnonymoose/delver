import React from 'react';

export default class CompactCard extends React.Component {
  render() {
    return (
      <div className="list-group-item">
        <h4 className="list-group-item-heading">{this.props.name} {this.props.mana}</h4>
        <p class="list-group-item-text">
          {this.props.rules}
        </p>
      </div>
    );
  }
}