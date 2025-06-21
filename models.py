from database import Base
from sqlalchemy import Column, Integer, String, Float, DECIMAL, ForeignKey, Text, Date, Boolean, DECIMAL
from sqlalchemy.orm import relationship


class Car(Base):
    __tablename__="cars"
    id = Column(Integer, primary_key=True, autoincrement=True)
    mark_id = Column(Integer, ForeignKey("marks.id"), default=1)
    model_id = Column(Integer, ForeignKey("models.id"), default=1)
    year = Column(Integer)
    type_id = Column(Integer, ForeignKey("types.id"), default=1)
    price_per_day = Column(Float)
    status_id = Column(Integer, ForeignKey("statuses.id"), default=1)

    mark = relationship("Mark", backref="cars")
    model = relationship("Model", backref="cars")
    type = relationship("Type", backref="cars")
    status = relationship("Status", backref="cars")


class Mark(Base):
    __tablename__="marks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_mark = Column(String)

class Model(Base):
    __tablename__="models"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_model = Column(String)

class Type(Base):
    __tablename__="types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_type = Column(String)


class Rent(Base):
    __tablename__="rents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), default=1)
    car_id = Column(Integer, ForeignKey("cars.id"), default=1)
    start_date = Column(Date)
    end_date = Column(Date)
    cost = Column(DECIMAL)
    status_id = Column(Integer, ForeignKey("statuses.id"), default=1)

    user = relationship("User", backref="rents")
    car = relationship("Car", backref="rents")
    status = relationship("Status", backref="rents")

class Role(Base):
    __tablename__="roles"
    id=Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(20), unique=True)


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(20))
    lastname = Column(String(20))
    username = Column(String(20), unique=True)
    password = Column(String(255))
    role_id = Column(Integer, ForeignKey("roles.id"), default=1)

    role = relationship("Role", backref='users')


class Status(Base):
    __tablename__="statuses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String(20))


class Review(Base):
    __tablename__="reviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey("cars.id"), default=1)
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Float)
    description = Column(Text, nullable=True)

    car = relationship("Car", backref="reviews")
    user = relationship("User", backref="reviews")