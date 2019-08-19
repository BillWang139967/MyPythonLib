#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-08-15 23:05:56

# File Name: test_user.py
# Description:

"""
from faker import Factory
from datetime import datetime
import hashlib

import xlib.db
from xlib.db.peewee import *

# Create an instance of a Database
mysql_config_url="mysql+pool://root:123456@127.0.0.1:3306/test?max_connections=300&stale_timeout=300"
db = xlib.db.connect(url=mysql_config_url)


# Define a model class
class User(Model):
    # If none of the fields are initialized with primary_key=True,
    # an auto-incrementing primary key will automatically be created and named 'id'.
    id = PrimaryKeyField()
    email = CharField(index=True, max_length=64)
    username = CharField(unique=True, max_length=32)
    password = CharField(null=True, max_length=64)
    createTime = DateTimeField(column_name="create_time", default=datetime.now)
    role = CharField(null=False,max_length=64,default="")

    class Meta:
        database = db
        table_name = 'tb_user'
        # If Models without a Primary Key
        # primary_key = False

    def __str__(self):
        return "User(id：{} email：{} username：{} password：{} createTime: {})".format(self.id, self.email, self.username, self.password, self.createTime)

    @staticmethod
    def create_password(raw):
        return hashlib.new("md5", raw).hexdigest()

    def check_password(self, raw):
        return hashlib.new("md5", raw).hexdigest() == self.password


db.connect()
db.drop_tables([User])
db.create_tables([User])

""" CREATE """
print("-------------CREATE")

# 创建User对象
# 明文密码
#user = User.create(email="meetbill@163.com", username="meetbill", password="meet")
password='111111'
user = User.create(email="meetbill@163.com", username="meetbill", password=User.create_password(password),role="admin")
# 保存User
user.save()

# 创建faker工厂对象
faker = Factory.create()
# 利用faker创建多个User对象
fake_users = [{
    'username': faker.name(),
    'password': faker.word(),
    'email': faker.email(),
} for i in range(5)]
# 批量插入
User.insert_many(fake_users).execute()

""" RETRIEVE/GET/FIND """
print("-------------RETRIEVE/GET/FIND")
user = User().select().where(User.id == 1).get()
if user.check_password(password):
    print "check password OK"

user = User().select().where(User.id != 1).get()
print(user)
user = User.select().where(User.username.contains("meet")).get()
print(user)
count = User.select().filter(User.id >= 3).count()
print(count)
users = User.select().order_by(User.email)
for u in users:
    print(u)

""" UPDATE """
print("-------------UPDATE")

effect_count = User.update({User.username: "lisi", User.email: "ls@163.com"}).where(User.id == 1).execute()
print(effect_count)

""" DELETE """
print("-------------DELETE")

effect_count = User().delete_by_id(6)
print(effect_count)
effect_count = User.delete().where(User.id >= 4).execute()
print(effect_count)
