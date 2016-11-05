import database
import os

try:
	os.remove('test.db')
except:
	pass

database.init_db()
