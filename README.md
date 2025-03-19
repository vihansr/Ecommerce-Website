# 🛍️ Flask E-Commerce Store with Stripe Checkout

## 🚀 Project Overview
This is a **fully functional e-commerce web application** built using **Flask, SQLAlchemy, Bootstrap, and Stripe** for payment processing. Users can **browse products by category, add items to their cart, and securely complete purchases via Stripe.**

🌐 Live Demo: [Fashion-Haven](https://fashion-haven.onrender.com)

## 🎯 Features
✅ **User Authentication** (Register/Login using Flask-Login)  
✅ **Product Management** (Add, View, and Categorize Products)  
✅ **Shopping Cart** (Add/Remove Products & View Total Price)  
✅ **Secure Payments** with **Stripe Checkout**  
✅ **Category-Based Browsing** (Easily filter products by category)  
✅ **Order Success Page** (Cart clears after successful payment)  

## 🛠️ Technologies Used
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **Flask-Login** - User authentication
- **Bootstrap** - Responsive UI
- **Stripe API** - Payment processing

## 📂 Installation & Setup
1️⃣ **Clone the Repository**
```bash
git clone https://github.com/vihansr/ecommerce-website.git
cd Ecommerce-Website
```

2️⃣ **Create a Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3️⃣ **Set Up Environment Variables** (Create a `.env` file and add your Stripe keys)
```ini
STRIPE_PUBLIC_KEY=your_publishable_key
STRIPE_SECRET_KEY=your_secret_key
SECRET_KEY=your_flask_secret_key
```

4️⃣ **Run the Application**
```bash
flask run
```

## 🛒 How It Works
1️⃣ **Users register/login** to access the cart & checkout.  
2️⃣ **Browse products** by category and add them to the cart.  
3️⃣ **Proceed to checkout**, where Stripe handles secure payments.  
4️⃣ **After successful payment, the cart is cleared** and users see a success page.  

## 📌 Future Enhancements
- ✅ Order tracking system
- ✅ Admin panel for product management
- ✅ User reviews & ratings

## 📩 Contributions & Feedback
Feel free to **fork, improve, and submit PRs!** Suggestions are always welcome. 😊

📧 **Contact:** vihansrathore2006@email.com  
📌 **GitHub:** [Ecommerce-Website](https://github.com/vihansr/ecommerce-website)
