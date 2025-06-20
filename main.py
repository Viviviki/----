from fastapi import FastAPI, HTTPException, Depends, Query
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
from auth import auth_handler
import bcrypt


app=FastAPI()

@app.post("/login")
def user_auth(login: pyd.LoginUser, db: Session=Depends(get_db)):
    user_db = db.query(m.User).filter(
        m.User.login == login.login
    ).first()
    if not user_db:
        raise HTTPException(404, "Пользователь не найден!")
    if auth_handler.verify_password(login.password, user_db.password):
        # logging.info(f"{dt.now()} - User: {user_db.username} loggined")
        return {"token": auth_handler.encode_token(user_db.id, user_db.role_id)}
    # logging.info(f"{dt.now()} - User: {user_db.username} fail authentication")
    raise HTTPException(400, "Доступ запрещён!")

# Товары
# Получение товаров
@app.get("/api/products", response_model=List[pyd.SchemeProduct])
def get_products(limit:None|int=Query(None, le=100), page:None|int=Query(1), category:None|str=Query(None), minPrice:None|float=Query(None), db:Session=Depends(get_db)):
    products = db.query(m.Product)
    if category:
        category_db = db.query(m.Category).filter(
            m.Category.category_name == category
        ).first()
        if not category_db:
            raise HTTPException(404, "Категория не найдена!")
        products = products.filter(
            m.Product.category_id == category_db.id
        )
    if minPrice:
        products = products.filter(
            m.Product.product_price >= minPrice
        )
    if limit:
        products = products[(page - 1) * limit:page * limit]
        if not products:
            raise HTTPException(404, "Товары не найдены!")
        return products
    all_product = products.all()
    if not all_product:
        raise HTTPException(404, "Товары не найдены!")
    return all_product

# Получение товара
@app.get("/api/product/{id}", response_model=pyd.SchemeProduct)
def get_product(id:int, db:Session=Depends(get_db)):
    product_db = db.query(m.Product).filter(
        m.Product.id == id
    ).first()
    if not product_db:
        raise HTTPException(404, "Товар не найден!")
    return product_db

# Создание товара
@app.post("/api/product", response_model=pyd.SchemeProduct)
def create_product(product:pyd.CreateProduct, db:Session=Depends(get_db), manager:m.User=Depends(auth_handler.manager_wrapper)):
    product_dublicate = db.query(m.Product).filter(
        m.Product.product_name == product.product_name
    ).first()
    if product_dublicate:
        raise HTTPException(400, "Такой товар уже существует!")
    product_db = m.Product()
    product_db.product_name = product.product_name
    product_db.product_price = product.product_price
    product_db.category_id = product.category_id
    product_db.description = product.description
    product_db.amount = product.amount

    db.add(product_db)
    db.commit()

    logging.info(f"{dt.now()} - User: {manager["user_id"]} - {manager["username"]} create product: {product_db.product_name}")
    return product_db


# Изменение товара
@app.put("/api/product/{id}", response_model=pyd.SchemeProduct)
def edit_product(id:int, product:pyd.CreateProduct, db:Session=Depends(get_db), manager:m.User=Depends(auth_handler.manager_wrapper)):
    product_db = db.query(m.Product).filter(
        m.Product.id == id
    ).first()
    if not product_db:
        raise HTTPException(404, "Товар не найден!")
    product_db.product_name = product.product_name
    product_db.product_price = product.product_price
    product_db.category_id = product.category_id
    product_db.description = product.description
    product_db.amount = product.amount

    db.add(product_db)
    db.commit()

    return product_db

# Удаление товара
@app.delete("/api/product/{id}")
def delete_product(id:int, db:Session=Depends(get_db), manager:m.User=Depends(auth_handler.manager_wrapper)):
    product_db = db.query(m.Product).filter(
        m.Product.id == id
    ).first()
    if not product_db:
        raise HTTPException(404, "Товар не найден!")
    db.delete(product_db)
    db.commit()

    return {"detail": "Товар удалён!"}


