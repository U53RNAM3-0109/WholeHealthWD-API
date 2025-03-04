import sys
import os

# Path to project directory & venv
proj_home = 'var/www/html/WholeHealthWD-API'
venv_path = 'var/www/html/apivenv'

# Add dir to sys.path
sys.path.insert(0, proj_home)

# Activate Venv
activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')
exec(open(activate_this).read(), dict(__file__=activate_this)

# Start app
from app import app as application
