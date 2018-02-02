import os
from prettytable import PrettyTable
t = PrettyTable(['Command', 'Result'])
t.add_row(['__file__', __file__])
t.add_row(['os.path.realpath(__file__)', os.path.realpath(__file__)])
t.add_row(['os.path.abspath(__file__)', os.path.abspath(__file__)])
t.add_row(['os.path.dirname(os.path.abspath(__file__))', os.path.dirname(os.path.abspath(__file__))])
t.add_row(['os.path.dirname(__file__)', os.path.dirname(__file__)])
t.add_row(['os.path.abspath(os.path.dirname(__file__))', os.path.abspath(os.path.dirname(__file__))])

print t

DIR = os.path.abspath(os.path.dirname(__file__))
FILENAME = "log/" + __file__ + ".log"

print os.path.join(DIR, FILENAME)