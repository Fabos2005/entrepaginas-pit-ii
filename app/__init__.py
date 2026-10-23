"""Fábrica Flask: configuração, proteção de sessão e inicialização idempotente."""
import os
import secrets
from pathlib import Path
from datetime import timedelta
from flask import Flask, g, session, request, abort, render_template
from . import models

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        ADMIN_PASSWORD=os.environ.get('ADMIN_PASSWORD'),
        DATABASE=os.environ.get('DATABASE',str(Path(app.instance_path)/'library.sqlite')),
        SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=os.environ.get('COOKIE_SECURE')=='1',
        PERMANENT_SESSION_LIFETIME=timedelta(hours=2), MAX_CONTENT_LENGTH=16384,
    )
    if test_config:
        app.config.update(test_config)
    if not app.config['SECRET_KEY'] or not app.config['ADMIN_PASSWORD']:
        raise RuntimeError('Configure SECRET_KEY e ADMIN_PASSWORD antes de iniciar. Consulte README.md.')
    Path(app.config['DATABASE']).parent.mkdir(parents=True, exist_ok=True)
    with app.app_context():
        models.db().executescript(Path(__file__).with_name('schema.sql').read_text())
        models.db().commit()
        g.pop('db').close()
    @app.teardown_appcontext
    def close_db(error=None):
        connection = g.pop('db',None)
        if connection is not None:
            connection.close()
    @app.before_request
    def protect_forms():
        if 'csrf' not in session:
            session['csrf'] = secrets.token_hex(32)
        if request.method == 'POST':
            token=request.form.get('csrf','')
            if not secrets.compare_digest(token.encode(),session['csrf'].encode()):
                abort(400, description='Formulário expirado. Recarregue a página e tente novamente.')
    @app.after_request
    def headers(response):
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['X-Frame-Options']='DENY'
        response.headers['Content-Security-Policy']="default-src 'self'; style-src 'self'; script-src 'self'; form-action 'self'; frame-ancestors 'none'"
        response.headers['Cache-Control']='no-store'
        return response
    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(413)
    def error_page(error):
        return render_template('error.html',message=error.description),error.code
    from .controllers import bp
    app.register_blueprint(bp)
    return app
