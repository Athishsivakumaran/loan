from .database import db


class Employee(db.Model):
    __tablename__='employee'
    emp_id = db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    emp_name = db.Column(db.String,nullable=False,unique=True)
    emp_pass = db.Column(db.String,unique=True,nullable=False)
    emp_Photo = db.Column(db.BLOB,nullable=False)
    borrowers=db.relationship('Borrowers',backref="employee",lazy='subquery')
    payees=db.relationship('Payment',backref="employee",lazy='subquery')

class Account_holders(db.Model):
    __tablename__='account_holders'
    accno = db.Column(db.Integer,primary_key=True)
    accname = db.Column(db.String,nullable=False)
    ph_no = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String,nullable=False)


class LO_TY(db.Model):
    __tablename__ = 'lo_ty'
    loty_id= db.Column(db.Integer, primary_key=True)
    loty_name = db.Column(db.String, nullable=False,unique=True)
    desc = db.Column(db.String, nullable=False)
    int_rate = db.Column(db.REAL, nullable=False)
    penalty_rate=db.Column(db.REAL, nullable=False)
    maxloan_amt = db.Column(db.Integer, nullable=False)


class LO_PL(db.Model):
    __tablename__ = 'lo_pl'
    lopl_id= db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.String, nullable=False)


class Borrowers(db.Model):
    __tablename__ = 'Borrowers'
    reference_id= db.Column(db.Integer, primary_key=True)
    bor_id =db.Column(db.Integer,db.ForeignKey('account_holders.accno'))
    bor_type = db.Column(db.String, nullable=False)
    bor_plan = db.Column(db.String, nullable=False)
    bor_int_rate = db.Column(db.REAL, nullable=False)
    bor_amt = db.Column(db.Integer, nullable=False)
    bor_tot_amt=db.Column(db.Integer, nullable=False)
    bor_mon_amt=db.Column(db.Integer, nullable=False)
    rem_amt=db.Column(db.Integer,nullable=False)
    loan_date=db.Column(db.String, nullable=False)
    amt_paid=db.Column(db.String, nullable=False)
    loan_mat_date=db.Column(db.String,nullable=False)
    purpose=db.Column(db.String,nullable=False)
    emp_id=db.Column(db.Integer,db.ForeignKey('employee.emp_id'))
    payments=db.relationship('Payment',backref="borrower",lazy='subquery', cascade='all, delete')


class Payment(db.Model):
    __tablename__='payment'
    payment_id=db.Column(db.Integer,primary_key=True)
    payee_id=db.Column(db.Integer,db.ForeignKey('account_holders.accno'),nullable=False)
    loan_id=db.Column(db.Integer,db.ForeignKey('Borrowers.reference_id'),nullable=False)
    payee_amt=db.Column(db.Integer, nullable=False)
    payment_date=db.Column(db.String, nullable=False)
    emp_id=db.Column(db.Integer,db.ForeignKey('employee.emp_id'),nullable=False)
