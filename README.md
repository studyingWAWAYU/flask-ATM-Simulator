flask-ATM-Simulator
====
Develop a system that imitates an ATM using the Flask framework in Python, save data to a MySQL database, and write the frontend interface using HTML files
----
### Project Introduction 项目简介
我们的项目是基于PythonWeb中Flask框架开发的一个模仿自动取款机（ATM）的系统，以网页形式使用。
大致可分为：登录功能、主页菜单、查询余额、转账业务、理财频道、充值缴费、取款服务共7个部分。

### Directory Description 目录说明
在项目总文件夹中总共是三个文件夹：
1. static文件夹放静态文件
2. templates文件夹放所有的.html文件
3. views文件夹放所有的.py文件。
每个.py文件都对应了一个.html文件


-__init__.py  蓝图导入，实例化全局的flask对象和数据库对象
manager.py  启动文件（运行此文件）
settings.py  配置文件
sql.py  连接数据库和ORM映射建表


3.1 安装依赖项

下载源码后，安装相关依赖库
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask,render_template,request,redirect,session,flash
from flask import Blueprint
import time


3.2 自建MySQL数据库

自建一个本地MySQL数据库，根据本地数据库更改项目 ATMflask/ATMflask/sql.py 文件下连接MySQL的数据库账号名，密码等信息。

3.3 运行主文件

连接上后，运行 ATMflask/ATMflask/manager.py 文件即可得到网址

3.4 打开网址使用

点击网址进入即可使用
