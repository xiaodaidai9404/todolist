#!/usr/bin/env python2.7
#coding=utf-8

import sys

reload(sys)

sys.setdefaultencoding('utf8')

from flask import Flask,request,render_template,session,redirect,url_for,flash
from flask_script import Manager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
import action_db
import time
import datetime

app = Flask(__name__)
bootstrap =  Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'welcome to my blog'


#一个时间获取函数，返回当天的日期和7天之前的日期
def Time():
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-7)
    return now_time.strftime('%Y-%m-%d'),yes_time.strftime('%Y-%m-%d')

#展示页面，get页面直接返回页面，post的话点击stop的话就删除这条记录再返回页面，ok的话就改变事情的状态然后再返回页面
@app.route('/',methods=['GET','POST'])
def show():
    nowtime = Time()
    item0 = action_db.select0(nowtime[0], nowtime[1])
    item1 = action_db.select1(nowtime[0], nowtime[1])
    if item0 == '':
        item0 = []
    elif item1 == '':
        item1 = []
    items=format(item0,item1)
    if request.method == 'POST':
        print request.form
        if request.form.keys() == ['stop']:
            action_db.delete(request.form['stop'])
            item0 = action_db.select0(nowtime[0], nowtime[1])
            item1 = action_db.select1(nowtime[0], nowtime[1])
            items = format(item0,item1)
        elif request.form.keys() == ['ok']:
            action_db.update(request.form['ok'])
            item0 = action_db.select0(nowtime[0], nowtime[1])
            item1 = action_db.select1(nowtime[0], nowtime[1])
            items = format(item0,item1)
        elif request.form['submit'] == 'Create Todo':
            item_name = request.form['thing']
            item_level = request.form['level']
            action_db.insert(item_name,item_level,nowtime[0])
            item0 = action_db.select0(nowtime[0], nowtime[1])
            item1 = action_db.select1(nowtime[0], nowtime[1])
            items = format(item0, item1)
        return render_template('show1.html', items=items)
    return render_template('show1.html',items=items)

@app.route('/update',methods=['GET','POST'])
def update():
    return render_template('update.html')

@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/user/<name>',methods=['GET','POST'])
def user(name):
    session['name'] = name
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        #return render_template('user.html',form=form,name=session.get('name'))
    return render_template('user.html',form=form,name=session.get('name'))

#下面的三个函数用来处理todolist页面的排序
def cmp_ignore_case(s1, s2):
    if s1 == '重要' and s2 == '紧急':
        return 1
    elif s1 == '普通'  and s2 != '普通':
        return 1
    else:
        return -1

def cmp_ignore_statu(s1, s2):
    if s1 == '0':
        return -1
    else:
        return 1

def format(item0,item1):
    item_no = sorted(item0, cmp=lambda x, y: cmp_ignore_case(x[1], y[1]))
    item_yes = sorted(item1, cmp=lambda x, y: cmp_ignore_case(x[1], y[1]))
    items = item_no + item_yes
    return items

@app.route('/list/<comments>')
def list(comments):
    return render_template('list.html',comments=comments)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

@app.route('/test',methods=['GET','POST'])
def test():
    print request.form
    return render_template('test.html')

class NameForm(Form):
    name = StringField('What is your name?')
    submit =  SubmitField('Submit')


if __name__ == '__main__':
    manager.run()
