# Publicação no PythonAnywhere

Estado: preparação concluída; implantação depende de conta autenticada e configuração na hospedagem. O repositório GitHub armazena o código e não executa o servidor Python.

## Preparar conta

Criar conta Beginner em https://www.pythonanywhere.com/pricing/ e confirmar o e-mail. Consultar condições atuais do plano. A documentação indica uma aplicação e expiração mensal no plano gratuito; acompanhar o painel e renovar quando solicitado para manter o endereço disponível durante a avaliação.

## Terminal Bash da hospedagem

```bash
git clone https://github.com/Fabos2005/entrepaginas-pit-ii.git
cd entrepaginas-pit-ii
python3.12 -m venv ~/.virtualenvs/entrepaginas
~/.virtualenvs/entrepaginas/bin/pip install -r requirements.txt
~/.virtualenvs/entrepaginas/bin/python deploy/configure_host.py
~/.virtualenvs/entrepaginas/bin/python -m unittest discover -s tests -v
```

O instalador solicita uma senha exclusiva para a aplicação, diferente da senha do GitHub ou da hospedagem. Não publica essa senha. As variáveis ficam em ~/.config/entrepaginas.json, com permissão restrita; banco em ~/.local/share/entrepaginas/library.sqlite. Não enviar esses arquivos ao GitHub.

## Aba Web

Criar uma aplicação, escolher Manual configuration e Python 3.12, desde que a versão esteja disponível na conta. Usar a mesma versão selecionada para o ambiente virtual. Informar o caminho absoluto do virtualenv ~/.virtualenvs/entrepaginas, expandindo ~ para /home/SEU_USUARIO. Abrir o arquivo WSGI indicado pelo painel e substituir pelo conteúdo de deploy/pythonanywhere_wsgi.py. O projeto deve estar em /home/SEU_USUARIO/entrepaginas-pit-ii.

Ativar HTTPS/Force HTTPS quando oferecido e recarregar a aplicação. Não executar run.py para a publicação; a hospedagem importa application no WSGI. Acessar o domínio fornecido pela aba Web, testar login, cadastro, empréstimo, devolução, e recarregar novamente para comprovar persistência. A configuração de cookies seguros exige acesso por HTTPS.

## Evidências e atualização

Capturar telas somente depois de testar o endereço real. Atualizar os links na entrega. Para atualizar o código: git pull --ff-only na pasta e Reload na aba Web. Manter o arquivo do banco e a configuração fora do código. O esquema atual não possui migrações automáticas para futuras alterações estruturais.

## Fontes oficiais

- https://www.pythonanywhere.com/pricing/
- https://help.pythonanywhere.com/pages/FreeAccountsFeatures/
- https://help.pythonanywhere.com/pages/Flask/

A validação visual e o teste da configuração nessa hospedagem ainda estão pendentes.
