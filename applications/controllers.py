from flask import Flask,request,redirect,url_for
from flask import render_template
from applications.models import *
from flask import current_app as app
from sqlalchemy.sql import text
from datetime import date,timedelta
name=""
log=""

@app.route("/", methods=["GET", "POST"])
def a1():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        global name,log
        name=request.form["name"]
        pass_word=request.form["password"]
        log=Employee.query.filter_by(emp_name=name).first()
        db.session.execute(text('''DROP VIEW IF EXISTS boremp'''))
        db.session.commit()
        db.session.execute(text('''create view boremp as select * from borrowers where emp_id={id}'''.format(id=log.emp_id)))
        db.session.commit()
        if log.emp_name == name and log.emp_pass == pass_word:
            with open('D:\CIT\FAR(SEM 4 project)\static\img\emp.jpeg',"wb") as f:f.write(log.emp_Photo)
            return redirect(url_for('a2'))
        else:
            return render_template("404.html")



@app.route("/home", methods=["GET", "POST"])
def a2():
    if request.method == "GET":
        return render_template("home.html",emp=name.capitalize(),
                               Nob=(a1:=len([i for i in Borrowers.query.all()])),
                               loc=(b1:=len([i for i in Borrowers.query.filter_by(rem_amt=0)])),
                               louc=a1-b1,
                               Noc=len([i for i in Account_holders.query.all()]),
                               loans=[[i[0],0 if i[1] is None else i[1]] for i in db.session.execute(
                                   text('''select lt.loty_name,bu.count from lo_ty as lt left outer join
                                (select loty_name ,count(loty_name) as count from lo_ty as lt JOIN 
                                Borrowers as br on br.bor_type=lt.loty_name group by (loty_name))
                                as bu on lt.loty_name=bu.loty_name'''))])



@app.route("/loans", methods=["GET", "POST"])
def a3():
    if request.method == "GET":
        return render_template("loans.html",emp=name.capitalize(),
                               bors=[i.accno for i in Account_holders.query.all()],
                               loty=[i.loty_name for i in LO_TY.query.all()] ,
                               lopl=[i.duration for i in LO_PL.query.all()],
                                borrow = [i for i in db.session.execute(text('''Select * from boremp as br inner join account_holders as ac on br.bor_id=ac.accno''')).all()])


    elif request.method=="POST":
        db.session.add(Borrowers(bor_id=request.form["br"],bor_type=(r1:=request.form["lt"]),
                              bor_plan=(r3:=request.form["lp"]),bor_int_rate=(r:=LO_TY.query.filter_by(loty_name=r1).first().int_rate),
                              bor_amt=(r2:=int(request.form["amt"])),bor_tot_amt=round(ta:=r2+r2*r/100),bor_mon_amt=round(ta/((c1:=int(r3.split(" ")[0]))*12)),
                              loan_date=date.today().strftime("%b %d, %Y"),loan_mat_date=(date.today()+timedelta(days=c1*365)).strftime("%b %d, %Y"),
                              purpose=request.form["pur"],emp_id=log.emp_id,rem_amt=round(ta),amt_paid=0))
        db.session.commit()
        return render_template("loans.html", emp=name.capitalize(),
                               bors=[i.accno for i in Account_holders.query.all()],
                               loty=[i.loty_name for i in LO_TY.query.all()],
                               lopl=[i.duration for i in LO_PL.query.all()],
                               borrow=[i for i in db.session.execute(text('''Select * from boremp as br inner join account_holders as ac on br.bor_id=ac.accno''')).all()])


@app.route("/payments", methods=["GET", "POST"])
def a4():
    if request.method == "GET":
        return render_template("payments.html", emp=name.capitalize(),payees=[i for i in Payment.query.filter_by(emp_id=log.emp_id)],lr=[i.reference_id for i in db.session.execute(text('''Select * from boremp''')).all()])
    elif request.method == "POST":
        db.session.add(Payment(loan_id=(id1:=request.form["lb"]),payee_id=Borrowers.query.filter_by(reference_id=id1).first().bor_id,
                        payee_amt=(amt:=int(request.form["amount"])),payment_date=date.today().strftime("%b %d, %Y"),employee=log))
        db.session.commit()
        b1=Borrowers.query.filter_by(reference_id=id1).first()
        b1.rem_amt-=amt
        b1.amt_paid+=amt
        db.session.commit()
        return render_template("payments.html", emp=name.capitalize(),payees=[i for i in Payment.query.filter_by(emp_id=log.emp_id)],lr=[i.reference_id for i in Borrowers.query.all()])



