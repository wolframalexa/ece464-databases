# populates the new sailors_extended database with tables Sailor, Base, Reservation, and Expense

from __future__ import print_function
from ipdb import set_trace

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, DateTime, Numeric
Base = declarative_base()

class Sailor(Base):
    __tablename__ = 'sailors'

    sid = Column(Integer, primary_key=True)
    sname = Column(String)
    rating = Column(Integer)
    age = Column(Integer)

    def __repr__(self):
        return "<Sailor(id=%s, name='%s', rating=%s)>" % (self.sid, self.sname, self.age)


from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

class Boat(Base):
    __tablename__ = 'boats'

    bid = Column(Integer, primary_key=True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)

    reservations = relationship('Reservation',
                                backref=backref('boat', cascade='delete'))

    def __repr__(self):
        return "<Boat(id=%s, name='%s', color=%s)>" % (self.bid, self.bname, self.color)

from sqlalchemy import PrimaryKeyConstraint

class Reservation(Base):
    __tablename__ = 'reserves'
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)
    amount_paid = Column(Numeric)

    sailor = relationship('Sailor')

    def __repr__(self):
        return "<Reservation(sid=%s, bid=%s, day=%s, amount_paid=%d)>" % (self.sid, self.bid, self.day, self.amount_paid)


class Expense(Base):
    __tablename__ = 'expenses'

    eid = Column(Integer, primary_key=True)
    type = Column(Integer)
    recipient_id = Column(Integer)
    day = Column(DateTime)
    amount = Column(Numeric(2))

    def __repr__(self):
        return "<Expense(eid=%s, type=%s, recipient_id=%s, day=%s, amount=%d)>" % (self.eid, self.type, self.recipient_id, self.day, self.amount)
