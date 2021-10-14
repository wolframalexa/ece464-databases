from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker
from sailors import Sailor, Reservation, Boat

engine = create_engine("mysql+pymysql://alexa:Hello123%21%40%23@localhost:1345/sailors")

Session = sessionmaker(bind = engine)
session = Session()


def q1(session):
	# first query

	expected = [ # bid | bname | count(reserves.bid)
	(103, "Clipper", 8),
	(109, "Driftwood", 5),
	(101, "Interlake", 5),
	(110, "Klapser", 3),
	(105, "Marine", 7),
	(112, "Sooney", 2)]

	result = session.query(Reservation.bid, Boat.bname, func.count(Reservation.bid)).\
		join(Reservation, Boat.bid == Reservation.bid).group_by(Boat.bname).all()
	print(s1)

	for expected, result in zip (expected, result):
		assert expected == result
	session.commit()

def q2():
	# second query:

	expected = [] # empty set

	red_boat_reserves = session.query(Sailor.sid, Sailor.sname, Boat.bid).join(Reserve, Sailor.sid == Reserve.sid).join(Boat, Reserve.bid == Boat.bid).filter(Boat.color == "red").distinct().subquery()
	num_red = session.query(func.count(Boat.bid)).filter(Boat.color == "red").scalar()
	sailors_reserved_all_red = session.query(red_boat_reserves.c.sid, red_boat_reserves.c.sname, func.count(red_boat_reserves.c.sid)).group_by(red_boat_reserves.c.sid).having(func.count(red_boat_reserves.c.sid) == num_red_boats).all()

	assert sailors_reserved_all_red == expected
	session.commit()

def q3():
	# third query: list sailors who have reserved only red boats
	expected = [
	# sid | name
	(23, emilio)
	(24, scruntus)
	(35, figaro)
	(61, ossola)
	(62, shaun)
	]


	sailors_not_red = session.query(Sailor.sid).join(Reserve, Sailor.sid == Reserve.sid).join(Reserve, Boat.bid == Reserve.bid).filter(Boat.color != "red").group_by(Sailor.sid).subquery()

	sailors_reserves = session.query(Sailor.sid).join(Reservation, Sailor.sid == Reservation.sid).distinct().subquery()

	sailors_no_reserves = session.query(Sailor.sid).filter(Sailor.sid.notin_(sailors_reserves)).distinct()
	sailors_only_not_red = union_all(sailors_not_red, sailors_no_reserves).distinct().subquery()
	sailors_only_red = session.query(Sailor.sid, Sailor.sname).filter(Sailor.sid.notin_(sailors_only_not_red)).all()

	for expected, sailors_only_red in zip(expected, sailors_only_red):
		assert expected == sailors_only_red
	session.commit()


def q4():
	# boat with max # reservations
	expected = [
	(101, Interlake, 5)
	]

	bid_count = session.query(func.count(Reserve.bid)).subquery
	max_reserves_boat = session.query(Boat.bid, Boat.bname, func.max(bid_count)).join(Boat, Reserve.bid == Boat.bid).group_by(Reserve.bid)

	for expected, sailors_only_red in zip(expected, sailors_only_red):
		assert expected == sailors_only_red
	session.commit()

def q5():
	# sailors who have never reserved a red boat

	expected = [ # sid | sname
	(29, brutus)
	(32, andy)
	(58, rusty)
	(60, jit)
	(71, zorba)
	(74, horatio)
	(85, art)
	(90, vin)
	(95, bob)
	]


	reserved_red = session.query(Sailor.sid).join(Sailor, Reserves.sid == Sailor.sid).join(Reserve, Boat.sid == Reserve.sid).filter(Boat.color == "red").distinct()
	never_reserved_red = session.query(Sailor.sid, Sailor.sname).filter(Sailor.sid not in reserved_red)

	for expected, never_reserved_red in zip(expected, never_reserved_red):
		assert expected == never_reserved_red
	session.commit()

def q6():
	# find average age of sailors whose rating is 10

	expected = 35;

	age = session.query(func.avg(Sailor.age)).filter(Sailor.rating == 10)
	assert int(age) == expected
	session.commit()

def q7():
	# for each rating find the sailor (name and sid) with the minimum age
	expected = [
	(1, scruntus, 24, 33)
	(3, art, 85, 25)
	(7, dusting, 22, 16)
	(8, lubber, 31, 25)
	(9, horatio, 74, 25)
	(10, rusty, 58, 35)
	]

	min_age_rating = session.query(Sailor.rating, Sailor.sname, Sailor.sid, func.min(Sailor.age)).group_by(Sailor.rating)

	for expected, min_age_rating in zip(expected, min_age_rating):
		assert expected == min_age_rating
	session.commit()

def q8():
	# for each boat find the sailor that reserved it the most often
	expected = [
	(101, 22, 1)
	(101, 22, 1)
	(102, 22, 1)
	(103, 22, 1)
	(104, 22, 1)
	(105, 23, 1)
	(106, 59, 2)
	(107, 88, 1)
	(108, 89, 1)
	(109, 59, 1)
	(110, 62, 2)
	(111, 88, 1)
	(112, 61, 1)
	]

	bid_count = session.query(Reserve.bid, Reserve.sid, func.count(Reserve.bid)).subquery().group_by(Reserve.bid, Reserve.sid).order_by(Reserve.bid)
	most_reserves = session.query(Reserve.bid, Reserve.sid, func.max(bid_count))

	for expected, most_reserves in zip(expected, most_reserves):
		assert expected == most_reserves
	session.commit()


q1(session)
q2()
q3()
q4()
q5()
q6()
q7()
q8()
