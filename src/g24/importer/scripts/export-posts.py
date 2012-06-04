import MySQLdb
import time

from xml.dom.minidom import Document

conn = MySQLdb.connect (host = "localhost",
                           user = "root",
                           passwd = "root",
                           db = "g24")

"""
mysql> describe nuke_phpbb_topics;
+---------------------+-----------------------+------+-----+---------+----------------+
| Field               | Type                  | Null | Key | Default | Extra          |
+---------------------+-----------------------+------+-----+---------+----------------+
| topic_id            | mediumint(8) unsigned | NO   | PRI | NULL    | auto_increment |
| forum_id            | smallint(8) unsigned  | NO   | MUL | 0       |                |
| topic_title         | char(60)              | NO   |     |         |                |
| topic_poster        | mediumint(8)          | NO   |     | 0       |                |
| topic_time          | int(11)               | NO   |     | 0       |                |
| topic_views         | mediumint(8) unsigned | NO   |     | 0       |                |
| topic_replies       | mediumint(8) unsigned | NO   |     | 0       |                |
| topic_status        | tinyint(3)            | NO   | MUL | 0       |                |
| topic_vote          | tinyint(1)            | NO   |     | 0       |                |
| topic_type          | tinyint(3)            | NO   | MUL | 0       |                |
| topic_first_post_id | mediumint(8) unsigned | NO   |     | 0       |                |
| topic_last_post_id  | mediumint(8) unsigned | NO   |     | 0       |                |
| topic_moved_id      | mediumint(8) unsigned | NO   | MUL | 0       |                |
| topic_attachment    | tinyint(1)            | NO   |     | 0       |                |
| topic_icon          | tinyint(2) unsigned   | NO   |     | 0       |                |
| support_status      | tinyint(3)            | NO   |     | 0       |                |
+---------------------+-----------------------+------+-----+---------+----------------+

mysql> describe nuke_phpbb_posts;
+-----------------+-----------------------+------+-----+---------+----------------+
| Field           | Type                  | Null | Key | Default | Extra          |
+-----------------+-----------------------+------+-----+---------+----------------+
| post_id         | mediumint(8) unsigned | NO   | PRI | NULL    | auto_increment |
| topic_id        | mediumint(8) unsigned | NO   | MUL | 0       |                |
| forum_id        | smallint(5) unsigned  | NO   | MUL | 0       |                |
| poster_id       | mediumint(8)          | NO   | MUL | 0       |                |
| post_time       | int(11)               | NO   | MUL | 0       |                |
| poster_ip       | varchar(8)            | NO   |     |         |                |
| post_username   | varchar(25)           | YES  |     | NULL    |                |
| enable_bbcode   | tinyint(1)            | NO   |     | 1       |                |
| enable_html     | tinyint(1)            | NO   |     | 0       |                |
| enable_smilies  | tinyint(1)            | NO   |     | 1       |                |
| enable_sig      | tinyint(1)            | NO   |     | 1       |                |
| post_edit_time  | int(11)               | YES  |     | NULL    |                |
| post_edit_count | smallint(5) unsigned  | NO   |     | 0       |                |
| post_attachment | tinyint(1)            | NO   |     | 0       |                |
| post_icon       | tinyint(2) unsigned   | NO   |     | 0       |                |
+-----------------+-----------------------+------+-----+---------+----------------+

mysql> describe nuke_phpbb_posts_text;
+--------------+-----------------------+------+-----+---------+-------+
| Field        | Type                  | Null | Key | Default | Extra |
+--------------+-----------------------+------+-----+---------+-------+
| post_id      | mediumint(8) unsigned | NO   | PRI | 0       |       |
| bbcode_uid   | varchar(10)           | NO   |     |         |       |
| post_subject | varchar(60)           | YES  |     | NULL    |       |
| post_text    | text                  | YES  |     | NULL    |       |
+--------------+-----------------------+------+-----+---------+-------+

['post_username', 'post_attachment', 'post_time', 'poster_ip', 'post_subject', 'post_edit_time', 'bbcode_uid', 'enable_html', 'forum_id', 'enable_sig', 'poster_id', 'post_id', 'enable_smilies', 'post_icon', 'post_edit_count', 'topic_id', 'post_text', 'pt.post_id', 'enable_bbcode']

mysql> describe nuke_phpbb_forums;
+-------------------------+-----------------------+------+-----+---------+----------------+
| Field                   | Type                  | Null | Key | Default | Extra          |
+-------------------------+-----------------------+------+-----+---------+----------------+
| forum_id                | smallint(5) unsigned  | NO   | PRI | NULL    | auto_increment |
| cat_id                  | mediumint(8) unsigned | NO   | MUL | 0       |                |
| forum_name              | varchar(150)          | YES  |     | NULL    |                |
| forum_desc              | text                  | YES  |     | NULL    |                |
| forum_status            | tinyint(4)            | NO   |     | 0       |                |
| forum_order             | mediumint(8) unsigned | NO   | MUL | 1       |                |
| forum_posts             | mediumint(8) unsigned | NO   |     | 0       |                |
| forum_topics            | mediumint(8) unsigned | NO   |     | 0       |                |
| forum_last_post_id      | mediumint(8) unsigned | NO   | MUL | 0       |                |
| prune_next              | int(11)               | YES  |     | NULL    |                |
| prune_enable            | tinyint(1)            | NO   |     | 0       |                |
| auth_view               | tinyint(2)            | NO   |     | 0       |                |
| auth_read               | tinyint(2)            | NO   |     | 0       |                |
| auth_post               | tinyint(2)            | NO   |     | 0       |                |
| auth_reply              | tinyint(2)            | NO   |     | 0       |                |
| auth_edit               | tinyint(2)            | NO   |     | 0       |                |
| auth_delete             | tinyint(2)            | NO   |     | 0       |                |
| auth_sticky             | tinyint(2)            | NO   |     | 0       |                |
| auth_announce           | tinyint(2)            | NO   |     | 0       |                |
| auth_vote               | tinyint(2)            | NO   |     | 0       |                |
| auth_pollcreate         | tinyint(2)            | NO   |     | 0       |                |
| auth_attachments        | tinyint(2)            | NO   |     | 0       |                |
| auth_download           | tinyint(2)            | NO   |     | 0       |                |
| topic_sort_order        | tinyint(2)            | NO   |     | 0       |                |
| post_sort_order         | tinyint(2)            | NO   |     | 0       |                |
| support_forum           | tinyint(1)            | NO   |     | 0       |                |
| exclude_global_announce | tinyint(1)            | NO   |     | 0       |                |
+-------------------------+-----------------------+------+-----+---------+----------------+

"""

