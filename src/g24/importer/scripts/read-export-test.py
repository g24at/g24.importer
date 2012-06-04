import MySQLdb
import time
from xml.dom.minidom import parse

"""
dom = parse('userexport.xml')
for el in dom.getElementsByTagName('user'):
    print el.getAttribute('username')
"""


dom = parse('export-posts.xml')

for p in dom.getElementsByTagName('post'):
    print p.getAttribute('post_id') , p.getAttribute('post_subject')
    
