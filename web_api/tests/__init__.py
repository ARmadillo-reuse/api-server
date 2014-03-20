import os
import importlib

directory = os.path.dirname(os.path.realpath(__file__))

test_files = [f.rstrip(".py") for f in os.listdir(directory)
           if os.path.isfile("%s/%s"%(directory,f))
           and f.endswith(".py")
           and f != "__init__.py"]

for f in test_files:
    exec("from web_api.tests.%s import %s" % (f,f))

__all__ = test_files
