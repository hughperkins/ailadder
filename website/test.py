
from core import *
from utils import *

def test():
   tester.test()
   dates.test()
   stringhelper.test()

   sqlalchemysetup.setup()
   roles.test()
   sqlalchemysetup.close()

if __name__ == '__main__':
   test()

