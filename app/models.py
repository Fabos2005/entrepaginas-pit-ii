"""Persistência e regras de negócio; estoque calculado, nunca duplicado."""
import sqlite3
from datetime import date, timedelta
from flask import current_app, g

class ValidationError(ValueError):
    pass

def db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'], timeout=10)
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys=ON')
    return g.db

def text(value, label, maximum):
    value = (value or '').strip()
    if not value or len(value) > maximum:
        raise ValidationError(f'{label}: preencha entre 1 e {maximum} caracteres.')
    return value

def integer(value, label, maximum=999):
    try:
        result = int(value)
    except (ValueError, TypeError):
        raise ValidationError(f'{label}: informe um número inteiro.') from None
    if not 1 <= result <= maximum:
        raise ValidationError(f'{label}: valor fora do intervalo permitido.')
    return result

def books(query=''):
    return db().execute('''SELECT b.*, b.copies-count(l.id) available FROM books b
        LEFT JOIN loans l ON b.id=l.book_id AND l.returned_on IS NULL
        WHERE b.title LIKE ? OR b.author LIKE ? GROUP BY b.id ORDER BY b.title''',
        ('%'+query+'%', '%'+query+'%')).fetchall()

def readers():
    return db().execute('SELECT * FROM readers ORDER BY name').fetchall()

def loans():
    return db().execute('''SELECT l.*, b.title, r.name, r.code FROM loans l
        JOIN books b ON b.id=l.book_id JOIN readers r ON r.id=l.reader_id
        ORDER BY l.returned_on IS NOT NULL, l.due_on, l.id DESC''').fetchall()

def add_book(form):
    values = (text(form.get('title'),'Título',120), text(form.get('author'),'Autor',100),
              integer(form.get('copies'),'Exemplares'))
    with db():
        db().execute('INSERT INTO books(title,author,copies) VALUES (?,?,?)', values)

def add_reader(form):
    values = (text(form.get('name'),'Nome',100), text(form.get('code'),'Código',30).upper())
    try:
        with db():
            db().execute('INSERT INTO readers(name,code) VALUES (?,?)',values)
    except sqlite3.IntegrityError:
        raise ValidationError('Este código de leitor já está cadastrado.') from None

def borrow(form):
    book_id = integer(form.get('book_id'),'Livro',2**31-1)
    reader_id = integer(form.get('reader_id'),'Leitor',2**31-1)
    try:
        due = date.fromisoformat(form.get('due_on',''))
    except (ValueError, TypeError):
        raise ValidationError('Informe uma data de devolução válida.') from None
    if not date.today() <= due <= date.today()+timedelta(days=60):
        raise ValidationError('O prazo deve ser entre hoje e os próximos 60 dias.')
    connection = db()
    try:
        # Bloqueio antes de consultar disponibilidade evita empréstimo concorrente excessivo.
        connection.execute('BEGIN IMMEDIATE')
        book = connection.execute('SELECT copies FROM books WHERE id=?',(book_id,)).fetchone()
        reader = connection.execute('SELECT id FROM readers WHERE id=?',(reader_id,)).fetchone()
        if not book or not reader:
            raise ValidationError('Livro ou leitor não encontrado.')
        active = connection.execute('SELECT count(*) FROM loans WHERE book_id=? AND returned_on IS NULL',(book_id,)).fetchone()[0]
        if active >= book['copies']:
            raise ValidationError('Não há exemplares disponíveis deste livro.')
        connection.execute('INSERT INTO loans(book_id,reader_id,borrowed_on,due_on) VALUES (?,?,?,?)',
                           (book_id,reader_id,date.today().isoformat(),due.isoformat()))
        connection.commit()
    except Exception:
        connection.rollback()
        raise

def give_back(loan_id):
    with db():
        result = db().execute('UPDATE loans SET returned_on=? WHERE id=? AND returned_on IS NULL',
                              (date.today().isoformat(),loan_id))
        if result.rowcount != 1:
            raise ValidationError('Empréstimo inexistente ou já devolvido.')
