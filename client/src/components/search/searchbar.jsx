import React from 'react';

export default class SearchBar extends React.Component {
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