# A table of all known mana symbols and their canonical form.
# This ensures that all mana symbols in the database are in a 
# specific known form for easier searching.
CANONICAL_SYMBOLS = {
	# basic color symbols
	'w':'w', 'u':'u', 'b':'b', 'r':'r', 'g':'g', 'c':'c',

	# numbers
	'0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7',
	'8':'8', '9':'9', '10':'10', '11':'11', '12':'12', '13':'13', '14':'14',
	'15':'15', '16':'16', '20':'20', '100':'100', '1000000':'1000000',
	'inf':'infinity', 'infinity': 'infinity',

	# allied hybrid
	'wu':'wu', 'uw':'wu', 'ub':'ub', 'bu':'ub', 'br':'br', 'rb':'br',
	'rg':'rg', 'gr':'rg', 'gw':'gw', 'wg':'gw',

	# enemy hybrid
	'wb':'wb', 'bw':'wb', 'ur':'ur', 'ru':'ur', 'bg':'bg', 'gb':'bg',
	'rw':'rw', 'wr':'rw', 'gu':'gu', 'ug':'gu',

	# 2brid
	'2w':'2w', '2u':'2u', '2b':'2b', '2r':'2r', '2g':'2g',

	# phyrexian
	'pw':'pw', 'pu':'pu', 'pb':'pb', 'pr':'pr', 'pg':'pg',

	# snow
	's': 's',

	# X, Y, and Z
	'x':'x', 'y':'y', 'z':'z',

	# tap/untap
	't':'t', 'tap':'t', 'q':'q', 'untap':'q'
}


# Table for easily converting mana symbols to their converted mana cost.
MANACOST_TO_CMC = {
	'w':1, 'u':1, 'b':1, 'r':1, 'g':1, 'c':1,

	'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7,	'8':8, '9':9,
	'10':10, '11':11, '12':12, '13':13, '14':14, '15':15, '16':16, '20':20,
	'100':100, '1000000':1000000, 'infinity':999999999,

	'wu':1, 'ub':1, 'br':1, 'rg':1, 'gw':1,
	'wb':1, 'ur':1, 'bg':1, 'rw':1, 'gu':1,

	'2w':2, '2u':2, '2b':2, '2r':2, '2g':2,

	'pw':1, 'pu':1, 'pb':1, 'pr':1, 'pg':1,

	's':1,

	'x':0, 'y':0, 'z':0,
}


# List of characters to ignore when parsing mana costs
IGNORE_CHARS = str.maketrans('', '', ''.join(c for c in map(chr, range(256)) if not c.isalnum() and c != ' '))


def tokenizeManaString(mana):
	""" Takes in a string of mana symbols and tokenizes it.
		Tokens are strings enclosed in {}s; the braces are
		optional for one-character tokens.

		Ignores all non-alphanumeric-or-space characters.

		Example:
			tokenizeManaString("{uw}b{2r}t")
				-> ["uw", "b", "2r", "t"]
	"""

	tokens = []
	token_start = 0

	while token_start < len(mana):
		if mana[token_start] == '{':
			rbrace = mana.find('}', token_start)

			if rbrace == -1:
				token = '{'
				token_start += 1
			else:
				token = mana[token_start+1 : rbrace]
				token_start = rbrace + 1
		else:
			token = mana[token_start]
			token_start += 1

		# clean up the token a bit and save it
		token = token.lower().translate(IGNORE_CHARS)

		# Do we want to check if this is a known token?
		tokens.append( token )

	return tokens


def computeCMC(mana):
	""" Given a mana cost, computes the corresponding CMC.

		If the cost contains an unknown symbol, assumes that
		that symbol has a CMC of 0.
	"""

	tokens = tokenizeManaString(mana)

	total = 0
	for token in tokens:
		if token in MANACOST_TO_CMC:
			total += MANACOST_TO_CMC[token]

	return total



"""
NORMALIZING MANA COSTS

I am a little obsessive about details like putting mana symbols
in the correct order.  Since many people aren't, the following set of 
functions helps get them just right. It also helps to have a standard.

By 'normalized', we mean that tokens come in the following order:
	1. X, Y, Z
	2. Numeric
	3. snow
	4. obligate colorless
	5. 2-brid, in standard order
	6. allied hybrid, in standard order by 'upper' color
	7. enemy hybrid, in standard order by 'upper' color
	8. phyrexian, in standard order
	9. normal colored symbols, in standard order.

As Wizards has inconsiderately not printed any card with more than three
of these (Marisi's Twinclaws), most of this is speculative.

As for 'standard order', this refers to the usual ordering of n WUBRG symbols:
	Mono-colored: trivial
	Two colors: shortest clockwise distance along the WUBRG circle
	Three colors:
		Shards: WUBRG-first order (WUB, UBR, BRG, RGW, GWU)
		Wedges: skip-2 order (WBG, URW, BGU, RWB, GUR)
	Four colors: start after missing color (UBRG, BRWG, etc.)
	Five colors: trivial
"""

