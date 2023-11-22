# backup_script.py
import subprocess
import os
from datetime import datetime

# Imposta il percorso del tuo progetto Django
DJANGO_PROJECT_PATH = '/home/giulio/django/mapelli'

# Trova il percorso completo di Python nell'ambiente virtuale
python_path = '/home/giulio/django/venv/bin/python'

# Crea un nome di file unico basato sulla data e ora correnti
backup_file_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

# Percorso completo del file di backup
backup_file_path = os.path.join(DJANGO_PROJECT_PATH, backup_file_name)

# Comando per eseguire il dump del database
dump_command = f"{python_path} {os.path.join(DJANGO_PROJECT_PATH, 'manage.py')} dumpdata --indent 4 > {backup_file_path}"

# Esegui il comando di dump del database
subprocess.run(dump_command, shell=True, cwd=DJANGO_PROJECT_PATH)

