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
app.config['SQLALCHEMY_ECHO'] = True #prints query to console for testing



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
    
class Mechanic(db.Model):
    m_ID = db.Column(db.Integer, primary_key = True)
    m_name = db.Column(db.String, unique = False)
    m_position = db.Column(db.String, unique = False)
    
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
    
class Part(db.Model):
    p_partKey = db.Column(db.Integer, primary_key = True)
    p_partName = db.Column(db.String, unique = False)
    p_isOEM = db.Column(db.Boolean, unique = False)
    p_partCost = db.Column(db.Float, unique = False) 

class Equipment(db.Model):
    e_equipmentKey = db.Column(db.Integer, primary_key = True)
    e_name = db.Column(db.String, unique = False)
    e_comment = db.Column(db.String, unique = False)
    
class Service(db.Model):
    sv_workOrderNo = db.Column(db.Integer, primary_key = True)
    sv_serviceType = db.Column(db.String, unique = False)
    sv_date = db.Column(db.String, unique = False)
    sv_VIN = db.Column(db.String, unique = False)
    sv_partKey = db.Column(db.Integer, unique = False)
    sv_equipmentKey = db.Column(db.Integer, unique = False)
    sv_cID = db.Column(db.Integer, unique = False)
    sv_mID = db.Column(db.Integer, unique = False)
    sv_partCost = db.Column(db.Integer, unique = False)
    sv_partQty = db.Column(db.Integer, unique = False)
    sv_completed = db.Column(db.Boolean, unique = False)
    

admin.add_view(ModelView(Vehicle, db.session))
admin.add_view(ModelView(Salesperson, db.session))
admin.add_view(ModelView(Mechanic, db.session))
admin.add_view(ModelView(Sales, db.session))
admin.add_view(ModelView(Service, db.session))

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
    maint = (Service.query.outerjoin(Mechanic, Mechanic.m_ID==Service.sv_mID)
                            .outerjoin(Customer, Customer.c_ID==Service.sv_cID)
                            .outerjoin(Vehicle, Vehicle.v_VIN==Service.sv_VIN)
                            .outerjoin(Part, Part.p_partKey==Service.sv_partKey)
                            .outerjoin(Equipment, Equipment.e_equipmentKey==Service.sv_equipmentKey)
                            .add_columns(Service.sv_workOrderNo,Service.sv_date,Service.sv_serviceType,Service.sv_partQty,Service.sv_completed,
                                         Vehicle.v_VIN,Vehicle.v_year,Vehicle.v_make,Vehicle.v_model,
                                         Mechanic.m_name, Part.p_partName, Equipment.e_name,Customer.c_name)
                            .all())
    return render_template('maint.html', maint=maint)

@app.route('/cars', methods = ['GET'])  #SHOWS ALL CARS CURRENTLY FOR SALE
def cars():
    # car = Vehicle.query.filter_by(v_status="FOR SALE").all()
    car = Vehicle.query.all() #temp

    return render_template('viewcars.html', allCars=car)

@app.route('/cars/<string:vin>', methods = ['GET', 'POST'])  #Link to individually selected vehicle by VIN
def thisCar(vin):
    
    x=True
    car = Vehicle.query.filter_by(v_VIN=vin).first()
    salesperson = Salesperson.query.all()
    mechanic = Mechanic.query.all()
    
    part = Part.query.all()
    equipment = Equipment.query.all()
    
    serviceRecords = (Service.query.filter_by(sv_VIN=vin)
                                    .join(Mechanic, Mechanic.m_ID==Service.sv_mID)
                                    .join(Part, Part.p_partKey==Service.sv_partKey)
                                    .join(Equipment, Equipment.e_equipmentKey==Service.sv_equipmentKey)
                                    .add_columns(Service.sv_workOrderNo,Service.sv_date,Service.sv_serviceType,Service.sv_equipmentKey,
                                                 Service.sv_partQty,Service.sv_completed,Service.sv_partKey,
                                                 Mechanic.m_name, Part.p_partName, Equipment.e_name)
                                    .all())
    if (bool(Sales.query.filter_by(s_VIN=vin).first())):
        print("Sales Record Exists")
        sales = Sales.query.filter_by(s_VIN=vin).first()
        x = False    
        owner = Customer.query.filter_by(c_ID=sales.s_cID).first()
    elif (bool(Service.query.filter_by(sv_VIN=vin).first())):
        service = Service.query.filter_by(sv_VIN=vin).first()
        print("\n\n\t\tsvCID",service.sv_cID)
        print("Service Record Exists")
        
        x = False
        owner = Customer.query.filter_by(c_ID=service.sv_cID).first()
    
    else:
        owner = Customer.query.first()
        
    if(request.method == "POST"):
        servicesPerf = request.form.get('services')
        partNoUsedID = request.form.get('part')
        partQty = request.form.get('quantity')
        equipUsedID = request.form.get('equip')
        selectedMechID = request.form.get('mech')
        
        date = request.form.get('date')
        
        custName = request.form.get('custName')
        custPhone = request.form.get('custNo')
        salesPersID = request.form.get('sper')
        totalPrice = request.form.get('totalPrice')
        print(custName,custPhone,salesPersID,totalPrice, date, type(date))
        
    return render_template('selectedcar.html', thisCar=car, sper=salesperson, mech=mechanic, 
                                                carForSale=x, owner=owner, service=serviceRecords,
                                                part=part, equip=equipment)

@app.route("/admin")     #ADMIN PAGE
def admin():
    return redirect(url_for('admin.index'))

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