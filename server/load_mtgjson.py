import models
import database
import mana

import json

def statToNum(s):
	if 'X' in s or '*' in s:
		cleaned = s.replace('X', '0').replace('*', '0')
		return eval(cleaned)
	else:
		# The easy case
		return int(s)


def serializeColors(colors):
	colorMap = {
		'White': 'w',
		'Blue': 'u',
		'Black': 'b',
		'Red': 'r',
		'Green': 'g'
	}

	if colors is None:
		return 'c'

	return ''.join(colorMap[c] for c in colors)

def serializeColorIdentity(ci):
	if ci is None:
		return 'c'

	return ''.join(ci).lower()


def ensureCardExists(cardData):
	result = models.Card.query.filter(models.Card.name == cardData['name']).first()
	if result is not None:
		return result
	else:
		thisCard = generate_card(cardData)
		if thisCard is None:
			return

		try:
			database.db_session.add(thisCard)
		except: 
			pdb.set_trace()

		database.db_session.flush()

		# print("Added card with name '" + cardData['name'] + "' and id " + str(thisCard.id))
		return thisCard


def generate_card(cardData):
	if cardData['layout'] in [ 'plane', 'vanguard', 'phenomenon', 'scheme' ]:
		return

	if 'colors' in cardData:
		colors = serializeColors(cardData['colors'])
	else:
		colors = 'c'

	if 'colorIdentity' in cardData:
		colorId = serializeColorIdentity(cardData['colorIdentity'])
	else:
		colorId = 'c'

	if 'manaCost' in cardData:
		mc = mana.normalize(cardData['manaCost'])
		cmc = cardData['cmc']
	else:
		mc = ''
		cmc = 0

	thisCard = models.Card(
		cardData['name'],
		cardData['layout'],
		mc,
		cmc,
		colors,
		colorId,
		cardData['type']
	)

	if 'names' in cardData:
		related[ cardData['name'] ] = cardData['names']
		related[ cardData['name'] ].remove( cardData['name'] )

	if 'power' in cardData:
		thisCard.power = cardData['power']
		thisCard.toughness = cardData['toughness']
		thisCard.powerNum = statToNum( cardData['power'] )
		thisCard.toughnessNum = statToNum( cardData['toughness'] )

	if 'loyalty' in cardData:
		thisCard.loyalty = cardData['loyalty']

	if 'text' in cardData:
		thisCard.rules = cardData['text']

	return thisCard



with open('AllSets-x.json', 'r') as f:
	blob = json.load(f)

printings = []

# We need to come back and fill these in later.
related = {}

for setCode in blob:
	setData = blob[setCode]

	# Fuck these sets
	if setData['name'] in [ 'Unhinged', 'Unglued' ]:
		continue

	print('Loading set: ' + setData['name'])
	thisSet = models.Set(setData['name'], setData['code'])
	database.db_session.add(thisSet)
	database.db_session.flush()


	for cardData in setData['cards']:
		thisCard = ensureCardExists(cardData)
		if thisCard is None:
			continue

		thisPrinting = models.CardPrinting(
			thisCard.id,
			thisSet.id,
			cardData['rarity'].lower()
		)
		
		if 'flavor' in cardData:
			thisPrinting.flavor = cardData['flavor']

		if 'multiverseid' in cardData:
			thisPrinting.multiverseId = cardData['multiverseid']

		printings.append(thisPrinting)


print('Added all cards. Linking cards to sets...')
database.db_session.bulk_save_objects(printings)
		
print('Adding relationships between cards (DFCs, split cards, etc.)...')
# Fill in 'related' data
for key in related:
	# print('Setting up relationship: ' + key + " => " + str(related[key]))
	thisCard = models.Card.query.filter(models.Card.name == key).first()

	otherCards = []
	for other in related[key]:
		otherCards.append( models.Card.query.filter(models.Card.name == other).first() )

	thisCard.related = otherCards
	database.db_session.commit()

print('Success!')