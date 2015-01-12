import sys, os.path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '.virtualenv', 'lib', 'python2.7', 'site-packages'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from letslide import app as application
