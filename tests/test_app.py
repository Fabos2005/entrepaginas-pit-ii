import tempfile, unittest, sqlite3
from pathlib import Path
from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor
from app import create_app, models

class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.app=create_app({'TESTING':True,'SECRET_KEY':'test-key','ADMIN_PASSWORD':'test-pass','DATABASE':str(Path(self.tmp.name)/'test.sqlite')})
        self.client=self.app.test_client()
        self.client.get('/login'); self.post('/login',{'password':'test-pass'})
        with self.app.app_context():
            models.add_book({'title':'Dom Casmurro','author':'Machado de Assis','copies':'1'})
            models.add_reader({'name':'Leitor de teste','code':'T-001'})
        self.loan={'book_id':'1','reader_id':'1','due_on':(date.today()+timedelta(days=14)).isoformat()}
    def tearDown(self): self.tmp.cleanup()
    def post(self,url,data):
        with self.client.session_transaction() as s: token=s['csrf']
        return self.client.post(url,data={**data,'csrf':token},follow_redirects=True)
    def test_dashboard(self):
        r=self.client.get('/'); self.assertEqual(r.status_code,200); self.assertIn('Dom Casmurro',r.text)
    def test_requires_login(self): self.assertEqual(self.app.test_client().get('/').status_code,302)
    def test_wrong_password(self):
        self.post('/logout',{}); self.assertIn('Senha incorreta',self.post('/login',{'password':'incorréta'}).text)
    def test_csrf(self): self.assertEqual(self.client.post('/books',data={'title':'x','csrf':'inválido'}).status_code,400)
    def test_book_creation(self): self.assertIn('Livro cadastrado',self.post('/books',{'title':'Novo','author':'Autor','copies':'2'}).text)
    def test_blank_title(self): self.assertIn('preencha entre',self.post('/books',{'title':' ','author':'A','copies':'1'}).text)
    def test_invalid_quantity(self):
        for copies in ['0','-1','1.5','1000','x']:
            with self.subTest(copies=copies),self.app.app_context(),self.assertRaises(models.ValidationError):
                models.add_book({'title':'T','author':'A','copies':copies})
    def test_duplicate_reader(self): self.assertIn('já está cadastrado',self.post('/readers',{'name':'Outro','code':'t-001'}).text)
    def test_borrow_decreases_availability(self):
        self.post('/loans',self.loan)
        with self.app.app_context(): self.assertEqual(models.books()[0]['available'],0)
    def test_out_of_stock(self):
        self.post('/loans',self.loan); self.assertIn('Não há exemplares',self.post('/loans',self.loan).text)
    def test_past_due_date_rejected(self): self.assertIn('próximos 60 dias',self.post('/loans',{**self.loan,'due_on':(date.today()-timedelta(days=1)).isoformat()}).text)
    def test_future_limit(self): self.assertIn('próximos 60 dias',self.post('/loans',{**self.loan,'due_on':(date.today()+timedelta(days=61)).isoformat()}).text)
    def test_invalid_date(self): self.assertIn('data de devolução válida',self.post('/loans',{**self.loan,'due_on':'2026-02-31'}).text)
    def test_unknown_reader(self): self.assertIn('não encontrado',self.post('/loans',{**self.loan,'reader_id':'999'}).text)
    def test_return_and_history(self):
        self.post('/loans',self.loan); self.post('/loans/1/return',{})
        with self.app.app_context():
            self.assertEqual(models.books()[0]['available'],1); self.assertIsNotNone(models.loans()[0]['returned_on'])
    def test_duplicate_return(self):
        self.post('/loans',self.loan); self.post('/loans/1/return',{}); self.assertIn('já devolvido',self.post('/loans/1/return',{}).text)
    def test_missing_return(self): self.assertIn('inexistente',self.post('/loans/999/return',{}).text)
    def test_search(self):
        self.assertIn('Dom Casmurro',self.client.get('/?q=Machado').text); self.assertIn('Nenhum resultado',self.client.get('/?q=zzzzzz').text)
    def test_xss_escaped(self):
        r=self.post('/books',{'title':'<script>alert(1)</script>','author':'Autor','copies':'1'})
        self.assertNotIn('<script>alert(1)</script>',r.text); self.assertIn('&lt;script&gt;',r.text)
    def test_sql_injection_search(self):
        self.client.get('/?q=%27%20OR%201=1--')
        with self.app.app_context(): self.assertEqual(len(models.books()),1)
    def test_foreign_key(self):
        with self.app.app_context(),self.assertRaises(sqlite3.IntegrityError):
            models.db().execute('INSERT INTO loans(book_id,reader_id,borrowed_on,due_on) VALUES (9,9,?,?)',(date.today().isoformat(),date.today().isoformat()))
    def test_concurrency_last_copy(self):
        def attempt(_):
            with self.app.app_context():
                try: models.borrow(self.loan); return True
                except models.ValidationError: return False
        with ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(attempt,range(2)))
        self.assertEqual(sum(results),1)
    def test_overdue(self):
        with self.app.app_context():
            yesterday=(date.today()-timedelta(days=1)).isoformat()
            models.db().execute('INSERT INTO loans(book_id,reader_id,borrowed_on,due_on) VALUES (1,1,?,?)',(yesterday,yesterday)); models.db().commit()
        self.assertIn('Em atraso',self.client.get('/').text)
    def test_persistence(self):
        app2=create_app(dict(self.app.config))
        with app2.app_context(): self.assertEqual(models.books()[0]['title'],'Dom Casmurro')
    def test_security_headers(self):
        r=self.client.get('/'); self.assertEqual(r.headers['X-Frame-Options'],'DENY'); self.assertIn("default-src 'self'",r.headers['Content-Security-Policy'])
    def test_not_found(self): self.assertEqual(self.client.get('/missing').status_code,404)

if __name__=='__main__': unittest.main(verbosity=2)
