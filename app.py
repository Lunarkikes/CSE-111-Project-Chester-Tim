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
from flask_admin.menu import MenuLink
from sqlalchemy import func

import pandas as pd

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
    v_year = db.Column(db.Integer, unique = False)
    v_make = db.Column(db.String, unique = False) 
    v_model = db.Column(db.String, unique = False)
    v_trim = db.Column(db.Integer, unique = False)
    v_color = db.Column(db.Integer, nullable = True, unique = False)
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
    
class CarOwner(db.Model):
    co_ID = db.Column(db.Integer, primary_key = True)
    co_VIN = db.Column(db.String, unique = False)
    co_cID = db.Column(db.Integer, unique = False)
    
class AdminModelView(ModelView):

    column_searchable_list = ['v_VIN','v_year','v_make','v_model','v_trim','v_color','v_MSRP','v_status']
    
    column_filters = ['v_VIN','v_year','v_make','v_model','v_trim','v_color','v_MSRP','v_status']
    page_size = 50




admin.add_view(AdminModelView(Vehicle, db.session))

admin.add_view(ModelView(Salesperson, db.session))
admin.add_view(ModelView(Mechanic, db.session))
admin.add_view(ModelView(Customer, db.session))

admin.add_view(ModelView(Sales, db.session))
admin.add_view(ModelView(Service, db.session))
admin.add_view(ModelView(Part, db.session))
admin.add_view(ModelView(Equipment, db.session))
admin.add_view(ModelView(CarOwner, db.session))

admin.add_link(MenuLink(name='Main Page', category='', url='/'))

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

@app.route('/sales', methods = ['GET', 'POST'])
def sales():
    if request.method == 'GET':
        sales = (Sales.query.outerjoin(Salesperson, Salesperson.sp_ID==Sales.s_spID)
                            .outerjoin(Customer, Customer.c_ID==Sales.s_cID)
                            .outerjoin(Vehicle, Vehicle.v_VIN==Sales.s_VIN)
                            .add_columns(Salesperson.sp_name, Customer.c_name,Sales.s_invoiceNo,Sales.s_date,
                                        Sales.s_VIN,Sales.s_spID,Sales.s_cID,Sales.s_MSRP,Sales.s_totalCost,
                                        Vehicle.v_year,Vehicle.v_make,Vehicle.v_model,Vehicle.v_VIN)
                            .all())
        return render_template('sales.html', sales=sales)
    if request.method == 'POST':
        vin = request.form['vinS']
        vin = vin.upper()
        sale = (Sales.query.outerjoin(Salesperson, Salesperson.sp_ID==Sales.s_spID)
                        .outerjoin(Customer, Customer.c_ID==Sales.s_cID)
                        .outerjoin(Vehicle, Vehicle.v_VIN==Sales.s_VIN)
                        .add_columns(Salesperson.sp_name, Customer.c_name,Sales.s_invoiceNo,Sales.s_date,
                                        Sales.s_VIN,Sales.s_spID,Sales.s_cID,Sales.s_MSRP,Sales.s_totalCost,
                                         Vehicle.v_year,Vehicle.v_make,Vehicle.v_model,Vehicle.v_VIN).filter(Sales.s_VIN.like("%"+vin+"%")))
        counter = 0
        for x in sale:
            counter += 1
        if counter != 0:
            return render_template('sales.html', sales=sale)
        else:
            sales = (Sales.query.outerjoin(Salesperson, Salesperson.sp_ID == Sales.s_spID)
                     .outerjoin(Customer, Customer.c_ID == Sales.s_cID)
                     .outerjoin(Vehicle, Vehicle.v_VIN == Sales.s_VIN)
                     .add_columns(Salesperson.sp_name, Customer.c_name, Sales.s_invoiceNo, Sales.s_date,
                                  Sales.s_VIN, Sales.s_spID, Sales.s_cID, Sales.s_MSRP, Sales.s_totalCost,
                                  Vehicle.v_year, Vehicle.v_make, Vehicle.v_model,Vehicle.v_VIN)
                     .all())
            return render_template('sales.html', sales=sales)

