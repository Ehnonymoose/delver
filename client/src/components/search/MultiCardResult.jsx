import React from 'react';

import CompactCard from './card.jsx';

let NUM_RESULTS_PER_PAGE = 15;


class PaginationButton extends React.Component {
  render() {
    let btnClasses = "btn btn-default btn-sm";
    if (this.props.onClick === undefined) {
      btnClasses += " disabled";
    }

    return (
      <button type="button" className={btnClasses} onClick={this.props.onClick}>
        <span className={ "glyphicon glyphicon-" + this.props.icon }></span>
      </button>
    );
  }
}


class ResultPagination extends React.Component {
  constructor(props) {
    super(props);

    let changeFn = this.props.changeStart;
    this.buttonHandler = function(newStart, isDisabled) {
      if (isDisabled) return;
      return function() { changeFn(newStart); }
    }
  }

  render() {
    var previousStart = Math.max(0, this.props.first - NUM_RESULTS_PER_PAGE);
    var nextStart = Math.min(this.props.total, this.props.last + 1);
    var lastStart = NUM_RESULTS_PER_PAGE * (Math.ceil(this.props.total / NUM_RESULTS_PER_PAGE) - 1);

    var disableBack = (this.props.first === 0);
    var disableForward = (this.props.last + 1 === this.props.total);    // +1 for 0-based indexing and 1-based counting

    var firstButton    = <PaginationButton icon="fast-backward" onClick={this.buttonHandler(0, disableBack)} />;
    var previousButton = <PaginationButton icon="step-backward" onClick={this.buttonHandler(previousStart, disableBack)} />;
    var nextButton     = <PaginationButton icon="step-forward"  onClick={this.buttonHandler(nextStart, disableForward)} />;
    var lastButton     = <PaginationButton icon="fast-forward"  onClick={this.buttonHandler(lastStart, disableForward)} />;

    return (
      <div className="col-sm-4 col-sm-offset-4" style={{marginTop:'10px', marginBottom:'10px'}}>
        <div className="pull-left">
          { firstButton }
          { previousButton }
        </div>
        <div className="pull-right">
          { nextButton }
          { lastButton }
        </div>
        <div className="center-block btn btn-sm" style={{cursor:'default'}}>
          Showing {this.props.first + 1}-{this.props.last + 1} of {this.props.total}.
        </div>
      </div>
    );
  }
}

export default class MultiCardResult extends React.Component {
  render() {
    let cardList = this.props.cards.map( function(card, idx) {
      return (
        <CompactCard {...card} key={idx} />
      );
    });

    let firstIdx = this.props.start,
        lastIdx  = this.props.start + this.props.cards.length - 1;

    return (
      <div>
        <ResultPagination first={firstIdx} last={lastIdx} total={this.props.count} changeStart={this.props.changeStart} />
        <div className="list-group col-sm-10 col-sm-offset-1">
          {cardList}
        </div>
      </div>
    );
  }
}
