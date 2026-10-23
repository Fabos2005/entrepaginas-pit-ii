"""Copiar este conteúdo para o arquivo WSGI indicado na aba Web."""
import json
import os
import sys
import time
from pathlib import Path

project = Path.home() / 'entrepaginas-pit-ii'
sys.path.insert(0, str(project))
settings = json.loads((Path.home() / '.config' / 'entrepaginas.json').read_text())
os.environ.update(settings)
os.environ['TZ'] = 'America/Sao_Paulo'
if hasattr(time, 'tzset'):
    time.tzset()
from app import create_app
application = create_app()