@app.route('/sales1', methods = ['GET', 'POST'])
def sales1():
    Svin = request.form['v1']
    sale = (Sales.query.join(Salesperson, Salesperson.sp_ID == Sales.s_spID)
            .join(Customer, Customer.c_ID == Sales.s_cID)
            .join(Vehicle, Vehicle.v_VIN == Sales.s_VIN)
            .add_columns(Salesperson.sp_name, Customer.c_name, Sales.s_invoiceNo, Sales.s_date,
                         Sales.s_VIN, Sales.s_spID, Sales.s_cID, Sales.s_MSRP, Sales.s_totalCost,
                         Vehicle.v_year, Vehicle.v_make, Vehicle.v_model).filter(Sales.s_invoiceNo.like("%" + Svin + "%")))

    counter = 0
    for x in sale:
        counter += 1
    if counter > 0:
        return render_template('sales.html', sales=sale)
    else:
        sales = (Sales.query.join(Salesperson, Salesperson.sp_ID == Sales.s_spID)
                 .join(Customer, Customer.c_ID == Sales.s_cID)
                 .join(Vehicle, Vehicle.v_VIN == Sales.s_VIN)
                 .add_columns(Salesperson.sp_name, Customer.c_name, Sales.s_invoiceNo, Sales.s_date,
                              Sales.s_VIN, Sales.s_spID, Sales.s_cID, Sales.s_MSRP, Sales.s_totalCost,
                              Vehicle.v_year, Vehicle.v_make, Vehicle.v_model)
                 .all())
        return render_template('sales.html', sales=sales)

@app.route('/sales2', methods = ['GET', 'POST'])
def sales2():
    Svin = request.form['v2']
    sale = (Sales.query.join(Salesperson, Salesperson.sp_ID == Sales.s_spID)
            .join(Customer, Customer.c_ID == Sales.s_cID)
            .join(Vehicle, Vehicle.v_VIN == Sales.s_VIN)
            .add_columns(Salesperson.sp_name, Customer.c_name, Sales.s_invoiceNo, Sales.s_date,
                         Sales.s_VIN, Sales.s_spID, Sales.s_cID, Sales.s_MSRP, Sales.s_totalCost,
                         Vehicle.v_year, Vehicle.v_make, Vehicle.v_model).filter(Sales.s_date.like("%" + Svin + "%")))

    counter = 0
    for x in sale:
        counter += 1
    if counter > 0:
        return render_template('sales.html', sales=sale)
    else:
        sales = (Sales.query.join(Salesperson, Salesperson.sp_ID == Sales.s_spID)
                 .join(Customer, Customer.c_ID == Sales.s_cID)
                 .join(Vehicle, Vehicle.v_VIN == Sales.s_VIN)
                 .add_columns(Salesperson.sp_name, Customer.c_name, Sales.s_invoiceNo, Sales.s_date,
                              Sales.s_VIN, Sales.s_spID, Sales.s_cID, Sales.s_MSRP, Sales.s_totalCost,
                              Vehicle.v_year, Vehicle.v_make, Vehicle.v_model)
                 .all())
        return render_template('sales.html', sales=sales)
    
@app.route('/sales3', methods = ['GET', 'POST'])
def sales3():
    Svin = request.form['v3']
    sale = (Sales.query.join(Salesperson, Salesperson.sp_ID == Sales.s_spID)
            .join(Customer, Customer.c_ID == Sales.s_cID)
            .join(Vehicle, Vehicle.v_VIN == Sales.s_VIN)
            .add_columns(Salesperson.sp_name, Customer.c_name, Sales.s_invoiceNo, Sales.s_date,
                         Sales.s_VIN, Sales.s_spID, Sales.s_cID, Sales.s_MSRP, Sales.s_totalCost,
                         Vehicle.v_year, Vehicle.v_make, Vehicle.v_model).filter(Salesperson.sp_name.like("%" + Svin + "%")))

    counter = 0
    for x in sale:
        counter += 1
    if counter > 0:
        return render_template('sales.html', sales=sale)
    else:
        sales = (Sales.query.join(Salesperson, Salesperson.sp_ID == Sales.s_spID)
                 .join(Customer, Customer.c_ID == Sales.s_cID)
                 .join(Vehicle, Vehicle.v_VIN == Sales.s_VIN)
                 .add_columns(Salesperson.sp_name, Customer.c_name, Sales.s_invoiceNo, Sales.s_date,
                              Sales.s_VIN, Sales.s_spID, Sales.s_cID, Sales.s_MSRP, Sales.s_totalCost,
                              Vehicle.v_year, Vehicle.v_make, Vehicle.v_model)
                 .all())
        return render_template('sales.html', sales=sales)

