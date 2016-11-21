import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRoute, browserHistory } from 'react-router';

import YMtG from './components/layout';
import MainSearch from './components/search/main';

ReactDOM.render((
  <Router history={browserHistory}>
    <Route path="/" component={YMtG}>
      <IndexRoute component={MainSearch} />
    </Route>
  </Router>
  ), document.getElementById('app')
);
