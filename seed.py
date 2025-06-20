from sqlalchemy.orm import Session
from database import engine
import models as m
import bcrypt


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
    u2 = m.User(firstname="Егор", lastname="Иванов", username="Egor", password=bcrypt.hashpw(b"d*1#09Ru", bcrypt.gensalt()), role_id=2)
    u3 = m.User(firstname="Петя", lastname="Иванов", username="Petya007", password=bcrypt.hashpw(b"%8hC5A*Y", bcrypt.gensalt()), role_id=3)

    session.add(u1)
    session.add(u2)
    session.add(u3)

    c1 = m.Product(product_name="Самсунг", product_price="86000", 
                category_id="1", amount="500")
    c2 = m.Product(product_name="Айфон", product_price="64000", 
                category_id="1", amount="600")
    
    session.add(p1)
    session.add(p2)

    session.commit()