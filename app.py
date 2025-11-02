from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Table, Column, ForeignKey, String, select, DateTime, Numeric
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from marshmallow import ValidationError,fields
from typing import List, Optional
from datetime import date
import json

#Initializing the Flask app
app = Flask(__name__)

#Configuring the MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:78W%40ngQi%40n69@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Creating the Base Model
class Base(DeclarativeBase):
    pass

#Initializing SQLAlchemy and Marshmallow (extensions)
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

#Junction Table
orders_products = Table(
    "orders_products",
    Base.metadata,
    Column('order_id', db.Integer, ForeignKey("orders.id"), primary_key=True),
    Column('product_id', db.Integer, ForeignKey('products.id'), primary_key=True)
)

#Models
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    address: Mapped[str] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=False, unique=True)
    
    orders: Mapped[List["Order"]] = db.relationship(back_populates='user')

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[date] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    user: Mapped["User"] = db.relationship(back_populates='orders')
    products: Mapped[List["Product"]] = relationship("Product", secondary='orders_products', back_populates='orders')
    
    
class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(7, 2), nullable=False)
    orders: Mapped[List["Order"]] = relationship("Order", secondary='orders_products', back_populates='products')    

# Marshmallow Schemas

# User Schema:

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        
# Order Schema:

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        include_fk = True 
        include_relationships = True
        
# Product Schema:

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        
# Initializing the Schemas:

user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
        
#User Endpoints

#Retrieve All Users:
@app.route('/users', methods=['GET'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    
    return users_schema.jsonify(users), 200

#Retrieve User by ID:
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"message": f"Invalid user id: {id}"}), 400
        
    return user_schema.jsonify(user), 200

#Create a New User:
@app.route('/new_user', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_user = User(name=user_data['name'], address=user_data['address'], email=user_data['email'])
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.jsonify(new_user), 201

#Update a User by ID:
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid user id"}), 400

    try:
        user_data = user_schema.load(request.json)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    user.name = user_data['name']
    user.address = user_data['address']
    user.email = user_data['email']
    
    db.session.commit()
    return user_schema.jsonify(user), 200

#Delete a User by ID:
@app.route('/users/<int:id>', methods = ['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    db.session.delete(user)    
    db.session.commit()
    
    return jsonify({"message": f"Successfully deleted user {id}"}), 200

#Product Endpoints

#Retrieve All Products:
@app.route('/products', methods=['GET'])
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    
    return products_schema.jsonify(products), 200

#Retrieve a Product by ID:
@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"message": f"Invalid product id: {id}"})
    
    return product_schema.jsonify(product), 200

#Create a New Product:
@app.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_product = Product(product_name=product_data['product_name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    
    return product_schema.jsonify(new_product), 201

#Update a Product by ID:
@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"message": "Invalid product id"}), 400

    try:
        product_data = product_schema.load(request.json)
        
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    product.product_name = product_data['product_name']
    product.price = product_data['price']
    
    db.session.commit()
    return product_schema.jsonify(product), 200

#Delete a Product by ID:
@app.route('/product/<int:id>', methods = ['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"message": "Invalid prduct id"}), 400
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({"message": f"Successfuly deleted product {id}"}), 200

#Order Endpoints

#Create a New Order
@app.route('/orders/<int:usr_id>', methods = ['POST'])
def place_order(usr_id):
    user = db.session.get(User, usr_id)
    if not user:
        return jsonify({"message": f"Invalid user id: {usr_id}"})
    
    dt = date.today()
    
    new_order = Order(user_id = user.id, order_date = dt)
    
    product_list = request.json
    ids = product_list["products"]
    for product_id in ids:
        product = db.session.get(Product, product_id)
        if not product:
            return jsonify({"message": f"Invalid product id: {product_id}"})
        new_order.products.append(product)
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order), 201
               
#Add a Product to an Order:
@app.route('/orders/<int:order_id>/products/<int:product_id>', methods = ['PUT'])
def add_product(order_id, product_id):
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)
    if not order and product:
        return jsonify({"message": "Invalid order and/or product id"}), 400
    
    order.products.append(product)
    return jsonify({"message": f"Product: {product_id} added successfully!"}), 200
    
#Remove a Product From an Order:
@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods = ['PUT'])
def remove_product(order_id, product_id):        
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)
    if not order and product:
        return jsonify({"message": "Invalid order and/or product id"})
    try:
        order.products.remove(product)
    except ValueError:
        return jsonify({"message": f"Product {product_id} not found in order {order_id}"}), 400 

    db.session.commit()
    return jsonify({"message": f"Product {product_id} removed from order {order_id} successfully!"}), 200
    
#Get All Orders for a User:
@app.route('/orders/user/<int:user_id>', methods = ['GET'])
def get_users_orders(user_id):
    user_orders = ""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    for order in user.orders:
        user_orders += f"{order.id}, "
    
    return jsonify({"message": f"The following order numbers were retrieved for user {user_id}: {user_orders}."}), 200

#Get All Products for an Order:
@app.route('/orders/<int:order_id>/products', methods = ['GET'])
def get_order_products(order_id):
    order_products = ""
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message:": "Invalid order id"}), 400
    for product in order.products:
        order_products += f"{product.id}, "
        
    return jsonify({"message": f"The following products were retrieved for order {order_id}: {order_products}"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()

