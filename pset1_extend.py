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


# major costs of the business



