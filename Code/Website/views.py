from cgitb import reset
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
import json
views = Blueprint('views', __name__)
from . import db
from .models import Lot, Messages,Consignment
from datetime import datetime

@views.route('/')
def home():
    return redirect(url_for('auth.login'))

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@views.route('/dashboard.html')
def dashboard_html():
    return redirect(url_for('views.dashboard'))

@views.route('/login.html')
def login_html():
    return redirect(url_for('auth.login'))

@views.route('/lotcreation', methods=['POST','GET'])
@login_required
def lot_creation():
    if request.method == 'POST':
        destination = request.form.get('destination')
        plotid = request.form.get('plotId')
        packhouse = request.form.get('packHouse')
        qty = request.form.get('qty')
        packing = False
        new_lot = Lot(destination = destination, plotid = plotid, packhouse=packhouse, qty = qty, user_id=current_user.id, packing = packing, consignment=0)
        db.session.add(new_lot)
        db.session.commit()
        if new_lot:
            new_message = Messages(message=f'Lot Id {202203000 + new_lot.id} created.',user_id=current_user.id)
            db.session.add(new_message)
            db.session.commit()
            print(new_message.message)
            print(new_message.date)
            flash(f'Lot Created Successfully!!! Lot ID is {202203000 + new_lot.id}', category='success_lot')
    return render_template('lotcreation.html',user=current_user)

@views.route('lotcreation.html')
def lot_creation_html():
    return redirect(url_for('views.lot_creation'))

@views.route('/packingentry',methods=['POST','GET'])
@login_required
def packing_entry():
    if request.method == "POST":
        lotid = int(request.form.get('lotid')) - 202203000
        lotid = Lot.query.filter_by(id=str(lotid)).first()
        lotid.packing = True
        flash(f'Packing Details of Lot ID {202203000 + lotid.id} updated successfully!!!', category='success_packing')
        db.session.commit()
        new_message = Messages(message=f'Packing Details of Lot Id {202203000 + lotid.id} updated.',user_id=current_user.id)
        db.session.add(new_message)
        db.session.commit()
            


    return render_template('packingentry.html',user=current_user)


@views.route('packingentry.html')
def lot_packing_entry_html():
    return redirect(url_for('views.packing_entry'))

@views.route('/createconsignment',methods=['POST','GET'])
@login_required
def create_consignment():
    if request.form.get("btn")=="first":
        if request.method=="POST":
            country = request.form.get('country')
            packhouse = request.form.get('packhouse')
            return redirect(url_for('views.create_consignment_2',country=country,packhouse=packhouse))
    return render_template('createconsignment.html',user=current_user)

# def create_consignment_2(country,packhouse):
#     flash(f'{country}', category='create_consignment_country')
#     flash(f'{packhouse}', category='create_consignment_packhouse')
#     if request.form.get("btn_second")=="second":
#         if request.method=="POST":
#             print('Hello')
#             print(request.form.getlist('mycheckbox'))
#     return render_template('createconsignment2.html',user=current_user, country=country, packhouse=packhouse)



@views.route('createconsignment2',methods=['POST','GET'])
@login_required
def create_consignment_2():
    flash(f'{request.args["country"]}', category='create_consignment_country')
    flash(f'{request.args["packhouse"]}', category='create_consignment_packhouse')

    if request.method=="POST":
        lotid = request.form.getlist('mycheckbox')
        print(lotid)
        res=[]
        for i in lotid:
            res.append(Lot.query.filter_by(id=str(i)).first())
        for i in res:
            i.consignment=True
        new_consignment = Consignment(lot=res,user_id=current_user.id,pre=False,psc=False)
        db.session.add(new_consignment)
        db.session.commit()

        if new_consignment:
            for lot in new_consignment.lot:
                lot.consignment = True
                db.session.commit()
            for lot in new_consignment.lot:
                print(lot.consignment)
            new_message = Messages(message=f'Consignment ID {2203000 + new_consignment.id} created successfully.',user_id=current_user.id)
            db.session.add(new_message)
            db.session.commit()    
            flash(f'Consignment Created Successfully!!! Consignment ID is {2203000 + new_consignment.id}', category='success_consignment')
    return render_template('createconsignment2.html',user=current_user, country=request.args["country"], packhouse=request.args["packhouse"])

@views.route('createconsignment2.html')
def create_consignment_2_html():
    return redirect(url_for('views.create_consignment_2'))

@views.route('createconsignment.html')
def create_consignment_html():
    return redirect(url_for('views.create_consignment'))

@views.route('preclearanceinspection',methods=['POST','GET'])
@login_required
def pre_clearance_certificate():
    if request.method=="POST":
        consignment_id = int(request.form.get('mycheckbox1'))
        lab = request.form.get('lab')
        consign = Consignment.query.filter_by(id=str(consignment_id)).first()
        consign.pre=True
        db.session.commit()
        flash(f'Consignment ID {2203000 + consign.id} sent for Pre Clearance Inspection by IPQA jointly with JPQI', category='success_pre')
        new_message = Messages(message=f'Consignment ID {2203000 + consign.id} sent for Pre Clearance Inspection',user_id=current_user.id)
        db.session.add(new_message)
        db.session.commit()
        new_message = Messages(message=f'Pre Clearance Inspection of Consignment ID {2203000 + consign.id} Approved',user_id=current_user.id)
        db.session.add(new_message)
        db.session.commit()

    return render_template('cag.html',user=current_user)

@views.route('cag.html')
@login_required
def cag():
    return redirect(url_for('views.pre_clearance_certificate'))

@views.route('psc',methods=['POST','GET'])
@login_required
def psc():
    if request.method=="POST":
        consign_id = request.form.get('consignmentid')
        print(consign_id)
        consign = Consignment.query.filter_by(id=str(consign_id)).first()
        consign.psc = True
        db.session.commit()
        flash(f'Consignment ID {2203000 + consign.id} sent for Phytosanitory Certification', category='success_psc')
        new_message = Messages(message=f'Consignment ID {2203000 + consign.id} sent for Phytosanitary Certification',user_id=current_user.id)
        db.session.add(new_message)
        db.session.commit()
        new_message = Messages(message=f'Phytosanitary Certification of Consignment ID {2203000 + consign.id} Approved',user_id=current_user.id)
        db.session.add(new_message)
        db.session.commit()
    return render_template('psc.html',user=current_user)

@views.route('psc.html')
@login_required
def psc_html():
    return redirect(url_for('views.psc'))

@views.route('trackconsignment')
@login_required
def track_consignment():
    return render_template('trackconsignment.html',user=current_user)

@views.route('trackconsignment.html')
@login_required
def track_consignment_html():
    return redirect(url_for('views.track_consignment'))