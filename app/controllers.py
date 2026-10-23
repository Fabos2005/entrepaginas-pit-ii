"""Controladores HTTP: autenticação, coordenação do modelo e renderização."""
import secrets
import sqlite3
from functools import wraps
from datetime import date, timedelta
from flask import Blueprint, current_app, request, session, redirect, url_for, render_template, flash
from . import models
bp=Blueprint('web',__name__)

def login_required(view):
    @wraps(view)
    def wrapped(*args,**kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('web.login'))
        return view(*args,**kwargs)
    return wrapped

@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        if secrets.compare_digest(request.form.get('password','').encode(),current_app.config['ADMIN_PASSWORD'].encode()):
            session.clear()
            session.update(authenticated=True,csrf=secrets.token_hex(32))
            session.permanent=True
            return redirect(url_for('web.index'))
        flash('Senha incorreta. Confira e tente novamente.','error')
    return render_template('login.html')

@bp.post('/logout')
def logout():
    session.clear()
    return redirect(url_for('web.login'))

@bp.get('/')
@login_required
def index():
    query=request.args.get('q','').strip()[:120]
    all_books=models.books()
    all_loans=models.loans()
    today=date.today().isoformat()
    stats={'titles':len(all_books),'available':sum(b['available'] for b in all_books),
           'active':sum(l['returned_on'] is None for l in all_loans),
           'overdue':sum(l['returned_on'] is None and l['due_on']<today for l in all_loans)}
    return render_template('index.html',books=models.books(query),all_books=all_books,
        readers=models.readers(),loans=all_loans,stats=stats,q=query,today=today,
        default_due=(date.today()+timedelta(days=14)).isoformat(),
        max_due=(date.today()+timedelta(days=60)).isoformat())

def mutation(action,message):
    try:
        action()
        flash(message,'success')
    except models.ValidationError as exc:
        flash(str(exc),'error')
    except sqlite3.OperationalError:
        current_app.logger.exception('Falha de persistência')
        flash('Não foi possível salvar agora. Tente novamente.','error')
    return redirect(url_for('web.index'))

@bp.post('/books')
@login_required
def add_book():
    return mutation(lambda:models.add_book(request.form),'Livro cadastrado.')

@bp.post('/readers')
@login_required
def add_reader():
    return mutation(lambda:models.add_reader(request.form),'Leitor cadastrado.')

@bp.post('/loans')
@login_required
def borrow():
    return mutation(lambda:models.borrow(request.form),'Empréstimo registrado.')

@bp.post('/loans/<int:loan_id>/return')
@login_required
def give_back(loan_id):
    return mutation(lambda:models.give_back(loan_id),'Devolução registrada. Exemplar disponível novamente.')
