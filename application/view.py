from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Expense
from . import db

view = Blueprint('view', __name__)


@view.route('/')
def index():
    return redirect(url_for('auth.login'))


@view.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        user = current_user.id
        typ = request.form.get('type')
        paidto = request.form.get('paidto')
        amount = request.form.get('amount')
        mon = request.form.get('month')
        status = request.form.get('status')
        date = request.form.get('date')
        prev_bal = request.form.get('bal')
        new_expense = Expense(type=typ, paidto=paidto, amount=amount, mon=mon, status=status, transaction_date=date, prev_bal=prev_bal, user_id=user)
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense saved', category='success')
        return redirect(url_for('view.dashboard'))
    return render_template('dashboard.html', user=current_user)


@view.route('/details', methods=['GET', 'POST'])
@login_required
def details():
    user = current_user.id
    expenses = Expense.query.filter_by(user_id=user).all()
    return render_template('details.html', user=current_user, data=expenses)


@view.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    user = current_user.id
    expenses = Expense.query.filter_by(user_id=user).all()
    return render_template('manage.html', user=current_user, data=expenses)


@view.route('/delete', methods=['POST'])
@login_required
def delete():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        id = request.form.get('id')
        ex = Expense.query.get(id)
        db.session.delete(ex)
        db.session.commit()
        flash('Deleted', category='success')
        return manage()
    return render_template('manage.html', user=current_user, data=expenses)
