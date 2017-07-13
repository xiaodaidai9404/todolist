#!/usr/bin/python2.7
#coding=utf-8

import sys
reload(sys)

sys.setdefaultencoding('utf8')

import MySQLdb

def select0(now_time,yes_time):
    conn=MySQLdb.connect(host='localhost',user='root',db='study',port=3306,passwd='xiongqian0610',unix_socket='/private/tmp/mysql.sock',charset="utf8")
    cur=conn.cursor()
    rows = cur.execute('select item_name,item_level,statu,date from dolist_tbl where date>=%s and date<=%s and statu=0',(yes_time,now_time))
    if rows == 0 :
        return ''
    else:
        return cur.fetchall()
    cur.close()
    conn.close()

def select1(now_time,yes_time):
    conn=MySQLdb.connect(host='localhost',user='root',db='study',port=3306,passwd='xiongqian0610',unix_socket='/private/tmp/mysql.sock',charset="utf8")
    cur=conn.cursor()
    rows = cur.execute('select item_name,item_level,statu,date from dolist_tbl where date>=%s and date<=%s and statu=1',(yes_time,now_time))
    if rows == 0 :
        return ''
    else:
        return cur.fetchall()
    cur.close()
    conn.close()

def insert(item_name,item_level,nowtime):
    conn=MySQLdb.connect(host='localhost',user='root',db='study',port=3306,passwd='xiongqian0610',unix_socket='/private/tmp/mysql.sock',charset="utf8")
    cur=conn.cursor()
    cur.execute('insert into dolist_tbl (item_name,item_level,date) values(%s,%s,%s)',(item_name,item_level,nowtime))
    conn.commit()
    cur.close()

def delete(item_name):
    conn = MySQLdb.connect(host='localhost', user='root', db='study', port=3306, passwd='xiongqian0610',unix_socket='/private/tmp/mysql.sock',charset="utf8")
    cur = conn.cursor()
    cur.execute('delete from dolist_tbl where item_name=%s', (item_name))
    conn.commit()
    cur.close()

def update(item_name):
    conn=MySQLdb.connect(host='localhost',user='root',db='study',port=3306,passwd='xiongqian0610',unix_socket='/private/tmp/mysql.sock',charset="utf8")
    cur=conn.cursor()
    cur.execute('update dolist_tbl set statu=1 where item_name=%s',(item_name))
    conn.commit()
    cur.close()


