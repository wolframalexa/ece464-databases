from sqlalchemy import func, create_engine, union_all, select
from sqlalchemy.orm import sessionmaker
from sailors import Sailor, Reservation, Boat

engine = create_engine("mysql+pymysql://alexa:Hello123%21%40%23@localhost:3306/sailors")

Session = sessionmaker(bind = engine)
session = Session()


def q1():
	# first query

	expected = [ # bid | bname | count(reserves.bid)
	(103, "Clipper", 8),
	(109, "Driftwood", 5),
	(101, "Interlake", 5),
	(110, "Klapser", 3),
	(105, "Marine", 7),
	(112, "Sooney", 2)]

	s1 = session.query(Reservation.bid, Boat.bname, func.count(Reservation.bid)).\
		join(Reservation, Boat.bid == Reservation.bid).group_by(Boat.bname).all()

	for expected, s1 in zip (expected, s1):
		assert expected == s1
	session.commit()

def q2():
	# second query:

	expected = [] # empty set

	red_boat_reserves = session.query(Sailor.sid, Sailor.sname, Boat.bid).join(Reservation, Sailor.sid == Reservation.sid).join(Boat, Reservation.bid == Boat.bid).filter(Boat.color == "red").distinct().subquery()
	num_red = session.query(func.count(Boat.bid)).filter(Boat.color == "red").scalar()
	sailors_reserved_all_red = session.query(red_boat_reserves.c.sid, red_boat_reserves.c.sname, func.count(red_boat_reserves.c.sid)).group_by(red_boat_reserves.c.sid).having(func.count(red_boat_reserves.c.sid) == num_red).all()

	assert sailors_reserved_all_red == expected
	session.commit()

def q3():
	# third query: list sailors who have reserved only red boats
	expected = [
	# sid | name
	(23, "emilio"),
	(24, "scruntus"),
	(35, "figaro"),
	(61, "ossola"),
	(62, "shaun")
	]


	sailors_not_red = session.query(Sailor.sid).join(Reservation, Sailor.sid == Reservation.sid).join(Boat, Reservation.bid == Boat.bid).filter(Boat.color != "red").group_by(Sailor.sid)

	sailors_reserves = session.query(Sailor.sid).join(Reservation, Sailor.sid == Reservation.sid).distinct().subquery()

	sailors_no_reserves = session.query(Sailor.sid).filter(Sailor.sid.notin_(sailors_reserves)).distinct()

	sailors_only_not_red = sailors_not_red.union_all(sailors_no_reserves).distinct().subquery()
	sailors_only_red = session.query(Sailor.sid, Sailor.sname).filter(Sailor.sid.notin_(sailors_only_not_red)).all()

	for expected, sailors_only_red in zip(expected, sailors_only_red):
		assert expected == sailors_only_red
	session.commit()


def q4():
	# boat with max # reservations
	expected = (101, "Interlake", 5)

	res_per_boat = session.query(Reservation.bid, Boat.bname, func.count(Reservation.bid).label("bid_count")).join(Reservation, Boat.bid == Reservation.bid).group_by(Reservation.bid).subquery()
	max_reserves_boat = session.query(res_per_boat.c.bid, res_per_boat.c.bname, func.max(res_per_boat.c.bid_count)).first()

	assert expected == max_reserves_boat
	session.commit()

def q5():
	# sailors who have never reserved a red boat

	expected = [ # sid | sname
	(29, "brutus"),
	(32, "andy"),
	(58, "rusty"),
	(60, "jit"),
	(71, "zorba"),
	(74, "horatio"),
	(85, "art"),
	(90, "vin"),
	(95, "bob")
	]


	reserved_red = session.query(Reservation.sid).join(Boat, Reservation.bid == Boat.bid).filter(Boat.color == "red").distinct()
	never_reserved_red = session.query(Sailor.sid, Sailor.sname).filter(Sailor.sid.not_in(reserved_red))

	for expected, never_reserved_red in zip(expected, never_reserved_red):
		assert expected == never_reserved_red
	session.commit()

def q6():
	# find average age of sailors whose rating is 10

	expected = (35)

	age = session.query(func.avg(Sailor.age)).filter(Sailor.rating == 10).scalar()
	assert age == expected
	session.commit()

def q7():
	# for each rating find the sailor (name and sid) with the minimum age
	expected = [
	(1, "scruntus", 24, 33),
	(3, "art", 85, 25),
	(7, "dusting", 22, 16),
	(8, "lubber", 31, 25),
	(9, "horatio", 74, 25),
	(10, "rusty", 58, 35)
	]

	min_age_rating = session.query(Sailor.rating, Sailor.sname, Sailor.sid, func.min(Sailor.age)).group_by(Sailor.rating)

	for expected, min_age_rating in zip(expected, min_age_rating):
		assert expected == min_age_rating
	session.commit()

def q8():
	# for each boat find the sailor that reserved it the most often
	expected = [
	(101, 22, 1),
	(102, 22, 1),
	(103, 22, 1),
	(104, 22, 1),
	(105, 23, 1),
	(106, 59, 2),
	(107, 88, 1),
	(108, 89, 1),
	(109, 59, 1),
	(110, 62, 2),
	(111, 88, 1),
	(112, 61, 1)
	]

	res_per_boat = session.query(Reservation.bid, Reservation.sid, func.count(Reservation.bid).label("bid_count")).group_by(Reservation.bid, Reservation.sid).order_by(Reservation.bid).subquery()
	most_reserves = session.query(res_per_boat.c.bid, res_per_boat.c.sid, func.max(res_per_boat.c.bid_count)).group_by(res_per_boat.c.bid).all()


	for expected, most_reserves in zip(expected, most_reserves):
		assert expected == most_reserves
	session.commit()


q1()
q2()
q3()
q4()
q5()
q6()
q7()
q8()
