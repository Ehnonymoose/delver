
import database
import models

from sqlalchemy import func

######### Individial Condition Generators #########

def createTextConditionForField(field):
	def createTextCondition(operator, term):
		if operator == ':':
			return field.ilike('%' + term + '%')
		elif operator == '!':
			return (func.lower(field) == func.lower(term))

	return createTextCondition


def createNumericalConditionForField(field, operator, term):
	try:
		rhs = int(term)
	except ValueError:
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
	return (func.lower(models.Set.code) == func.lower(term))


#TODO: these
def createColorCondition(operator, term):
	pass

def createManaCondition(operator, term):
	pass


######### List of supported tags #########

QUERY_TAGS = {
	't': ([':', '!'], createTextConditionForField(models.Card.types)),
	'o': ([':', '!'], createTextConditionForField(models.Card.rules)),
	#'c': ([':', '!'], createColorCondition),
	#'ci': ([':', '!'], createColorIdentityCondition),
	#'mana': ([':'], createManaCondition),
	#'mc': ([':'], createManaCondition),
	'cmc': ([':', '=', '>', '<', '<=', '>=', '!='], createCMCCondition),
	'pow': ([':', '=', '>', '<', '<=', '>=', '!='], createPowerCondition),
	'tou': ([':', '=', '>', '<', '<=', '>=', '!='], createToughnessCondition),
	'name': ([':', '!'], createTextConditionForField(models.Card.name)),

	# The following ones require information about a specific printing
	'ft': ([':', '!'], createTextConditionForField(models.CardPrinting.flavor)),
	'set': ([':'], createSetCondition),
	'e': ([':'], createSetCondition)
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