dom = Document()
dom.appendChild(dom.createElement('export'))

topiccursor = conn.cursor (MySQLdb.cursors.DictCursor)

sql_str = "select forum_id, forum_name, forum_desc, cat_title, cat_desc  from nuke_phpbb_forums f join nuke_phpbb_categories c on f.cat_id = c.cat_id"
topiccursor.execute (sql_str);
topicrows = topiccursor.fetchall()
cats_info = {}
for catrow in topicrows:
     cats_info[catrow['forum_id']] = catrow

#topiccursor.close() 

sql_str = "select * from nuke_phpbb_topics"
#sql_str = sql_str + " limit 0,5"
topiccursor.execute (sql_str);
topicrows = topiccursor.fetchall() 

# loop over topics
for topic in topicrows:
    try:
        threadnode = dom.createElement('thread')
        
        #tstruct = time.gmtime()
        
        #print cats_info[topic["forum_id"]]
        
        tags = [ cats_info[topic["forum_id"]]['forum_name'].decode('latin-1'), cats_info[topic["forum_id"]]['cat_title'].decode('latin-1')]
        
        # select posts for topic
        postcursor  = conn.cursor (MySQLdb.cursors.DictCursor)
        sql_str = "select * from nuke_phpbb_posts p left join nuke_phpbb_posts_text pt on p.post_id = pt.post_id where topic_id = " + str(topic['topic_id']) 
        postcursor.execute (sql_str);
        rows = postcursor.fetchall()
        
        # loop over topic's posts
        for row in rows:
            postnode = dom.createElement('post')
            
            # set attributes
            export_fields = ["post_username", "post_time", "post_subject"] 
            for attr in export_fields: 
                postnode.setAttribute(attr, str(row[attr]).decode('latin-1'))
            
            # clean posting text
            posting_text = row['post_text'].decode('latin-1')
            cleaned = []
            for line in posting_text.split("\n"):
                cleaned.append(''.join(c for c in line if ord(c) >= 32))
            
            # add posting text 
            txt = dom.createElement('text')
            txt.appendChild(dom.createCDATASection("\n".join(cleaned)))
            postnode.appendChild(txt)
            
            # add tags
            for t in tags:
                tagnode = dom.createElement('tag')
                tagnode.setAttribute('name', t)
                postnode.appendChild(tagnode)
            
            # add posting to thread
            threadnode.appendChild(postnode)

        # add topic/thread to export
        dom.childNodes[0].appendChild(threadnode)
        
        postcursor.close ()

    except Exception as err:
        #print "error in row" , str(rowcount)
        print "export of topic failed"
        print err

topiccursor.close()
conn.close ()

with open("export-posts.xml", "w") as f:
    f.write(dom.toprettyxml(encoding="UTF-8")) 


