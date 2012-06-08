import MySQLdb
import time
from xml.dom.minidom import parse

"""
dom = parse('userexport.xml')
for el in dom.getElementsByTagName('user'):
    print el.getAttribute('username')
"""

dom = parse('export-posts.xml')

for th in dom.getElementsByTagName('thread'):
    print "IMPORT THREAD"
    postings = th.getElementsByTagName('post')

    print "-R-" , postings[0].getAttribute('post_id'),postings[0].getAttribute('post_subject')
    for p in postings[1:len(postings)]:
        print "---", p.getAttribute('post_id') , p.getAttribute('post_subject')

        print p.getElementsByTagName('text')[0].childNodes[1].data

        for t in p.getElementsByTagName('tag'):
            print '.....t', t.getAttribute('name')

