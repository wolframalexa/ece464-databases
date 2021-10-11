from sqlalchemy import func
from sailors import Sailor, Reserve, Boat

engine = create_engine("mysql://alexa@localhost/sailors", echo=True, future=True)

with Session(engine) as session
	result = session.execute(text("select 'hello world'"))
	print(result.all())



def q1():
	# first query

	expected = [ # bid | bname | count(reserves.bid)
	(103, "Clipper", 8),
	(109, "Driftwood", 5),
	(101, "Interlake", 5),
	(110, "Klapser", 3),
	(105, "Marine", 7),
	(112, "Sooney", 2)
	]
	s1 = session.query(Reserve.bid, Boat.bname, func.count(Reserve.bid)).join(Reserve, Boat.bid == Reserve.bid).group_by(Boat.bname).all()
	print(s1)

	for expected, result in zip (expected, s1):
		assert expected == result
	session.commit()
