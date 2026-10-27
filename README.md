# EntrePáginas — DESCONTINUADO

Projeto acadêmico de gestão de biblioteca comunitária desenvolvido para Projeto Integrador Transdisciplinar em Engenharia de Software II.

> **Projeto descontinuado, preservado somente como histórico. Não integra a entrega atual do PIT II. Código e documentação abaixo não representam uma aplicação em produção.**

## Situação da aplicação

Aplicação desativada; este projeto não possui endereço público ativo.

A senha de demonstração é compartilhada separadamente com os avaliadores. Use dados fictícios.

## Executar localmente (Windows / PowerShell)

Instale Python 3.12 ou superior pelo site oficial https://www.python.org/downloads/ e extraia este ZIP. Abra um terminal na pasta que contém `run.py`.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:SECRET_KEY = (.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))")
$env:ADMIN_PASSWORD = Read-Host 'Defina a senha de acesso (uso local)'
.\.venv\Scripts\python.exe run.py
```

Abra http://127.0.0.1:5000 e use a senha definida. O terminal precisa permanecer aberto. Nenhum dado de demonstração é cadastrado automaticamente. Os registros persistem em `instance/library.sqlite`; não apague esse arquivo. Repita a definição das duas variáveis ao abrir outro terminal. Trocar SECRET_KEY encerra sessões antigas.

Linux/macOS: `python3 -m venv .venv`, `. .venv/bin/activate`, `pip install -r requirements.txt`. Configure SECRET_KEY aleatória e ADMIN_PASSWORD no ambiente; execute `python run.py`.

## O que funciona

Acesso por senha; cadastro de livros e leitores; busca de título/autor; empréstimos com prazo de até 60 dias; estoque calculado; devolução com histórico; indicação de atrasos e indicadores. Acesso é de um responsável compartilhado: não há contas individuais de leitores. Não há exclusão, edição, renovação, reserva, multas ou envio de mensagens nesta versão.

## Testes

`python -m unittest discover -s tests -v`

26 testes automatizados passaram no ambiente de desenvolvimento. Evidência: `docs/test-results.txt`. Os testes incluem modelos, banco de dados, controladores e HTML renderizado, com concorrência de dois empréstimos para o último exemplar. Não equivalem a teste visual em navegador nem a avaliação com cinco pessoas.

## Estrutura / MVC

- `app/models.py`: modelo, SQL parametrizado e validações.
- `app/controllers.py`: controladores HTTP e fluxo de autenticação.
- `app/templates/`, `app/static/`: views HTML/Jinja, CSS e JavaScript.
- `app/schema.sql`: projeto físico e restrições.
- `docs/`: documentação, modelagem, avaliação, roteiro e pendências.

## Publicação

1. Código e documentação: https://github.com/Fabos2005/entrepaginas-pit-ii. O repositório não é o endereço da aplicação. Para hospedar sem instalar Python no computador, siga `docs/HOSPEDAGEM.md`.
2. Escolha hospedagem Python/WSGI com disco persistente para SQLite, HTTPS e variáveis de ambiente. O arquivo `Procfile` oferece um comando Gunicorn para provedores compatíveis; ajuste PORT conforme o provedor. É necessário um único servidor/instância com esse disco compartilhado entre suas threads; não usar múltiplas réplicas com arquivos independentes.
3. Configure `SECRET_KEY` aleatória, `ADMIN_PASSWORD` exclusiva, `COOKIE_SECURE=1` e `DATABASE` apontando para o arquivo no volume persistente. Instale `requirements.txt`; inicie `gunicorn --workers 1 --threads 4 --bind 0.0.0.0:8000 'app:create_app()'` (Linux).
4. Teste cadastro, empréstimo e devolução no endereço público e reinicie a aplicação para verificar persistência. Faça backup do SQLite com a API de backup do SQLite; não copie o arquivo durante gravações.
5. Use apenas dados fictícios na demonstração e compartilhe a senha de demonstração separadamente com avaliadores. A versão não possui limitação de tentativas de login, recuperação de senha nem gestão de usuários; não é adequada a operação pública com dados pessoais reais sem ampliar essas proteções.

Aplicação descontinuada. Este material é histórico e não integra a entrega atual do PIT II. A hospedagem gratuita requer renovação mensal pelo botão "Run until 1 month from today" na aba Web; não requer upgrade.

## Roteiro para fechar a entrega

O planejamento está em [PIT I - Atualizado](docs/PIT%20I%20-%20Atualizado.md). A documentação técnica está em `docs/PROJETO.md` e `docs/MODELAGEM.md`.

**Atenção: há dois vídeos no template oficial.** Além do vídeo inicial (campo mínimo 5 minutos), a última página pede outro, de até 5 minutos, após os feedbacks e correções. Os dois roteiros estão em `docs/ROTEIRO-VIDEO.md`.