@app.route('/sales4', methods = ['GET', 'POST'])
def sales4():
    Svin = request.form['v4']
    sale = (Sales.query.join(Salesperson, Salesperson.sp_ID == Sales.s_spID)
            .join(Customer, Customer.c_ID == Sales.s_cID)
            .join(Vehicle, Vehicle.v_VIN == Sales.s_VIN)
            .add_columns(Salesperson.sp_name, Customer.c_name, Sales.s_invoiceNo, Sales.s_date,
                         Sales.s_VIN, Sales.s_spID, Sales.s_cID, Sales.s_MSRP, Sales.s_totalCost,
                         Vehicle.v_year, Vehicle.v_make, Vehicle.v_model).filter(Customer.c_name.like("%" + Svin + "%")))

    counter = 0
    for x in sale:
        counter += 1
    if counter > 0:
        return render_template('sales.html', sales=sale)
    else:
        sales = (Sales.query.join(Salesperson, Salesperson.sp_ID == Sales.s_spID)
                 .join(Customer, Customer.c_ID == Sales.s_cID)
                 .join(Vehicle, Vehicle.v_VIN == Sales.s_VIN)
                 .add_columns(Salesperson.sp_name, Customer.c_name, Sales.s_invoiceNo, Sales.s_date,
                              Sales.s_VIN, Sales.s_spID, Sales.s_cID, Sales.s_MSRP, Sales.s_totalCost,
                              Vehicle.v_year, Vehicle.v_make, Vehicle.v_model)
                 .all())
        return render_template('sales.html', sales=sales)


