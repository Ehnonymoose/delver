from sqlalchemy import Table, Column, Integer, String, Enum, Unicode, UnicodeText, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

# Some kinds of cards have multiple 'forms': DFCs, split, flip, and meld cards.
# This is apparently the correct way to set up a self-referential one-to-many relationship.
class RelatedCards(Base):
	__tablename__ = 'related_cards'
	left_card_id = Column(Integer, ForeignKey('cards.id'), primary_key=True)
	right_card_id = Column(Integer, ForeignKey('cards.id'), primary_key=True)


# All cards have some inherent traits: name, cost, text, etc.
class Card(Base):
	__tablename__ = 'cards'
	id = Column(Integer, primary_key=True)

	# This could be dramatically shorter, if not for "Our Market Research Shows
	#     That Players Like Really Long Card Names So We Made this Card to Have
	#     the Absolute Longest Card Name Ever Elemental". I hate that guy.
	name = Column(Unicode(150))

	# Card layout. Determines how it's rendered, for cards we render ourselves.
	layout = Column( Enum('normal', 'split', 'flip', 'double-faced', 'token', 'meld', 'leveler', 'basic land'))

	# This card's other 'parts'. Only used for DFC, meld, split, and flip cards.
	related = relationship("Card",
		secondary='related_cards',
		primaryjoin=(id == RelatedCards.left_card_id),
		secondaryjoin=(id == RelatedCards.right_card_id),
		backref='_names'
	)

	# All printings of this card
	printings = relationship("CardPrinting")

	# The mana cost, e.g. {5}{W}{W}. Longest currently is 30 (Progenitus).
	manaCost = Column(String(50))
	cmc = Column(Integer)

	# The card's colors, concatenated together: "wub", "c", etc.
	colors = Column(String(5))
	

	# The card's color *identity*, similarly stored.
	colorIdentity = Column(String(5))

	# The card's typeline, as it would appear on a card: "Legendary Creature - Human Wizard"
	types = Column(Unicode(64))

	# Rules text, with symbols 'escaped' as usual ({T}, etc.).
	rules = Column(UnicodeText())

	# Power and toughness, as strings, if applicable.  It's a string so things like * are representable.
	power = Column(String(5))
	toughness = Column(String(5))

	# Power and toughness, as integers, if applicable. This is for easy comparisons (* => 0).
	powerNum = Column(Integer)
	toughnessNum = Column(Integer)

	# Starting loyalty, if applicable
	loyalty = Column(Integer)

	def __init__(self, name, layout, manaCost, cmc, colors, colorIdentity, types):
		self.name = name
		self.layout = layout
		self.manaCost = manaCost
		self.cmc = cmc
		self.colors = colors
		self.colorIdentity = colorIdentity
		self.types = types


# Cards are printed in sets.
class Set(Base):
	__tablename__ = 'sets'
	id = Column(Integer, primary_key=True)

	name = Column(Unicode(50))
	code = Column(Unicode(5))
	symbolUrl = Column(UnicodeText())

	def __init__(self, name, code):
		self.name = name
		self.code = code


# Because the same card can be printed in multiple sets, we separate out per-printing
# information like flavor text, art, etc. into a separate record.
# Functionally, this is an association table where the associations have some data.
class CardPrinting(Base):
	__tablename__ = 'printings'
	id = Column(Integer, primary_key=True)

	# The card
	cardId = Column(Integer, ForeignKey('cards.id'))

	# A set this card is printed in
	setId = Column(Integer, ForeignKey('sets.id'))

	# The flavortext for this printing.
	flavor = Column(UnicodeText())

	# A card can be reprinted at a different rarity.
	rarity = Column( Enum('basic land', 'common', 'uncommon', 'rare', 'mythic rare', 'special') )

	# URL of an image of this printing of this card
	imageUrl = Column(UnicodeText())

	# Artist credit for this art, if applicable
	artist = Column(Unicode(50))

	# URL of this card's watermark image, if applicable
	watermarkUrl = Column(UnicodeText())

	# The Multiverse ID, used to index cards in the official Gatherer (and also get images)
	multiverseId = Column(Integer)

	def __init__(self, cardId, setId, rarity):
		self.cardId = cardId
		self.setId = setId
		self.rarity = rarity


