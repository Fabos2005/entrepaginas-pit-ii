"""Executar no terminal da hospedagem; segredos ficam fora do repositório."""
import getpass
import json
import os
import secrets
from pathlib import Path

def configure():
    target = Path.home() / '.config' / 'entrepaginas.json'
    if target.exists():
        raise SystemExit('Configuração já existe; nenhuma alteração realizada.')
    password = getpass.getpass('Defina a senha da aplicação (mínimo 12 caracteres): ')
    confirmation = getpass.getpass('Repita a senha: ')
    if len(password) < 12 or password != confirmation:
        raise SystemExit('Senha curta ou confirmação diferente; tente novamente.')
    data = {'SECRET_KEY': secrets.token_hex(32), 'ADMIN_PASSWORD': password,
            'COOKIE_SECURE': '1',
            'DATABASE': str(Path.home() / '.local' / 'share' / 'entrepaginas' / 'library.sqlite')}
    target.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as file:
        json.dump(data, file)
    print('Configuração salva fora do repositório. Segredos não foram exibidos.')

if __name__ == '__main__':
    configure()
