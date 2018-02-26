#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import html
import http.cookies
import os

from _wall import Wall

wall = Wall()

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")
if session is not None:
    session = session.value
user = wall.find_cookie(session)  # Ищем пользователя по переданной куке

form = cgi.FieldStorage()
action = form.getfirst("action", "")

if action == "publish":
    text = form.getfirst("text", "")
    text = html.escape(text)
    if text and user is not None:
        wall.publish(user, text)
elif action == "login":
    login = form.getfirst("login", "")
    login = html.escape(login)
    password = form.getfirst("password", "")
    password = html.escape(password)
    if wall.find(login, password):
        cookie = wall.set_cookie(login)
        print('Set-cookie: session={}'.format(cookie))
    elif wall.find(login):
        pass  # А надо бы предупреждение выдать
    else:
        wall.register(login, password)
        cookie = wall.set_cookie(login)
        print('Set-cookie: session={}'.format(cookie))

pattern = '''
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Стена</title>

  
<link href="/css/bootstrap.css" rel="stylesheet">
<link href="/css/style.css" rel="stylesheet">

</head>
<body>
<div class="container-fluid">
      <div class = "row" style="background: black;" id="topOffset">
          <div class = "col-md-1 col-sm-2 col-xs-3 text-left">
            <div class = "row">
                <div class = "col-md-offset-2 col-md-8 logo"></div>
            </div>
          </div>
          <div class = "col-md-10 col-sm-9 col-xs-7 center">
            <p class="page_name">Handwritten Calculator</p>
          </div>
          <div class = "col-md-1 col-sm-1 col-xs-2 text-right" ></div>
      </div>
      
      <div class="row" style="padding-top:10px">
        <div class="col-md-3" id="leftOffset"></div>
        <div class="col-md-6 center">
            <div id="canvasSimpleDiv"></div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-offset-4 col-md-4 center">
            <button id="clearCanvasSimple" type="button">Clear</button>
        </div>
      </div>
</div>
    <!--Форма логина и регистрации. При вводе несуществующего имени зарегистрируется новый пользователь.
    <div class='testdiv'>
        <form action="/cgi-bin/wall.py">
            Логин: <input type="text" name="login">
            Пароль: <input type="password" name="password">
            <input type="hidden" name="action" value="login">
            <input type="submit">
        </form>
    </div>

    {posts}

    {publish}-->
    
    <!-- Include all compiled plugins (below), or include individual files as needed -->
<script src="/js/bootstrap.js"></script>

    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.js"></script>
    <!--[if IE]><script type="text/javascript" src="/js/excanvas.js"></script><![endif]-->
    <script type="text/javascript" src="/js/simple.js"></script>
</body>  

</html>
'''

if user is not None:
    pub = '''
    <form action="/cgi-bin/wall.py">
        <textarea name="text"></textarea>
        <input type="hidden" name="action" value="publish">
        <input type="submit">
    </form>
    '''
else:
    pub = ''

print('Content-type: text/html\n')

print(pattern.format(posts=wall.html_list(), publish=pub))