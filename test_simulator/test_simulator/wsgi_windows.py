
import os
import sys
import site
from django.core.wsgi import get_wsgi_application

# add python site packages, you can use virtualenvs also
site.addsitedir("C:/Users/felisilva/Desktop/Felipe/Projetos/TestSimulator/Lib/site-packages")

# Add the app's directory to the PYTHONPATH 
sys.path.append('C:/Users/felisilva/Desktop/Felipe/Projetos/TestSimulator/test_simulator') 
sys.path.append('C:/Users/felisilva/Desktop/Felipe/Projetos/TestSimulator/test_simulator/test_simulator')  

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_simulator.settings' 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_simulator.settings")  
 
application = get_wsgi_application()