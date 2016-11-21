import React from 'react';

let symbolTranslations = {
  /* Basic symbols   */ 'w':'w', 'u':'u', 'b':'b', 'r':'r', 'g':'g', 'c':'c',
  /* Numeric symbols */ '0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5',
                        '6':'6', '7':'7', '8':'8', '9':'9', '10':'10', '11':'11',
                        '12':'12', '13':'13', '14':'14', '15':'15', '16':'16',
                        '20':'20', '100':'100', '1000000':'1000000', 'inf':'inf',
  /* Allied hybrid */   'wu':'wu', 'ub':'ub', 'br':'br', 'rg':'rg', 'gw':'gw',
                        'uw':'wu', 'bu':'ub', 'rb':'br', 'gr':'rg', 'wg':'gw', 
  /* Enemy hybrid */    'wb':'wb', 'ur':'ur', 'bg':'bg', 'rw':'rw', 'gu':'gu',
                        'bw':'wb', 'ru':'ur', 'gb':'bg', 'wr':'rw', 'ug':'gu',
  /* 2brid */           '2w':'2w', '2u':'2u', '2b':'2b', '2r':'2r', '2g':'2g',
  /* Phyrexian */       'pw':'pw', 'pu':'pu', 'pb':'pb', 'pr':'pr', 'pg':'pg', 'p':'p',
  /* X, Y, Z */         'x':'x', 'y':'y', 'z':'z',
  /* Tap, untap */      't':'t', 'tap':'t', 'q':'q', 'untap':'q',
  /* Colored snow */    'sw':'sw', 'su':'su', 'sb':'sb', 'sr':'sr', 'sg':'sg', 's':'s',
  /* Energy */          'e':'e'
};

// TODO: host better-looking mana symbols ourselves
let symbolBaseUrl = "http://forum.nogoblinsallowed.com/images/smilies/mana/";

function convertSymbols(text) {
  let symbolRegex = /\{([a-z0-9\/]+)\}/gi;
  let alphanumRegex = /[^a-zA-Z0-9]/;

  var newNodes = [];
  let textParts = text.split(symbolRegex);

  for (var i = 0; i < textParts.length; ++i)
  {
    // Consecutive mana symbols lead into this case.
    if (textParts[i].length === 0) {
      continue;
    }

    let symbol = textParts[i].replace(alphanumRegex, '').toLowerCase();
    if (symbolTranslations.hasOwnProperty(symbol)) {
      let symbolUrl = symbolBaseUrl + symbolTranslations[symbol] + '.png';
      newNodes.push( <img src={ symbolUrl } key={"sym" + i} /> );
    } else {
      newNodes.push( <span key={"text" + i}>{ textParts[i] }</span> );
    }
  } 

  return newNodes;
}


function prepareRulesText(text) {
  if (text === null || text === undefined) {
    return [];
  }

  let parenRegex = /(\(.*?\))/;

  var htmlParts = [];
  let lines = text.split('\n');
  for (var i = 0; i < lines.length; ++i) {
    var lineChildren = [];
    var lineText = lines[i];

    // Has an ability word?
    let dashIdx = lineText.indexOf('\u2014');
    if (dashIdx > -1) {
      lineChildren.push(<i key="ability"> {lineText.substring(0, dashIdx)} </i>);
      lineChildren.push(<span key="dash">{'\u2014'}</span>);
      lineText = lineText.substring(dashIdx + 1);
    }

    // Has a parenthesized section?
    let parenParts = lineText.split(parenRegex);
    for (var j = 0; j < parenParts.length; ++j) {
      let part = parenParts[j];
      if (part[0] === '(') {
        lineChildren.push( <i key={'l' + i + 'p' + j}> { convertSymbols(part) } </i> );
      } else if (part.length > 0) {
        lineChildren = lineChildren.concat( convertSymbols(part) );
      }
    }

    htmlParts.push( <p key={'line' + i}> {lineChildren} </p> );
  }

  return htmlParts;
}

function prepareFlavorText(text) {
  return (<i>{text}</i>);
}

export default class CompactCard extends React.Component {
  render() {
    var stats = "";
    if (this.props.power !== undefined && this.props.toughness !== undefined) {
      stats = " (" + this.props.power + "/" + this.props.toughness + ")";
    } else if (this.props.loyalty !== undefined) {
      stats = " (" + this.props.loyalty + ")";
    }

    var mana = "";
    if (this.props.layout === 'token') {
      mana = <span style={{ fontSize: "0.8em", marginLeft: "10px" }}> (token)</span>;
    } else {
      mana = (
          <span className="compact-mana">
            { convertSymbols(this.props.mana) }
          </span>
      );
    }

    var rarity = " (" + this.props.rarity[0].toUpperCase() + ")";

    if (this.props.flavor !== "") {
      var flavor = (
        <div className="compact-flavor">
          { prepareFlavorText(this.props.flavor) }
        </div>
      );
    }

    return (
      <a className="list-group-item">
        <h4 className="list-group-item-heading">
          {this.props.name}
          { mana }
        </h4>
        <div className="list-group-item-text">
          <p>
            { this.props.types }
            { stats }
            { rarity }
          </p>
          <div className="compact-rules">
            { prepareRulesText(this.props.rules) }
          </div>
          { flavor }
        </div>
      </a>
    );
  }
}