@app.route('/sales5', methods=['GET', 'POST'])
def sales5():
    Svin = request.form['v5']
    sale = (Sales.query.join(Salesperson, Salesperson.sp_ID == Sales.s_spID)
            .join(Customer, Customer.c_ID == Sales.s_cID)
            .join(Vehicle, Vehicle.v_VIN == Sales.s_VIN)
            .add_columns(Salesperson.sp_name, Customer.c_name, Sales.s_invoiceNo, Sales.s_date,
                         Sales.s_VIN, Sales.s_spID, Sales.s_cID, Sales.s_MSRP, Sales.s_totalCost,
                         Vehicle.v_year, Vehicle.v_make, Vehicle.v_model).filter(Sales.s_MSRP.like("%" + Svin + "%")))

    counter = 0
    for x in sale:
        counter += 1
    if counter > 0:
        return render_template('sales.html', sales=sale)
    else:
        sales = (Sales.query.join(Salesperson, Salesperson.sp_ID == Sales.s_spID)
                 .join(Customer, Customer.c_ID == Sales.s_cID)
                 .join(Vehicle, Vehicle.v_VIN == Sales.s_VIN)
                 .add_columns(Salesperson.sp_name, Customer.c_name, Sales.s_invoiceNo, Sales.s_date,
                              Sales.s_VIN, Sales.s_spID, Sales.s_cID, Sales.s_MSRP, Sales.s_totalCost,
                              Vehicle.v_year, Vehicle.v_make, Vehicle.v_model)
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
    return render_template('maint2.html', maint=maint)

@app.route('/maint1', methods = ['GET', 'POST'])
def maint1Search():
    Svin = request.form['S1']

    main = Service.query.filter(Service.sv_workOrderNo.like("%"+Svin+"%")).all()

    counter = 0
    for x in main:
        counter += 1
    if counter != 0:
        return render_template('maint.html', allCars=main)
    else:
        maint = (Service.query.all())
        return render_template('maint.html', maint=maint)

@app.route('/maint2', methods = ['GET', 'POST'])
def maint2Search():
    Svin = request.form['S2']

    main = Service.query.filter_by(sv_serviceType=Svin).all()

    counter = 0
    for x in main:
        counter += 1
    if counter != 0:
        return render_template('maint.html', maint=main)
    else:
        maint = (Service.query.all())
        return render_template('maint.html', maint=maint)

@app.route('/maint3', methods = ['GET', 'POST'])
def maint3Search():
    Svin = request.form['S3']

    main = Service.query.filter(Service.sv_date.like("%"+Svin+"%")).all()

    counter = 0
    for x in main:
        counter += 1
    if counter != 0:
        return render_template('maint.html', maint=main)
    else:
        maint = (Service.query.all())
        return render_template('maint.html', maint=maint)

@app.route('/maint4', methods = ['GET', 'POST'])
def maint4Search():
    Svin = request.form['S4']
    Svin = Svin.upper()
    main = Service.query.filter(Service.sv_VIN.like(Svin)).all()

    counter = 0
    for x in main:
        counter += 1
    if counter > 0:
        return render_template('maint.html', maint=main)
    else:
        maint = (Service.query.all())
        return render_template('maint.html', maint=maint)

@app.route('/maint5', methods = ['GET', 'POST'])
def maint5Search():
    Svin = request.form['S5']
    main = Service.query.filter(Service.sv_partKey.like("%"+Svin+"%")).all()

    counter = 0
    for x in main:
        counter += 1
    if counter != 0:
        return render_template('maint.html', maint=main)
    else:
        maint = (Service.query.all())
        return render_template('maint.html', maint=maint)

@app.route('/maint6', methods = ['GET', 'POST'])
def maint6Search():
    Svin = request.form['S6']
    main = Service.query.filter(Service.sv_equipmentKey.like("%"+Svin+"%")).all()

    counter = 0
    for x in main:
        counter += 1
    if counter != 0:
        return render_template('maint.html', maint=main)
    else:
        maint = (Service.query.all())
        return render_template('maint.html', maint=maint)

@app.route('/maint7', methods = ['GET', 'POST'])
def maint7Search():
    Svin = request.form['S7']
    main = Service.query.filter(Service.sv_cID.like("%"+Svin+"%")).all()

    counter = 0
    for x in main:
        counter += 1
    if counter != 0:
        return render_template('maint.html', maint=main)
    else:
        maint = (Service.query.all())
        return render_template('maint.html', maint=maint)

@app.route('/maint8', methods = ['GET', 'POST'])
def maint8Search():
    Svin = request.form['S8']
    main = Service.query.filter(Service.sv_mID.like("%"+Svin+"%")).all()

    counter = 0
    for x in main:
        return render_template('maint.html', maint=main)
    else:
        maint = (Service.query.all())
        return render_template('maint.html', maint=maint)

@app.route('/maint9', methods = ['GET', 'POST'])
def maint9Search():
    Svin = request.form['S9']
    main = Service.query.filter(Service.sv_partCost.like("%"+Svin+"%")).all()

    counter = 0
    for x in main:
        counter += 1
    for x in main:
        return render_template('maint.html', maint=main)
    else:
        maint = (Service.query.all())
        return render_template('maint.html', maint=maint)

@app.route('/maint10', methods = ['GET', 'POST'])
def maint10Search():
    Svin = request.form['S10']
    main = Service.query.filter(Service.sv_partQty.like("%"+Svin+"%")).all()

    counter = 0
    for x in main:
        return render_template('maint.html', maint=main)
    else:
        maint = (Service.query.all())
        return render_template('maint.html', maint=maint)

@app.route('/maint11', methods = ['GET', 'POST'])
def maint11Search():
    Svin = request.form['S11']
    main = Service.query.filter(Service.sv_completed.like("%"+Svin+"%")).all()
    counter = 0
    for x in main:
        counter += 1
    if counter != 0:
        return render_template('maint.html', maint=main)
    else:
        maint = (Service.query.all())
        return render_template('maint.html', maint=maint)

@app.route('/cars', methods = ['GET', 'POST'])  #SHOWS ALL CARS CURRENTLY FOR SALE
def cars():
    if request.form.get('action1') == 'All Vehicles':
        car = Vehicle.query.all() #temp
    elif  request.form.get('action2') == 'Cars For Sale':
        car = Vehicle.query.filter_by(v_status="FOR SALE").all()
    elif  request.form.get('action3') == 'Cars In Repair':
        car = Vehicle.query.filter_by(v_status="FOR REPAIR").all()
    elif  request.form.get('action4') == 'Cars Sold':
        car = Vehicle.query.filter_by(v_status="SOLD").all()
    else:
        car = Vehicle.query.all()
    return render_template('viewcars.html', allCars=car)

@app.route('/car', methods = ['GET', 'POST'])  #SEARCHES FOR CARS
def searchCars():
    vin = request.form['vin']
    vin = vin.upper()
    carsearch = Vehicle.query.filter(Vehicle.v_VIN.like("%"+vin+"%")).all() #temp
    count = 0
    for x in carsearch:
        count += 1
    if count != 0:
        return render_template('viewcars.html', allCars=carsearch)
    else:
        car = Vehicle.query.all()  # temp
        return render_template('viewcars.html', allCars=car)


@app.route('/car1', methods = ['GET', 'POST'])  #SEARCHES FOR CARS
def searchCars1():
    vin = request.form['c1']
    vin = vin.upper()
    carsearch = Vehicle.query.filter(Vehicle.v_color.like("%"+vin+"%")).all() #temp
    count = 0
    for x in carsearch:
        count += 1
    if count != 0:
        return render_template('viewcars.html', allCars=carsearch)
    else:
        car = Vehicle.query.all()  # temp
        return render_template('viewcars.html', allCars=car)

@app.route('/car2', methods = ['GET', 'POST'])  #SEARCHES FOR CARS
def searchCars2():
    vin = request.form['c2']
    vin = vin.upper()
    carsearch = Vehicle.query.filter(Vehicle.v_year.like("%"+vin+"%")).all() #temp
    count = 0
    for x in carsearch:
        count += 1
    if count != 0:
        return render_template('viewcars.html', allCars=carsearch)
    else:
        car = Vehicle.query.all()  # temp
        return render_template('viewcars.html', allCars=car)

@app.route('/car3', methods = ['GET', 'POST'])  #SEARCHES FOR CARS
def searchCars3():
    vin = request.form['c3']
    vin = vin.upper()
    carsearch = Vehicle.query.filter(Vehicle.v_make.like("%"+vin+"%")).all() #temp
    count = 0
    for x in carsearch:
        count += 1
    if count != 0:
        return render_template('viewcars.html', allCars=carsearch)
    else:
        car = Vehicle.query.all()  # temp
        return render_template('viewcars.html', allCars=car)

@app.route('/car4', methods = ['GET', 'POST'])  #SEARCHES FOR CARS
def searchCars4():
    vin = request.form['c4']
    vin = vin.upper()
    carsearch = Vehicle.query.filter(Vehicle.v_model.like("%"+vin+"%")).all() #temp
    count = 0
    for x in carsearch:
        count += 1
    if count != 0:
        return render_template('viewcars.html', allCars=carsearch)
    else:
        car = Vehicle.query.all()  # temp
        return render_template('viewcars.html', allCars=car)

@app.route('/car5', methods = ['GET', 'POST'])  #SEARCHES FOR CARS
def searchCars5():
    vin = request.form['c5']
    vin = vin.upper()
    carsearch = Vehicle.query.filter(Vehicle.v_trim.like("%"+vin+"%")).all() #temp
    count = 0
    for x in carsearch:
        count += 1
    if count != 0:
        return render_template('viewcars.html', allCars=carsearch)
    else:
        car = Vehicle.query.all()  # temp
        return render_template('viewcars.html', allCars=car)

@app.route('/car6', methods = ['GET', 'POST'])  #SEARCHES FOR CARS
def searchCars6():
    vin = request.form['c6']
    vin = vin.upper()
    carsearch = Vehicle.query.filter(Vehicle.v_MSRP.like("%"+vin+"%")).all() #temp
    count = 0
    for x in carsearch:
        count += 1
    if count != 0:
        return render_template('viewcars.html', allCars=carsearch)
    else:
        car = Vehicle.query.all()  # temp
        return render_template('viewcars.html', allCars=car)

@app.route('/cars/<string:vin>/<int:button>', methods = ['GET', 'POST'])  #Link to individually selected vehicle by VIN
def thisCar(vin,button):
    if request.form.get('action0') == 'DONE':
        workNo = request.form.get("workNo")
        workOrder = Service.query.filter_by(sv_workOrderNo=workNo).first()
        workOrder.sv_completed = True
        db.session.commit()
    x=True
    car = Vehicle.query.filter_by(v_VIN=vin).first()
    salesperson = Salesperson.query.all()
    mechanic = Mechanic.query.all()
    
    part = Part.query.all()
    equipment = Equipment.query.all()
    
    serviceRecords = (Service.query.filter_by(sv_VIN=vin)
                                    .outerjoin(Mechanic, Mechanic.m_ID==Service.sv_mID)
                                    .outerjoin(Part, Part.p_partKey==Service.sv_partKey)
                                    .outerjoin(Equipment, Equipment.e_equipmentKey==Service.sv_equipmentKey)
                                    .add_columns(Service.sv_workOrderNo,Service.sv_date,Service.sv_serviceType,Service.sv_equipmentKey,
                                                 Service.sv_partQty,Service.sv_completed,Service.sv_partKey,Service.sv_partCost,
                                                 Mechanic.m_name, Part.p_partName, Equipment.e_name)
                                    .all())
    sum = Service.query.with_entities(func.sum(Service.sv_partCost)).filter_by(sv_VIN=vin).first()
    if (bool(Sales.query.filter_by(s_VIN=vin).first())):
        print("Sales Record Exists")
        sales = Sales.query.filter_by(s_VIN=vin).first()
        x = False    
        owner = Customer.query.filter_by(c_ID=sales.s_cID).first()
    elif(bool(Service.query.filter_by(sv_VIN=vin).first())):
        service = Service.query.filter_by(sv_VIN=vin).first()
        print("\n\n\t\tsvCID",service.sv_cID)
        print("Service Record Exists")
        
        x = False
        owner = Customer.query.filter_by(c_ID=service.sv_cID).first()
    
    elif(bool(CarOwner.query.filter_by(co_VIN=vin).first())):
        x = False
        cowner = CarOwner.query.filter_by(co_VIN=vin).first()
        owner = Customer.query.filter_by(c_ID=cowner.co_cID).first()
        print("in else",owner.c_name)
    else:
        owner = Customer.query.first()
    if(request.method == "POST"):
        date = request.form.get('date')
        if (button==1):
            custName = request.form.get('custName')
            custPhone = request.form.get('custNo')
            salesPersID = request.form.get('sper')
            totalPrice = request.form.get('totalPrice')
            newCustomer = Customer(c_name=custName, c_phone=custPhone)
            db.session.add(newCustomer)
            db.session.commit()
            newCustomerID = Customer.query.filter_by(c_name=custName).first()
            newSale = Sales(s_date=date, s_VIN=vin, s_spID=salesPersID, s_cID=newCustomerID.c_ID, s_MSRP=car.v_MSRP, s_totalCost=totalPrice)
            db.session.add(newSale)
            car.v_status = 'SOLD' 
            db.session.commit()
            return redirect(url_for('sales'))
               
        elif (button==2):
            servicesPerf = request.form.get('services')
            partNoUsedID = request.form.get('part')
            partQty = request.form.get('quantity')
            equipUsedID = request.form.get('equip')
            selectedMechID = request.form.get('mech')
            partCost = Part.query.filter_by(p_partKey=partNoUsedID).first()
            newService = Service(sv_serviceType=servicesPerf,sv_date=date,sv_VIN=vin,sv_partKey=partNoUsedID,
                                 sv_equipmentKey=equipUsedID,sv_mID=selectedMechID,sv_partCost=partCost.p_partCost,sv_partQty=partQty,sv_completed=False)
            db.session.add(newService)
            car.v_status = 'FOR REPAIR'
            db.session.commit()
            return redirect(url_for('thisCar', vin=vin, button='0'))
    return render_template('selectedcar.html', thisCar=car, sper=salesperson, mech=mechanic, 
                                                carForSale=x, owner=owner, service=serviceRecords,
                                                part=part, equip=equipment, sum=sum)

@app.route("/new", methods = ['GET', 'POST'])   
def newCustCar():
    if request.method == 'POST':
        vin = request.form.get('newVIN')
        newyear = request.form.get('newyear')
        newmake = request.form.get('newmake')
        newmodel = request.form.get('newmodel')
        newCustName = request.form.get('newCustName')
        newCustPhone = request.form.get('newCustPhone')
        newCustomer = Customer(c_name=newCustName, c_phone=newCustPhone)
        newCar = Vehicle(v_VIN=vin, v_year=newyear,v_make=newmake,v_model=newmodel,v_color='Null',v_status='FOR REPAIR')
        db.session.add(newCustomer)
        db.session.add(newCar)
        db.session.commit()
        custID = Customer.query.filter_by(c_name=newCustName).first()
        newRelation = CarOwner(co_VIN=vin, co_cID=custID.c_ID)
        db.session.add(newRelation)
        db.session.commit()
        # return redirect(url_for('cars', sort=1))
        return redirect(url_for('thisCar', vin=vin, button='0'))
    return redirect(url_for('cars', sort=1))

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
    # admin = create_admin(app=app)
    # configure_admin(app, admin)