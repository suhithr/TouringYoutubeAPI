from app import db

class test(db.Model):
	__tablename__ = 'searches2'

	id = db.Column(db.Integer, primary_key=True)
	term = db.Column(db.String, nullable=False)
	response = db.Column(db.Text, nullable=False)
	time_of_search = db.Column(db.DateTime, nullable=False)

	def __init__(self, term, response, time_now):
		self.term = term
		self.response = response
		self.time_of_search = time_now

	def __repr__(self):
		return 'Here'

class test_selected(db.Model):
	__tablename__ = 'selected1'

	id = db.Column(db.Integer, primary_key=True)
	term_id = db.Column(db.String, nullable=False)
	response = db.Column(db.Text, nullable=False)
	time_of_request = db.Column(db.DateTime, nullable=False)

	def __init__(self, term_id, response, time_of_request):
		self.term_id = term_id
		self.response = response
		self.time_of_request = time_of_request

	def __repr__(self):
		return '<Requested is is "%s"' % (self.term_id)