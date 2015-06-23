from app import db

class test(db.Model):
	__tablename__ = 'searches'

	id = db.Column(db.Integer, primary_key=True)
	term = db.Column(db.String, nullable=False)
	response = db.Column(db.Text, nullable=False)

	def __init__(self, term, response):
		self.term = term
		self.response = response

	def __repr__(self):
		return '<Search Term {}'.format(self.term)