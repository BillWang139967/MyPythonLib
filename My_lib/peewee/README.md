## Peewee

<!-- vim-markdown-toc GFM -->

* [1 基本知识](#1-基本知识)
* [2 实践](#2-实践)
    * [2.1 定义 Model，建立数据库](#21-定义-model建立数据库)
        * [第一种方式：](#第一种方式)
        * [第二种方式：](#第二种方式)
    * [2.2 操作数据库](#22-操作数据库)
        * [增](#增)
        * [删](#删)
        * [改](#改)
        * [查](#查)
* [3 常见问题](#3-常见问题)
    * [3.1 OperationalError: (2013, 'Lost connection to MySQL server during query')](#31-operationalerror-2013-lost-connection-to-mysql-server-during-query)
* [4 官方文档](#4-官方文档)

<!-- vim-markdown-toc -->
Peewee 是一个简单小巧的 Python ORM，它非常容易学习，并且使用起来很直观。

如果想快速入门，请参考官方的 [quickstart](http://docs.peewee-orm.com/en/latest/peewee/quickstart.html#quickstart)

[源码](https://github.com/coleifer/peewee)

## 1 基本知识

在官方的 Quckstart 中，我了解到，Peewee 中 Model 类、fields 和 model 实例与数据库的映射关系如下：

|Object	|Corresponds to…|
|:-:|---|
|Model |class	Database table|
|Field |instance	Column on a table|
|Model |instance	Row in a database table|

也就是说

> * 一个 Model 类代表一个数据库的表
> * 一个 Field 字段代表数据库中的一个字段
> * 一个 model 类实例化对象则代表数据库中的一行。

Peewee 的实现原理可以结合 [道生一，一生二，二生三，三生万物](https://github.com/meetbill/redis-orm/wiki/metaclass)

## 2 实践

而使用过程，分成两步：

> * 定义 Model，建立数据库
> * 操作数据库

### 2.1 定义 Model，建立数据库

在使用的时候，根据需求先定义好 Model，然后可以通过 create_tables() 创建表，若是已经创建好数据库表了，可以通过 python -m pwiz 脚本工具直接创建 Model。

#### 第一种方式：

先定义 Model，然后通过 db.create_tables() 创建或 Model.create_table() 创建表。
例如，我们需要建一个 Person 表，里面有 name、birthday 和 is_relative 三个字段，我们定义的 Model 如下：
```
from peewee import *

# 连接数据库
database = MySQLDatabase('test', user='root', host='localhost', port=3306)

# 定义 Person
class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = database
```

然后，我们就可以创建表了
```
# 创建表
Person.create_table()

# 创建表也可以这样，可以创建多个
# database.create_tables([Person])
```
其中，CharField、DateField、BooleanField 等这些类型与数据库中的数据类型一一对应，我们直接使用它就行，至于 CharField => varchar(255) 这种转换 Peewee 已经为我们做好了 。

完成之后，就会在数据库中看到 test 数据库中，创建好了 person 表
```
mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| person         |
+----------------+
1 rows in set (0.00 sec)

mysql> desc person;
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| id          | int(11)      | NO   | PRI | NULL    | auto_increment |
| name        | varchar(255) | NO   |     | NULL    |                |
| birthday    | date         | NO   |     | NULL    |                |
| is_relative | tinyint(1)   | NO   |     | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+
```

```
如果使用 autoconnect = True（默认值）初始化数据库，则在使用数据库之前无需显式连接到数据库。 明确地管理连接被认为是最佳实践，因此可以考虑禁用自动连接行为。
```
#### 第二种方式：
已经存在过数据库，则直接通过 python -m pwiz 批量创建 Model。

例如，上面我已经创建好了 test 库，并且创建了 person 表，表中拥有 id、name、birthday 和 is_relative 字段。那么，我可以使用下面命令：
```
# 查看参数
python -m pwiz

# 指定 mysql，用户为 root，host 为 localhost，数据库为 test
python -m pwiz -e mysql -u root -H localhost -p 3306 --password test > testModel.py
```

然后，输入密码，pwiz 脚本会自动创建 Model，内容如下：
```
from peewee import *

database = MySQLDatabase('test', **{'charset': 'utf8', 'use_unicode': True, 'host': 'localhost', 'user': 'root', 'password': ''})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Person(BaseModel):
    birthday = DateField()
    is_relative = IntegerField()
    name = CharField()

    class Meta:
        table_name = 'person'

```

### 2.2 操作数据库

操作数据库，就是增、删、改和查。
#### 增
直接创建示例，然后使用 save() 就添加了一条新数据
```
# 添加一条数据
p = Person(name='liuchungui', birthday=date(1990, 12, 20), is_relative=True)
p.save()
```

#### 删
```
使用 delete().where().execute() 进行删除，where() 是条件，execute() 负责执行语句。若是已经查询出来的实例，则直接使用 delete_instance() 删除。
# 删除姓名为 perter 的数据
Person.delete().where(Person.name == 'perter').execute()

# 已经实例化的数据，使用 delete_instance
p = Person(name='liuchungui', birthday=date(1990, 12, 20), is_relative=False)
p.id = 1
p.save()
p.delete_instance()
```
#### 改

若是，已经添加过数据的的实例或查询到的数据实例，且表拥有 primary key 时，此时使用 save() 就是修改数据；若是未拥有实例，则使用 update().where() 进行更新数据。
```
# 已经实例化的数据，指定了 id 这个 primary key, 则此时保存就是更新数据
p = Person(name='liuchungui', birthday=date(1990, 12, 20), is_relative=False)
p.id = 1
p.save()

# 更新 birthday 数据
q = Person.update({Person.birthday: date(1983, 12, 21)}).where(Person.name == 'liuchungui')
q.execute()
```
#### 查
单条数据使用 Person.get() 就行了，也可以使用 Person.select().where().get()。若是查询多条数据，则使用 Person.select().where()，去掉 get() 就行了。语法很直观，select() 就是查询，where 是条件，get 是获取第一条数据。
```
# 查询单条数据
p = Person.get(Person.name == 'liuchungui')
print(p.name, p.birthday, p.is_relative)

# 使用 where().get() 查询
p = Person.select().where(Person.name == 'liuchungui').get()
print(p.name, p.birthday, p.is_relative)

# 查询多条数据
persons = Person.select().where(Person.is_relative == True)
for p in persons:
    print(p.name, p.birthday, p.is_relative)
```
## 3 常见问题
### 3.1 OperationalError: (2013, 'Lost connection to MySQL server during query')

[issue](https://github.com/coleifer/peewee/issues/961)

处理方法：

目前是通过每次访问都重新创建连接解决

## 4 官方文档

[官方文档](http://docs.peewee-orm.com/en/latest/peewee/database.html#using-mysql)
