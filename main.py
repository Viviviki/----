from fastapi import FastAPI, HTTPException, Depends, Query
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
from auth import auth_handler
import bcrypt
import decimal


app=FastAPI()

@app.post("/login")
def user_auth(login: pyd.LoginUser, db: Session=Depends(get_db)):
    user_db = db.query(m.User).filter(
        m.User.username == login.username
    ).first()
    if not user_db:
        raise HTTPException(404, "Пользователь не найден!")
    if auth_handler.verify_password(login.password, user_db.password):
        # logging.info(f"{dt.now()} - User: {user_db.username} loggined")
        return {"token": auth_handler.encode_token(user_db.id, user_db.role_id)}
    # logging.info(f"{dt.now()} - User: {user_db.username} fail authentication")
    raise HTTPException(400, "Доступ запрещён!")

@app.get("/api/cars")
def get_cars(page:None|int=Query(1), limit:None|int=Query(None, le=100), type:str|None=Query(None),
    status: str = None, minPrice_per_day:None|float=Query(None), db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    cars = db.query(m.Car)
    if type:
        type_db = db.query(m.Type).filter(
            m.Type.name_type == type
        ).first()
        if not type_db:
            raise HTTPException(404, "Тип машины не найден")
        cars = cars.filter(
            m.Car.type_id == type_db.id
        )
    if minPrice_per_day:
        cars = cars.filter(
            m.Car.price_per_day >= minPrice_per_day
        )
    if limit:
        cars = cars[(page - 1) * limit:page * limit]
        if not cars:
            raise HTTPException(404, "Машины не найдены")
        return cars
    all_car = cars.all()
    if not all_car:
        raise HTTPException(404, "Машины не найдены")
    return all_car


@app.get("/api/car/{id}")
def get_car(id:int, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    car_db = db.query(m.Car).filter(
        m.Car.id == id
    ).first()
    if not car_db:
        raise HTTPException(404, "Машина не найдена")
    return car_db

@app.post("/api/car")
def create_car(car:pyd.CreateCar, db:Session=Depends(get_db), manager:m.User=Depends(auth_handler.manager_wrapper)):
    car_db = m.Car()
    car_db.mark_id = car.mark_id
    car_db.model_id =car.model_id
    car_db.year = car.year
    car_db.type_id = car.type_id
    car_db.price_per_day = car.price_per_day
    car_db.status_id = car.status_id

    db.add(car_db)
    db.commit()
    return car_db


@app.put("/api/car/{id}")
def edit_car(id:int, car:pyd.CreateCar, db:Session=Depends(get_db), manager:m.User=Depends(auth_handler.manager_wrapper)):
    car_db = db.query(m.Car).filter(
        m.Car.id == id
    ).first()
    if not car_db:
        raise HTTPException(404, "Машина не найдена")
    car_db.mark_id = car.mark_id
    car_db.model_id =car.model_id
    car_db.year = car.year
    car_db.type_id = car.type_id
    car_db.price_per_day = car.price_per_day
    car_db.status_id = car.status_id

    db.add(car_db)
    db.commit()
    return car_db


@app.delete("/api/car/{id}")
def delete_car(id:int, db:Session=Depends(get_db), manager:m.User=Depends(auth_handler.manager_wrapper)):
    car_db = db.query(m.Car).filter(
        m.Car.id == id
    ).first()
    if not car_db:
        raise HTTPException(404, "Машина не найдена")
    db.delete(car_db)
    db.commit()

    return {"detail": "Машина удалёна"}



@app.get("/api/rents")
def get_rents(db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    rents = db.query(m.Rent).all()
    return rents



@app.get("/api/rent/{id}")
def get_rent(id:int, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    rent_db = db.query(m.Rent).filter(
        m.Rent.id == id,
    ).first()
    if not rent_db:
        raise HTTPException(404, "Аренда не найдена")
    return rent_db


@app.post("/api/rent")
def create_rent(rent:pyd.CreateRent, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    rent_db = m.Rent()
    user_db = db.query(m.User).filter(
        m.User.id == rent.user_id
    ).first()
    if not user_db:
        raise HTTPException(404, "Клиент не найден")
    rent_db.user_id = rent.user_id
    rent_db.status_id = rent.status_id
    rent_db.start_date = rent.start_date
    rent_db.end_date = rent.end_date
    rent_db.cost = rent.cost
    db.add(rent_db)
    db.commit()

    return rent_db



@app.put("/api/rent/{id}")
def edit_rent(id:int, rent:pyd.CreateRent, db:Session=Depends(get_db),  manager:m.User=Depends(auth_handler.manager_wrapper)):
    rent_db = db.query(m.Rent).filter(
        m.Rent.id == id
    ).first()
    if not rent_db:
        raise HTTPException(404, "Аренда не найдена")
    rent_db.user_id = rent.user_id
    rent_db.status_id = rent.status_id
    rent_db.start_date = rent.start_date
    rent_db.end_date = rent.end_date
    rent_db.cost = rent.cost
    db.add(rent_db)
    db.commit()

    return rent_db

@app.delete("/api/rent/{id}")
def delete_rent(id:int, db:Session=Depends(get_db), manager:m.User=Depends(auth_handler.manager_wrapper)):
    rent_db = db.query(m.Rent).filter(
        m.Rent.id == id
    ).first()
    if not rent_db:
        raise HTTPException(404, "Аренда не найдена")
    
    db.delete(rent_db)
    db.commit()

    return {"detail": "Аренда удалёна"}
# Users
@app.post("/api/user")
def create_user(user:pyd.CreateUser, db:Session=Depends(get_db), admin:m.User=Depends(auth_handler.admin_wrapper)):
    user_db = m.User()
    user_db.firstname = user.firstname
    user_db.lastname = user.lastname
    user_db.username = user.username
    user_db.password = user.end_date
    user_db.role_id = user.role_id
    db.add(user_db)
    db.commit()

    return user_db



@app.put("/api/user/{id}")
def edit_user(id:int, user:pyd.CreateUser, db:Session=Depends(get_db), admin:m.User=Depends(auth_handler.admin_wrapper)):
    user_db = db.query(m.User).filter(
        m.User.id == id
    ).first()
    if not user_db:
        raise HTTPException(404, "Клиент не найден")
    user_db.firstname = user.firstname
    user_db.lastname = user.lastname
    user_db.username = user.username
    user_db.password = user.end_date
    user_db.role_id = user.role_id
    db.add(user_db)
    db.commit()

    return user_db


@app.delete("/api/user/{id}")
def delete_user(id:int, db:Session=Depends(get_db), admin:m.User=Depends(auth_handler.admin_wrapper)):
    user_db = db.query(m.User).filter(
        m.User.id == id
    ).first()
    if not user_db:
        raise HTTPException(404, "Клиент не найден")
    
    db.delete(user_db)
    db.commit()

    return {"detail": "Клиент удален"}


# Отзывы
# Получение отзывов
@app.get("/api/reviews")
def get_reviews(db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    reviews = db.query(m.Review).all()
    if not reviews:
        raise HTTPException(404, "Отзывы не найдены")
    return reviews


# Получение отзыва
@app.get("/api/review/{id}")
def get_review(id:int, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    review_db = db.query(m.Review).filter(
        m.Review.id == id
    ).first()
    if not review_db:
        raise HTTPException(404, "Отзыв не найден")
    return review_db


# Создание отзыва
@app.post("/api/review")
def create_review(review:pyd.CreateReview, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    review_check = db.query(m.Review).filter(
        m.Review.user_id == review.user_id,
        m.Review.car_id == review.car_id
    ).first()
    if review_check:
        raise HTTPException(400, "Вы уже оставляли отзыв на машину")
    if review.user_id != user["user_id"]:
        raise HTTPException(403, "Вы не можете оставлять отзыв от чужого лица")
    review_db = m.Review()
    review_db.rating = review.rating
    review_db.car_id = review.car_id
    review_db.user_id = review.user_id
    review_db.description = review.description

    db.add(review_db)
    db.commit()

    return review_db


# Изменение отзыва
@app.put("/api/review/{id}")
def edit_review(id:int, review:pyd.CreateReview, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    if review.user_id != user["user_id"]:
        raise HTTPException(403, "Вы не можете редактировать чужой отзыв")
    review_db = db.query(m.Review).filter(
        m.Review.id == id,
        m.Review.user_id == user["user_id"]
    ).first()
    if not review_db:
        raise HTTPException(404, "Отзыв не найден")
    review_db.rating = review.rating
    review_db.car_id = review.car_id
    review_db.user_id = review.user_id
    review_db.description = review.description

    db.add(review_db)
    db.commit()

    return review_db


# Удаление отзыва
@app.delete("/api/review/{id}")
def delete_review(id:int, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    review_db = db.query(m.Review).filter(
        m.Review.id == id
    ).first()
    if not review_db:
        raise HTTPException(404, "Отзыв не найден")
    
    db.delete(review_db)
    db.commit()

    return {"detail": "Отзыв удалён"}