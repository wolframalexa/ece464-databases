from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker

# todo: figure out why this isn't connecting
engine = create_engine('mysql://alexa@localhost/sailors')

Session = sessionmaker(bind = engine)
session = Session()


# revenue this month: Oct 1998
revenue = session.query(func.sum(Reservation.amount_paid)).filter(day<='1998/10/31').filter(day>='1998/10/01')
assert revenue == 412

# sailors bringing in the most revenue
expected_sailors = [
	# sid | sname | sum(reserves.amount_paid)
	(31, lubber, 10197),
	(59, stum, 5107),
	(64, horatio, 3798),
	(35, figaro, 2940),
	(88, dan,1596),
	(60, jit,1283),
	(22, dusting, 590),
	(23, emilio, 551),
	(62, shaun, 145),
	(24, scruntus,100),
	(89, dye, 88),
	(61, ossola, 46),
	(90, vin, 36),
	(74, horatio, 23)
]

sailors_order_by_revenue = session.query(Sailor.sid, Sailor.sname, func.sum(Reservation.amount_paid)).join(Sailor, Reservation.sid == Sailor.sid).group_by(Sailor.sid).order_by(func.sum(Reservation.amount_paid))

for sailors_order_by_revenue, expected_sailors in zip(sailors_order_by_revenue, expected_sailors):
	assert sailors_order_by_revenue == expected_sailors

# boats bringing in the most revenue
expected_boats = [
# bid | bname     | sum(reserves.amount_paid) 
	(105,Marine,8171),
	(102,Interlake,5698),
	(103,Clipper,4679),
	(101,Interlake,3810),
	(106,Marine,1393),
	(110,Klapser,779),
	(104,Clipper,770),
	(111,Sooney,489),
	(107,Marine,473),
	(109,Driftwood,147),
	(112,Sooney,46),
	(108,Driftwood,45),
]

boats_order_by_revenue = session.query(Boat.bid, Boat.bname, func.sum(Reservation.amount_paid)).join(Boat, Reservation.bid == Boat.bid).group_by(Boat.bid).order_by(func.sum(Reservation.amount_paid))

for boats_order_by_revenue, expected_boats in zip(boats_order_by_revenue, expected_boats):
	assert boats_order_by_revenue == expected_boats

# major costs of the business

expected_costs = [

#	| type | sum(amount) |
	(4, 10000),
	(1, 1600),
	(5, 1457),
	(0, 1000),
	(2, 137)
]

costs = session.query(Expense.type, func.sum(Expense.amount)).group_by(Expense.type).order_by(func.sum(amount))

for costs, expected_costs in zip(costs, expected_costs):
	assert costs == expected_costs

