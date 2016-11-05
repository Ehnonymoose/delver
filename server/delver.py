from flask import Flask, request, jsonify, send_from_directory, make_response
from functools import wraps, update_wrapper
from datetime import datetime
from sqlalchemy import and_, or_
from sqlalchemy.sql import select

app = Flask(__name__)

from database import db_session
import query
import models

import json

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

from models import Card, CardPrinting, Set


def serializeCard(card, printing, cardSet):	
	data = {
		'name': card.name,
		'layout': card.layout,
		'related': [x.name for x in card.related],
		'mana': card.manaCost,
		'cmc': card.cmc,
		'types': card.types,
		'rules': card.rules
	};

	if card.power is not None:
		data['power'] = card.power

	if card.toughness is not None:
		data['toughness'] = card.toughness

	if card.loyalty is not None:
		data['loyalty'] = card.loyalty

	if printing.flavor is not None:
		data['flavor'] = printing.flavor

	if printing.rarity is not None:
		data['rarity'] = printing.rarity

	print(data)

	return data


@app.route("/query")
def handleQuery():
	tokens = query.parse(request.args.get('q', ''))
	print(tokens)
	
	clauses = query.generateClauses(tokens)
	statement = and_(*clauses)

	sql = db_session.query(models.Card, models.CardPrinting, models.Set)\
		.join(models.CardPrinting).join(models.Set)\
		.filter(statement)\
		.group_by(models.Card.id).order_by(models.Card.name)\
		.distinct().limit(10)

	results = sql.all()
	
	return json.dumps( [serializeCard(*result) for result in results] )




def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)




@app.route('/', defaults={'path':'index.html'})
@app.route('/<path:path>')
@nocache
def main(path):
	return send_from_directory('public', path)

if __name__ == "__main__":
    app.run()
