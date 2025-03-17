from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Float, ForeignKey
import os
from dotenv import load_dotenv
import stripe

load_dotenv()
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///store.db"
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)

stripe.api_key = STRIPE_SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



class User(db.Model, UserMixin):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String, unique=True, nullable=False)
    password_hash = db.Column(String, nullable=False)
    cart = relationship("Cart", back_populates="user")

class Cart(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('user.id'))
    product_name = db.Column(String, nullable=False)
    price = db.Column(Float, nullable=False)
    image_url = db.Column(String, nullable=True)
    user = relationship("User", back_populates="cart")

class Product(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=False)
    category = db.Column(String, nullable=False)
    price = db.Column(Float, nullable=False)
    image_url = db.Column(String, nullable=True)
    description = db.Column(String, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route("/")
def index():
    top_items = {category: db.session.query(Product).filter_by(category=category).first() for category in ["T-Shirts", "Sweatshirts", "Hoodies", "Jeans", "Pants"]}
    all_items = {category: db.session.query(Product).filter_by(category=category).all() for category in ["T-Shirts", "Sweatshirts", "Hoodies", "Jeans", "Pants"]}
    return render_template("index.html", top_items=top_items, all_items=all_items)

@app.route("/product/<int:product_id>")
def product_page(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return "Product not found", 404
    return render_template("product-page.html", product=product)

@app.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        price = float(request.form["price"])
        image_url = request.form["image_url"]
        description = request.form["description"]
        new_product = Product(name=name, category=category, price=price, image_url=image_url, description=description)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(username=username,
                        password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/cart")
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template("cart.html", cart_items=cart_items)

@app.route("/add_to_cart/<product_name>/<price>/<path:image_url>")
@login_required
def add_to_cart(product_name, price, image_url):
    new_cart_item = Cart(user_id=current_user.id,
                         product_name=product_name,
                         price=price,
                         image_url=image_url)
    db.session.add(new_cart_item)
    db.session.commit()
    return redirect(url_for("cart"))

@app.route("/remove_from_cart/<int:item_id>")
@login_required
def remove_from_cart(item_id):
    item = Cart.query.get_or_404(item_id)
    if item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.price for item in cart_items)

    if request.method == "POST":
        line_items = []
        for item in cart_items:
            line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": item.product_name},
                "unit_amount": int(item.price * 100),
            },
            "quantity": 1,
        })

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=url_for("success", _external=True),
            cancel_url=url_for("cart", _external=True),
        )
        return redirect(session.url, code=303)

    return render_template("checkout.html", cart_items=cart_items, total_price=total_price)

@app.route("/success")
def success():
    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return render_template("success.html")

@app.route("/category/<category>")
def category_page(category):
    products = Product.query.filter_by(category=category).all()
    if not products:
        return "No products found in this category", 404
    return render_template("category.html", category=category, products=products)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
