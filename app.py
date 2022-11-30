from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from flask_wtf import FlaskForm
# from flask_bcrypt import Bcrypt
# from wtforms import StringField, PasswordField, SubmitField, SelectField
# from wtforms.validators import InputRequired, Length, ValidationError
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import os

app = Flask(__name__)
CORS(app)

admin = Admin(app)

courses = os.path.abspath(os.path.dirname(__file__)) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(courses, 'DealershipDB.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'miata'
# app.config['SQLALCHEMY_ECHO'] = True #prints query to console for testing



db = SQLAlchemy(app)

class Vehicle(db.Model):
    v_VIN = db.Column(db.String, primary_key = True)
    v_year = db.Column(db.Float, unique = False)
    v_make = db.Column(db.String, unique = False) 
    v_model = db.Column(db.String, unique = False)
    v_trim = db.Column(db.Integer, unique = False)
    v_color = db.Column(db.Integer, unique = False)
    v_MSRP = db.Column(db.Float, unique = False)
    v_status = db.Column(db.String, unique = False)

    def __repr__(self):
        return f'<Car: {self.v_make, self.v_model}>'
    
class Salesperson(db.Model):
    sp_ID = db.Column(db.Integer, primary_key = True)
    sp_name = db.Column(db.String, unique = False)
    sp_position = db.Column(db.String, unique = False)
    
class Sales(db.Model):
    s_invoiceNo = db.Column(db.Integer, primary_key = True)
    s_date = db.Column(db.String, unique = False)
    s_VIN = db.Column(db.String, unique = False)
    s_spID = db.Column(db.Integer, unique = False)
    s_cID = db.Column(db.Integer, unique = False)
    s_MSRP = db.Column(db.Integer, unique = False)
    s_totalCost = db.Column(db.Integer, unique = False)
    
class Customer(db.Model):
    c_ID = db.Column(db.Integer, primary_key = True)
    c_name = db.Column(db.String, unique = False)
    c_phone = db.Column(db.String, unique = False)
    

admin.add_view(ModelView(Vehicle, db.session))
admin.add_view(ModelView(Salesperson, db.session))
admin.add_view(ModelView(Sales, db.session))
admin.add_view(ModelView(Customer, db.session))


@app.route('/student', methods = ['GET'])
def student():

    return render_template('student_page.html')

@app.route('/sale/<string:vin>', methods = ['GET', 'PUT'])
def addSale(vin):
    custName = request.form.get("custName")
    custNo = request.form.get("custNo")
    print(vin, custName, custNo)
    print(type(vin), type(custName), type(custNo))
    return redirect(url_for('sales'))

@app.route('/sales', methods = ['GET'])
def sales():
    sales = (Sales.query.join(Salesperson, Salesperson.sp_ID==Sales.s_spID)
                        .join(Customer, Customer.c_ID==Sales.s_cID)
                        .join(Vehicle, Vehicle.v_VIN==Sales.s_VIN)
                        .add_columns(Salesperson.sp_name, Customer.c_name,Sales.s_invoiceNo,Sales.s_date,
                                     Sales.s_VIN,Sales.s_spID,Sales.s_cID,Sales.s_MSRP,Sales.s_totalCost,
                                     Vehicle.v_year,Vehicle.v_make,Vehicle.v_model)
                        .all())
    return render_template('sales.html', sales=sales)

    

    
@app.route('/maint', methods = ['GET'])
def maint():
    maint = (Sales.query.join(Salesperson, Salesperson.sp_ID==Sales.s_spID)
                        .join(Customer, Customer.c_ID==Sales.s_cID)
                        .join(Vehicle, Vehicle.v_VIN==Sales.s_VIN)
                        .add_columns(Salesperson.sp_name, Customer.c_name,Sales.s_invoiceNo,Sales.s_date,
                                     Sales.s_VIN,Sales.s_spID,Sales.s_cID,Sales.s_MSRP,Sales.s_totalCost,
                                     Vehicle.v_year,Vehicle.v_make,Vehicle.v_model)
                        .all())
    return render_template('maint.html', maint=maint)

@app.route('/cars', methods = ['GET'])  #SHOWS ALL CARS CURRENTLY FOR SALE
def cars():
    car = Vehicle.query.filter_by(v_status="FOR SALE").all()
    return render_template('viewcars.html', allCars=car)

@app.route('/cars/<string:vin>', methods = ['GET'])  #Link to individually selected vehicle by VIN
def thisCar(vin):
    car = Vehicle.query.filter_by(v_VIN=vin).first()
    salesperson = Salesperson.query.all()
    return render_template('selectedcar.html', thisCar=car, sper=salesperson)

@app.route("/")     #HOME PAGE
def home():
    return render_template('index.html')

@app.route("/home")     #HOME PAGE
def home2():
    return redirect(url_for('/'))


if __name__ == '__main__':
    app.run(debug=True)

with app.app_context():
    db.create_all()