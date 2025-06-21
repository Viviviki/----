from sqlalchemy.orm import Session
from database import engine
import models as m
import bcrypt
from datetime import datetime as dt


m.Base.metadata.drop_all(bind=engine)
m.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:

    s1 = m.Status(status_name="Доступен")
    s2 = m.Status(status_name="Арендован")
    session.add(s1)
    session.add(s2)

    r1 = m.Role(role_name="Клиент")
    r2 = m.Role(role_name="Менеджер")
    r3 = m.Role(role_name="Админ")

    session.add(r1)
    session.add(r2)
    session.add(r3)

    u1 = m.User(firstname="Петя", lastname="Иванов", username="Petya", password=bcrypt.hashpw(b"zD*F64%3", bcrypt.gensalt()), role_id=1)
    u2 = m.User(firstname="Егор", lastname="Иванов", username="Egor", password=bcrypt.hashpw(b"P*VJ0Z&f", bcrypt.gensalt()), role_id=2)
    u3 = m.User(firstname="Петя", lastname="Иванов", username="Petya007", password=bcrypt.hashpw(b"%8hC5A*Y", bcrypt.gensalt()), role_id=3)

    session.add(u1)
    session.add(u2)
    session.add(u3)

    m1 = m.Mark(name_mark="Лада")
    m2 = m.Mark(name_mark="Фольксваген")
    m3 = m.Model(name_model="Гранта")
    m4 = m.Model(name_model="Поло")
    t1 = m.Type(name_type="Седан")
    t2 = m.Type(name_type="Хетчбэк")

    session.add(m1)
    session.add(m2)
    session.add(m3)
    session.add(m4)
    session.add(t1)
    session.add(t2)

    c1 = m.Car(mark_id=1, model_id=1, year="2011", type_id=1, price_per_day="500", status_id=1)
    c2 = m.Car(mark_id=2, model_id=2, year="2013", type_id=2, price_per_day="700", status_id=2)
    
    session.add(c1)
    session.add(c2)

    arent = m.Rent(user_id=1, car_id=1, start_date=dt.strptime("2012-12-12", "%Y-%m-%d").date(), end_date=dt.strptime("2012-12-12", "%Y-%m-%d").date(), cost="1000", status_id=1 )
    session.add(arent)

    session.commit()