# Заказы
# Получение заказов
@app.get("/api/orders", response_model=List[pyd.SchemeOrder])
def get_orders(db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    orders = db.query(m.Order).all()
    return orders


# Получение заказа
@app.get("/api/order/{id}", response_model=pyd.SchemeOrder)
def get_order(id:int, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    order_db = db.query(m.Order).filter(
        m.Order.id == id,
    ).first()
    if not order_db:
        raise HTTPException(404, "Заказ не найден!")
    if order_db.user_id != user["user_id"]:
        logging.info(f"{dt.now()} - User: {user["user_id"]} - {user["username"]} try watch order of User: {order_db.user_id}")
        raise HTTPException(403, "Вы не можете просматривать чужой заказ!")
    return order_db


# Создание заказа
@app.post("/api/order", response_model=pyd.SchemeOrder)
def create_order(order:pyd.CreateOrder, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    order_db = m.Order()
    user_db = db.query(m.User).filter(
        m.User.id == order.user_id
    ).first()
    if not user_db:
        raise HTTPException(404, "Пользователь не найден!")
    if user["role_id"] not in [2, 3]:
        if order.user_id != user["user_id"]:
            logging.info(f"{dt.now()} - User: {user["user_id"]} - {user["username"]} try create order from User: {order.user_id}")
            raise HTTPException(403, "Вы не можете создать заказ на чужое имя!")
    order_db.user_id = order.user_id
    order_db.status_id = order.status_id
    order_db.summ = order.summ
    order_db.order_date = order.order_date

    db.add(order_db)
    db.commit()

    logging.info(f"{dt.now()} - User: {user["user_id"]} - {user["username"]} create order: {order_db.id}")
    return order_db


# Изменение заказа
@app.put("/api/order/{id}", response_model=pyd.SchemeOrder)
def edit_order(id:int, order:pyd.CreateOrder, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    order_db = db.query(m.Order).filter(
        m.Order.id == id
    ).first()
    if not order_db:
        raise HTTPException(404, "Заказ не найден!")
    if user["role_id"] not in [2, 3]:
        if order.user_id != user["user_id"]:
            logging.info(f"{dt.now()} - User: {user["user_id"]} - {user["username"]} try create order from User: {order.user_id}")
            raise HTTPException(403, "Вы не можете изменять чужой заказ!")
    order_db.user_id = order.user_id
    order_db.status_id = order.status_id
    order_db.summ = order.summ
    order_db.order_date = order.order_date

    db.add(order_db)
    db.commit()

    return order_db


# Удаление заказа
@app.delete("/api/order/{id}")
def delete_order(id:int, db:Session=Depends(get_db), manager:m.User=Depends(auth_handler.manager_wrapper)):
    order_db = db.query(m.Order).filter(
        m.Order.id == id
    ).first()
    if not order_db:
        raise HTTPException(404, "Заказ не найден!")
    
    db.delete(order_db)
    db.commit()

    return {"detail": "Заказ удалён"}


# Отзывы
# Получение отзывов
@app.get("/api/reviews", response_model=List[pyd.SchemeReview])
def get_reviews(db:Session=Depends(get_db)):
    reviews = db.query(m.Review).filter(
        m.Review.accepted == True
    ).all()
    if not reviews:
        raise HTTPException(404, "Отзывы не найдены!")
    return reviews


# Получение отзыва
@app.get("/api/review/{id}", response_model=pyd.SchemeReview)
def get_review(id:int, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    review_db = db.query(m.Review).filter(
        m.Review.id == id
    ).first()
    if not review_db:
        raise HTTPException(404, "Отзыв не найден!")
    return review_db


# Создание отзыва
@app.post("/api/review", response_model=pyd.SchemeReview)
def create_review(review:pyd.CreateReview, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    review_check = db.query(m.Review).filter(
        m.Review.user_id == review.user_id,
        m.Review.product_id == review.product_id
    ).first()
    if review_check:
        raise HTTPException(400, "Вы уже оставляли отзыв на этот товар!")
    if review.user_id != user["user_id"]:
        logging.info(f"{dt.now()} - User: {user["user_id"]} - {user["username"]} try create review from User: {review.user_id}")
        raise HTTPException(403, "Вы не можете оставлять отзыв от чужого лица!")
    review_db = m.Review()
    review_db.rating = review.rating
    review_db.product_id = review.product_id
    review_db.user_id = review.user_id
    review_db.description = review.description

    db.add(review_db)
    db.commit()

    return review_db


# Изменение отзыва
@app.put("/api/review/{id}", response_model=pyd.SchemeReview)
def edit_review(id:int, review:pyd.CreateReview, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    if review.user_id != user["user_id"]:
        logging.info(f"{dt.now()} - User: {user["user_id"]} - {user["username"]} try change review: {id}")
        raise HTTPException(403, "Вы не можете редактировать чужой отзыв!")
    review_db = db.query(m.Review).filter(
        m.Review.id == id,
        m.Review.user_id == user["user_id"]
    ).first()
    if not review_db:
        raise HTTPException(404, "Отзыв не найден!")
    review_db.rating = review.rating
    review_db.product_id = review.product_id
    review_db.user_id = review.user_id
    review_db.description = review.description

    db.add(review_db)
    db.commit()

    return review_db

# Одобрение отзыва
@app.patch("/api/review/{id}")
def accept_review(id:int, review:pyd.AcceptReview, admin:m.User=Depends(auth_handler.admin_wrapper), db:Session=Depends(get_db)):
    review_db = db.query(m.Review).filter(
        m.Review.id == id
    ).first()
    if not review_db:
        raise HTTPException(404, "Отзыв не найден!")
    review_db.accepted = review.accepted

    db.add(review_db)
    db.commit()

    return {'detail': 'Доступность отзыва изменена'}

# Удаление отзыва
@app.delete("/api/review/{id}")
def delete_review(id:int, db:Session=Depends(get_db), user:m.User=Depends(auth_handler.auth_wrapper)):
    review_db = db.query(m.Review).filter(
        m.Review.id == id
    ).first()
    if not review_db:
        raise HTTPException(404, "Отзыв не найден!")
    
    db.delete(review_db)
    db.commit()

    return {"detail": "Отзыв удалён"}