@app.route("/borrowers", methods=["GET", "POST"])
def a5():
    if request.method == "GET":
        return render_template("customers.html", emp=name.capitalize(),borrows=[i for i in db.session.execute(text('''Select bor_id,count(bor_id) as count,accname,ph_no,address from boremp as br inner join account_holders as ac on br.bor_id=ac.accno group by bor_id'''))]
                               ,loans=[i for i in Borrowers.query.filter_by(emp_id=log.emp_id).all()])


@app.route("/loantypes", methods=["GET", "POST"])
def a6():
    if request.method == "GET":
        return render_template("loantypes.html", emp=name.capitalize(),loantypes=[i for i in LO_TY.query.all()])
    elif request.method=="POST":
        db.session.add(LO_TY(loty_name=request.form["l_name"],desc=request.form["l_desc"],int_rate=request.form["l_int_rate"]
                             ,maxloan_amt=request.form["max_amt"]))
        db.session.commit()
        return render_template("loantypes.html", emp=name.capitalize(),loantypes=[i for i in LO_TY.query.all()])


@app.route("/loanplans", methods=["GET", "POST"])
def a7():
    if request.method == "GET":
        return render_template("loanplans.html", emp=name.capitalize(),loanplans=[i for i in LO_PL.query.all()])
    elif request.method=="POST":
        db.session.add(LO_PL(duration=request.form["duration"]+" "+"yrs" ))
        db.session.commit()
        return render_template("loanplans.html", emp=name.capitalize(),loanplans=[i for i in LO_PL.query.all()])




@app.route("/borrowers/<int:bor_pay_id>", methods=["GET", "POST"])
def a8(bor_pay_id):
    if request.method == "GET":
        return render_template("payments_bor.html", emp=name.capitalize(),payments=[i for i in Payment.query.filter_by(loan_id=bor_pay_id).all()])




@app.route("/loans/<int:delete_id>/delete", methods=["GET", "POST"])
def a9(delete_id):
    if request.method == "GET":
        db.session.delete(Borrowers.query.filter_by(reference_id=delete_id).first())
        db.session.commit()
        return render_template("loans.html", emp=name.capitalize(),
                                bors=[i.accno for i in Account_holders.query.all()],
                               loty=[i.loty_name for i in LO_TY.query.all()],
                               lopl=[i.duration for i in LO_PL.query.all()],
                               borrow=[i for i in db.session.execute(text('''Select * from boremp as br inner join account_holders as ac on br.bor_id=ac.accno''')).all()])





@app.route("/payments/<int:delete_id>/delete", methods=["GET", "POST"])
def a10(delete_id):
    if request.method == "GET":
        db.session.delete(Payment.query.filter_by(payment_id=delete_id).first())
        db.session.commit()
        return render_template("payments.html", emp=name.capitalize(), payees=[i for i in Payment.query.filter_by(emp_id=log.emp_id)],
                               lr=[i.reference_id for i in db.session.execute(text('''select * from boremp'''))])





@app.route("/loanplans/<int:delete_id>/delete", methods=["GET", "POST"])
def a11(delete_id):
    if request.method == "GET":
        db.session.delete(LO_PL.query.filter_by(lopl_id=delete_id).first())
        db.session.commit()
        return render_template("loanplans.html",emp=name.capitalize(), loanplans=[i for i in LO_PL.query.all()])




@app.route("/loantypes/<int:delete_id>/delete", methods=["GET", "POST"])
def a12(delete_id):
    if request.method == "GET":
        db.session.delete(LO_TY.query.filter_by(loty_id=delete_id).first())
        db.session.commit()
        return render_template("loantypes.html", emp=name.capitalize(), loantypes=[i for i in LO_TY.query.all()])