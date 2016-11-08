
import database
import models
import mana

from sqlalchemy import func, and_, or_, not_

######### Individial Condition Generators #########

def createTextConditionForField(field):
	def createTextCondition(operator, term):
		if operator == ':':
			return field.contains(term)
		elif operator == '!':
			return (func.lower(field) == term.lower())

	return createTextCondition


def createNumericalConditionForField(field, operator, term):
	try:
		rhs = int(term)
	except ValueError:
		term = term.lower()
		if term == 'pow':
			rhs = models.Card.powerNum
		elif term == 'tou':
			rhs = models.Card.toughnessNum
		elif term == 'cmc':
			rhs = models.Card.cmc
		else:
			rhs = 0

	if operator in ":=":
		clause = (field == rhs)
	elif operator == ">":
		clause = (field > rhs)
	elif operator == "<":
		clause = (field < rhs)
	elif operator == "<=":
		clause = (field <= rhs)
	elif operator == ">=":
		clause = (field >= rhs)
	elif operator == "!=":
		clause = (field != rhs)
	else:
		raise "Unknown operator '%s'".format(operator)

	return clause

def createCMCCondition(operator, term):
	return createNumericalConditionForField(models.Card.cmc, operator, term)

def createPowerCondition(operator, term):
	# For exact matches, use string comparison
	term = term.lower()
	if operator in ":=":
		if term == 'tou':
			rhs = models.Card.toughness
		elif term == 'cmc':
			rhs = models.Card.cmc
		else:
			rhs = term

		return (models.Card.power == rhs)

	else:
		return createNumericalConditionForField(models.Card.powerNum, operator, term)

def createToughnessCondition(operator, term):
	term = term.lower()
	if operator in ":=":
		if term == 'pow':
			rhs = models.Card.power
		elif term == 'cmc':
			rhs = models.Card.cmc
		else:
			rhs = term

		return (models.Card.toughness == rhs)

	else:
		return createNumericalConditionForField(models.Card.toughnessNum, operator, term)


def createSetCondition(operator, term):
	return (func.lower(models.Set.code) == term.lower())


def createExclusiveColorCondition(field, term, multicolor):
	allColors = set('wubrg')
	usedColors = set(term)
	unusedColors = allColors - usedColors

	usedClauses = [ field.contains(c) for c in usedColors ]
	unusedClauses = [ not_(field.contains(c)) for c in unusedColors ]

	# If the 'm' flag was passed, require that every color be present.
	# Otherwise, require only that at least one color is present.
	if multicolor:
		return and_(*usedClauses, *unusedClauses)
	else:
		return and_(or_(*usedClauses), *unusedClauses)


def createInclusiveColorCondition(field, term, multicolor):
	# Require that at least one of these colors is present
	colorClauses = [ field.contains(c) for c in term ]
	clause = or_(*colorClauses)

	if multicolor:
		# Also require that more than one color is present
		return and_(clause, func.char_length(field) > 1)
	else:
		return clause


def createColorConditionForField(field):
	def createColorCondition(operator, term):
		term = term.lower()

		multicolor = False
		if 'm' in term:
			# Require multicolored
			multicolor = True
			term = term.replace('m', '')

		if operator == '!':
			return createExclusiveColorCondition(field, term, multicolor)
		else:
			return createInclusiveColorCondition(field, term, multicolor)



	return createColorCondition


def createRarityCondition(operator, term):
	return func.lower(models.CardPrinting.rarity).startswith(term.lower())

def createManaCondition(operator, term):
	normalMana = mana.normalize(term)
	return (models.Card.manaCost == normalMana)
	
def createFormatCondition(operator, term):
	if 'standard'.startswith(term):
		return (models.Card.standardLegal == True)
	if 'modern'.startswith(term):
		return (models.Card.modernLegal == True)
	if 'legacy'.startswith(term):
		return (models.Card.legacyLegal == True)
	if 'vintage'.startswith(term):
		return (models.Card.vintageLegal == True)
	if 'commander'.startswith(term):
		return (models.Card.commanderLegal == True)

	return True



######### List of supported tags #########

QUERY_TAGS = {
	't': ([':', '!'], createTextConditionForField(models.Card.types)),
	'o': ([':', '!'], createTextConditionForField(models.Card.rules)),
	'c': ([':', '!'], createColorConditionForField(models.Card.colors)),
	'ci': ([':', '!'], createColorConditionForField(models.Card.colorIdentity)),
	'mana': ([':'], createManaCondition),
	'mc': ([':'], createManaCondition),
	'cmc': ([':', '=', '>', '<', '<=', '>=', '!='], createCMCCondition),
	'pow': ([':', '=', '>', '<', '<=', '>=', '!='], createPowerCondition),
	'tou': ([':', '=', '>', '<', '<=', '>=', '!='], createToughnessCondition),
	'name': ([':', '!'], createTextConditionForField(models.Card.name)),
	'f': ([':'], createFormatCondition),

	# The following ones require information about a specific printing
	'ft': ([':', '!'], createTextConditionForField(models.CardPrinting.flavor)),
	'set': ([':'], createSetCondition),
	'e': ([':'], createSetCondition),
	'r': ([':'], createRarityCondition),
	'a': ([':'], createTextConditionForField(models.CardPrinting.artist))
}


######### Tying it all together #########

def parse(q):
	q = q.lstrip()

	tokens = []
	while len(q) > 0:
		for tag in QUERY_TAGS:
			(operators, generator) = QUERY_TAGS[tag]
			if q.startswith(tag):
				if len(q) > len(tag) + 2:
					maybeOp = q[len(tag):len(tag)+2]
					if maybeOp in operators:
						(token, q) = getFirstToken(q[len(tag)+2:])
						tokens.append( (tag, maybeOp, token) )
						break

				if len(q) > len(tag) + 1:
					maybeOp = q[len(tag)]
					if maybeOp in operators:
						(token, q) = getFirstToken(q[len(tag)+1:])
						tokens.append( (tag, maybeOp, token) )
						break
		else:
			# The rarely-seen for-else loop!
			# If we get here, no tag/operator matched. Assume it's a name query.
			if q[0] == '!':
				# Exact query
				token, q = getFirstToken(q[1:])
				tokens.append( ('name', '!', token) )
			else:
				token, q = getFirstToken(q)
				tokens.append( ('name', ':', token) )

		q.lstrip()

	return tokens



def generateClauses(tokens):
	clauses = []

	for (tag, operator, term) in tokens:
		generator = QUERY_TAGS[tag][1]
		clauses.append( generator(operator, term) )

	return clauses




######### Utility functions #########

# Input: a string starting with "
# Returns: tuple containing a quoted string, and the rest of the input
# Example: handleQuotedString( '"foo bar" baz') => ('foo bar', ' baz')
def getFirstToken(s):
	if len(s) == 0:
		return ('', '')

	if s[0] == '"':
		endQuote = s.find('"', 1)
		if endQuote == -1:
			return (s[1:], '')
		else:
			return (s[1:endQuote], s[endQuote+1:])
	else:
		endSpace = s.find(' ')
		if endSpace == -1:
			return (s, '')
		else:
			return (s[:endSpace], s[endSpace+1:])

