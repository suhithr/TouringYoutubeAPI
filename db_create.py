from app import db
from models import test

db.create_all()
#db.session.add(test("theTerm", "theResponse"))
db.session.commit()