def getOrderedTokens(tokens, order):
	""" Selects all tokens from `tokens` that are in `order` and orders them
		according to the order given by `order`.

		Hooray for illuminating docstrings.

		example: 
			getOrderedTokens(["r", "g", "r", "br"], ["w", "u", "b", "r", "g"])
				-> ["r", "r", "g"]
	"""
	result = []
	for token in order:
		result.extend([token] * tokens.count(token))

	return result


def getThreeColorOrder(tokens, unique, wubrg):
	""" tokens: list of all tokens 
		unique: list of unique tokens in `tokens` from `wubrg`
		wubrg: list of tokens filling the roles of WUBRG.  This
				exists so the same function can deal with normal
				mana symbols, phyrexian symbols, etc.
	"""
	# Shards have three consecutive symbols. Find them!
	for i in range(5):
		if  wubrg[i] in unique and wubrg[ (i+1) % 5] in unique and wubrg[ (i+2) % 5] in unique:
		 	
			colors = [ wubrg[i], wubrg[ (i+1)%5 ], wubrg[ (i+2)%5] ]
			return getOrderedTokens(tokens, colors)

	# OK, it's a wedge.  Wedges now have the canonical symbol order that goes
	# two steps at a time (so WBG rather than BGW or GWB or anything else).
	# Find that initial two-step.
	for i in range(5):
		if  wubrg[i] in unique and wubrg[ (i+2) % 5] in unique and wubrg[ (i+4) % 5] in unique:

			# Found it! Now we know what the token order should be.
			colors = [ wubrg[i], wubrg[ (i+2)%5 ], wubrg[ (i+4)%5] ]
			return getOrderedTokens(tokens, colors)

	# We should never get here
	raise ValueError("Three-color cost that's neither a shard nor a wedge?!")


def getWUBRGTokens(tokens, wubrg):
	""" Pull out all tokens from the `wubrg` array and return a list of
		those tokens in canonical form.

		`wubrg` lets the same function handle normal, phyrexian, etc. mana.
	"""
	wubrg_tokens = [ token for token in tokens if token in wubrg ]
	unique_tokens = list(set(wubrg_tokens))

	if len(unique_tokens) == 0:
		# for zero colors, the answer is easy!
		return []
	elif len(unique_tokens) == 1:
		# if there is only one color, return all symbols of that color
		return wubrg_tokens
	elif len(unique_tokens) == 2:
		# two colors. now we get to use those functions from above
		return getOrderedTokens(wubrg_tokens, wubrg)
	elif len(unique_tokens) == 3:
		# three colors -- hey, we've done this already too!
		return getThreeColorOrder(wubrg_tokens, unique_tokens, wubrg)
	elif len(unique_tokens) == 4:
		# four colors. Find the missing one.
		missing = (set(wubrg) - set(unique_tokens)).pop()
		missing_idx = wubrg.index(missing)

		order = [ wubrg[ (i + missing_idx)%5 ] for i in range(5)]
		return getOrderedTokens(wubrg_tokens, order)
	elif len(unique_tokens) == 5:
		return getOrderedTokens(wubrg_tokens, wubrg)
	else:
		# We should *never* get here
		raise ValueError("Why are there six colors in this mana cost.")


def normalize(mana):
	""" The function we've been building to. """
	tokens = tokenizeManaString(mana)
	normalized = []

	# X, Y, Z come first.
	normalized.extend( getOrderedTokens(tokens, ('x', 'y', 'z')) )

	# Now numeric symbols
	normalized.extend( getOrderedTokens(tokens, ('1000000', '100', '20', '16', '15', '14', '13', '12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0')) )

	# snow
	normalized.extend( getOrderedTokens(tokens, ('s')) )

	# obligate colorless
	normalized.extend( getOrderedTokens(tokens, ('c')) )

	# And two-brids
	normalized.extend( getWUBRGTokens(tokens, ('2w', '2u', '2b', '2r', '2g')) )

	# Allied hybrid
	normalized.extend( getWUBRGTokens(tokens, ('wu', 'ub', 'br', 'rg', 'gw')) )

	# Enemy hybrid
	normalized.extend( getWUBRGTokens(tokens, ('wb', 'ur', 'bg', 'rw', 'gu')) )

	# phyrexian
	normalized.extend( getWUBRGTokens(tokens, ('pw', 'pu', 'pb', 'pr', 'pg')) )

	# normal!
	normalized.extend( getWUBRGTokens(tokens, ('w', 'u', 'b', 'r', 'g')) )

	# We have sorted all the tokens. Now wrap them in braces and return.
	normal = ''.join( '{' + token + '}' for token in normalized )

	#print(mana, " => ", normal)
	return normal


test = 'zwbux{pw}{pu}{pg}{pr}sssywcwbx{2/u}{2u}{ur}{rg}{gu}3'

