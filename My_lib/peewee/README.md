## Peewee

<!-- vim-markdown-toc GFM -->

* [1 基本知识](#1-基本知识)
    * [1.1 字段](#11-字段)
        * [字段类型表](#字段类型表)
        * [字段初始参数](#字段初始参数)
        * [字段默认值](#字段默认值)
        * [外键字段](#外键字段)
        * [日期字段](#日期字段)
* [2 实践](#2-实践)
    * [2.1 定义 Model，建立数据库](#21-定义-model建立数据库)
        * [第一种方式：](#第一种方式)
        * [第二种方式：](#第二种方式)
    * [2.2 操作数据库](#22-操作数据库)
        * [增](#增)
        * [删](#删)
        * [改](#改)
        * [查](#查)
* [3 连接池](#3-连接池)
    * [3.1 为什么要显式的关闭连接](#31-为什么要显式的关闭连接)
    * [3.2 推荐姿势](#32-推荐姿势)
        * [手动关闭实例](#手动关闭实例)
* [4 常见问题](#4-常见问题)
    * [4.1 OperationalError: (2013, 'Lost connection to MySQL server during query')](#41-operationalerror-2013-lost-connection-to-mysql-server-during-query)
* [5 官方文档](#5-官方文档)
* [6 实践](#6-实践)
    * [6.1 user](#61-user)
* [7 源码说明](#7-源码说明)
* [8 传送门](#8-传送门)

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

### 1.1 字段


字段类用于描述模型属性到数据库字段的映射，每一个字段类型都有一个相应的 SQL 存储类型，如 `varchar`, `int`。并且 python 的数据类型和 SQL 存储类型之间的转换是透明的。

在创建模型类时，字段被定义为类属性。有一种特殊类型的字段 `ForeignKeyField`，可以以更直观的方式表示模型之间的外键关系。

```python
class Message(Model):
    user = ForeignKeyField(User, backref='messages')
    body = TextField()
    send_date = DateTimeField()
```

这允许你编写如下的代码：

```python
print(some_message.user.username)
for message in some_user.messages:
    print(message.body)
```

#### 字段类型表

|字段类型|	Sqlite	|Postgresql	|MySQL|
|-|-|-|-|
|IntegerField	|integer|	integer	|integer|
|BigIntegerField|	integer|	bigint|	bigint|
|SmallIntegerField|	integer|	smallint|	smallint|
|AutoField|	integer	|serial|	integer|
|FloatField|	real|	real|	real|
|DoubleField|	real|	double precision	|double precision|
|DecimalField|decimal|	numeric|	numeric|
|CharField|	varchar	|varchar|	varchar|
|FixedCharField|	char|	char|	char|
|TextField|	text	|text	|longtext|
|BlobField|	blob|	bytea|	blob|
|BitField|	integer	|bigint|	bigint|
|BigBitField|	blob|	bytea|	blob|
|UUIDField|	text|	uuid|	varchar(40)|
|DateTimeField|	datetime|	timestamp	|datetime|
|DateField|	date	|date|	date|
|TimeField	|time|	time|	time|
|TimestampField|	integer|	integer|	integer|
|IPField|	integer|	bigint|	bigint|
|BooleanField	|integer|	boolean|	bool|
|BareField|	untyped|	不支持|	不支持|
|ForeignKeyField|	integer	|integer|	integer|

#### 字段初始参数

所有字段类型接受的参数与默认值

+ `null = False` – 布尔值，表示是否允许存储空值
+ `index = False` – 布尔值，表示是否在此列上创建索引
+ `unique = False` – 布尔值，表示是否在此列上创建唯一索引
+ `column_name = None` – 如果和属性名不同，底层的数据库字段使用这个值
+ `default = None` – 字段默认值，可以是一个函数，将使用函数返回的值
+ `primary_key = False` – 布尔值，此字段是否是主键
+ `constraints = None` - 一个或多个约束的列表 例如：`[Check('price > 0')]`
+ `sequence = None` – 序列填充字段（如果后端数据库支持）
+ `collation = None` – 用于排序字段 / 索引的排序规则
+ `unindexed = False` – 表示虚拟表上的字段应该是未索引的（仅用于 sqlite）
+ `choices = None` – 一个可选的迭代器，包含两元数组`（value, display）`
+ `help_text = None` – 表示字段的帮助文本
+ `verbose_name = None` – 表示用户友好的字段名

一些字段的特殊参数

|字段类型|	特殊参数|
|-|-|
|CharField|	max_length|
|FixedCharField	|max_length|
|DateTimeField|	formats|
|DateField|	formats|
|TimeField|	formats|
|TimestampField	|resolution, utc|
|DecimalField|	max_digits, decimal_places, auto_round, rounding|
|ForeignKeyField	|model, field, backref, on_delete, on_update, extra|
|BareField|	coerce|


#### 字段默认值

创建对象时，peewee 可以为字段提供默认值，例如将字段的默认值`null`设置为`0`
```python
class Message(Model):
    context = TextField()
    read_count = IntegerField(default=0)
```

如果想提供一个动态值，比如当前时间，可以传入一个函数

```python
class Message(Model):
    context = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
```

数据库还可以提供字段的默认值。虽然 peewee 没有明确提供设置服务器端默认值的 API，但您可以使用 `constraints` 参数来指定服务器默认值：

```python
class Message(Model):
    context = TextField()
    timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
```

#### 外键字段

`foreignkeyfield` 是一种特殊的字段类型，允许一个模型引用另一个模型。通常外键将包含与其相关的模型的主键（但您可以通过指定一个字段来指定特定的列）。

可以通过追加 `_id` 的外键字段名称来访问原始外键值

```python
tweets = Tweet.select()
for tweet in tweets:
    # Instead of "tweet.user", we will just get the raw ID value stored
    # in the column.
    print(tweet.user_id, tweet.message)
```

`ForeignKeyField` 允许将反向引用属性绑定到目标模型。隐含地，这个属性将被命名为 `classname_set`，其中 classname 是类的小写名称，但可以通过参数覆盖 backref：

```python
class Message(Model):
    from_user = ForeignKeyField(User)
    to_user = ForeignKeyField(User, backref='received_messages')
    text = TextField()

for message in some_user.message_set:
    # We are iterating over all Messages whose from_user is some_user.
    print(message)

for message in some_user.received_messages:
    # We are iterating over all Messages whose to_user is some_user
    print(message)
```

#### 日期字段

`DateField` `TimeField` 和 `DateTimeField` 字段

`DateField` 包含 `year` `month` `day`
`TimeField` 包含 `hour` `minute` `second`
`DateTimeField` 包含以上所有

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
# 第一种方法插入单条数据
# 不会返回插入的自增 pk，而是成功返回 1，失败返回 0；
p = Person(name='liuchungui', birthday='1990-12-20', is_relative=True)
p.save()


# 第二种方法插入单条数据
# 返回值是一个 Person 对象
p = Person.create(name='liuchungui', birthday='1990-12-20', is_relative=True)

# 第三种方法插入单条数据
# 返回值是整型，职位 id
p = Person.insert(name='liuchungui', birthday='1990-12-20', is_relative=True)
```

批量写数据

```
def create():
    """批量添加数据"""
    data_source = [
        (avartar, 'Catherine', '2', pwd),
        (avartar, 'Jane', '2', pwd),
        (avartar 'Mary', '2', pwd),
    ]
    field = [User.avartar, User.uname, User.gender, User.password]
    uid = User.insert_many(data_source, field).execute()
    print('uid=%d' % uid)

```
#### 删
```
使用 delete().where().execute() 进行删除，where() 是条件，execute() 负责执行语句。若是已经查询出来的实例，则直接使用 delete_instance() 删除。
# 删除姓名为 perter 的数据
Person.delete().where(Person.name == 'perter').execute()

# 已经实例化的数据，使用 delete_instance
p = Person(name='liuchungui', birthday='1990-12-20', is_relative=False)
p.id = 1
p.save()
p.delete_instance()
```
#### 改

若是，已经添加过数据的的实例或查询到的数据实例，且表拥有 primary key 时，此时使用 save() 就是修改数据；若是未拥有实例，则使用 update().where() 进行更新数据。
```
# 已经实例化的数据，指定了 id 这个 primary key, 则此时保存就是更新数据
p = Person(name='liuchungui', birthday="1990-12-20", is_relative=False)
p.id = 1
p.save()

# 更新 birthday 数据
q = Person.update({Person.birthday: "1983-12-21"}).where(Person.name == 'liuchungui')
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
## 3 连接池

```
import db_url
mysql_config_url="mysql+pool://root:password@127.0.0.1:3306/test?max_connections=300&stale_timeout=300"
db = db_url.connect(url=mysql_config_url)
```
peewee 的连接池，使用时需要显式的关闭连接。
### 3.1 为什么要显式的关闭连接

```
def _connect(self, *args, **kwargs):
    while True:
        try:
            # Remove the oldest connection from the heap.
            ts, conn = heapq.heappop(self._connections)  # _connections 是连接实例的 list(pool)
            key = self.conn_key(conn)
        except IndexError:
            ts = conn = None
            logger.debug('No connection available in pool.')
            break
        else:
            if self._is_closed(key, conn):
                # This connecton was closed, but since it was not stale
                # it got added back to the queue of available conns. We
                # then closed it and marked it as explicitly closed, so
                # it's safe to throw it away now.
                # (Because Database.close() calls Database._close()).
                logger.debug('Connection %s was closed.', key)
                ts = conn = None
                self._closed.discard(key)
            elif self.stale_timeout and self._is_stale(ts):
                # If we are attempting to check out a stale connection,
                # then close it. We don't need to mark it in the "closed"
                # set, because it is not in the list of available conns
                # anymore.
                logger.debug('Connection %s was stale, closing.', key)
                self._close(conn, True)
                self._closed.discard(key)
                ts = conn = None
            else:
                break
    if conn is None:
        if self.max_connections and (
                len(self._in_use) >= self.max_connections):
            raise ValueError('Exceeded maximum connections.')
        conn = super(PooledDatabase, self)._connect(*args, **kwargs)
        ts = time.time()
        key = self.conn_key(conn)
        logger.debug('Created new connection %s.', key)

    self._in_use[key] = ts  # 使用中的数据库连接实例 dict
    return conn
```

根据 pool 库中的`_connect` 方法的代码可知：每次在建立数据库连接时，会检查连接实例是否超时。但是需要注意一点：使用中的数据库连接实例（_in_use dict 中的数据库连接实例），是不会在创建数据库连接时，检查是否超时的。

```
因为这段代码中，每次创建连接实例，都是在`_connections(pool)` 取实例，如果有的话就判断是否超时；如果没有的话就新建。

然而，使用中的数据库连接并不在 `_connections` 中，所以每次创建数据库连接实例时，并没有检测使用中的数据库连接实例是否超时。

只有调用连接池实例的 `_close` 方法。执行这个方法后，才会把使用后的连接实例放回到 `_connections (pool)`。
```
close 方法

```
def _close(self, conn, close_conn=False):
    key = self.conn_key(conn)
    if close_conn:
        self._closed.add(key)
        super(PooledDatabase, self)._close(conn)  # 关闭数据库连接的方法
    elif key in self._in_use:
        ts = self._in_use[key]
        del self._in_use[key]
        if self.stale_timeout and self._is_stale(ts):   # 到这里才会判断_in_use 中的连接实例是否超时
            logger.debug('Closing stale connection %s.', key)
            super(PooledDatabase, self)._close(conn)   # 超时的话，关闭数据库连接
        else:
            logger.debug('Returning %s to pool.', key)
            heapq.heappush(self._connections, (ts, conn))  # 没有超时的话，放回到 pool 中
```

如果不显式的关闭连接，会出现的问题

> * 每次都是新建数据库连接，因为 pool 中没有数据库连接实例。会导致稍微有一点并发量就会返回 Exceeded maximum connections. 错误
> * MySQL 也是有 timeout 的，如果一个连接长时间没有请求的话，MySQL Server 就会关闭这个连接，但是，peewee 的已建立的连接实例，并不知道 MySQL Server 已经关闭了，再去通过这个连接请求数据的话，就会返回 Error 2006: “MySQL server has gone away”错误

### 3.2 推荐姿势

每次操作完数据库就关闭连接实例

#### 手动关闭实例
```
 if not database.is_closed():
        database.close()

```
## 4 常见问题
### 4.1 OperationalError: (2013, 'Lost connection to MySQL server during query')

[issue](https://github.com/coleifer/peewee/issues/961)

处理方法：

目前是通过每次访问都重新创建连接解决

## 5 官方文档

[官方文档](http://docs.peewee-orm.com/en/latest/peewee/database.html#using-mysql)

## 6 实践

### 6.1 user

> ImportError: No module named dateutil //faker 使用
```
pip  install python-dateutil
```

```python

from xlib.db.peewee import *
from faker import Factory
from datetime import datetime
import xlib.db

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
    class Meta:
        database = db
        table_name = 'tb_user'
        # If Models without a Primary Key
        # primary_key = False

    def __str__(self):
        return "User(id：{} email：{} username：{} password：{} createTime: {})".format(self.id, self.email, self.username, self.password, self.createTime)


db.connect()
db.drop_tables([User])
db.create_tables([User])

""" CREATE """
print("-------------CREATE")

# 创建 User 对象
user = User.create(email="meetbill@163.com", username="meetbill", password="meet")
# 保存 User
user.save()

# 创建 faker 工厂对象
faker = Factory.create()
# 利用 faker 创建多个 User 对象
fake_users = [{
    'username': faker.name(),
    'password': faker.word(),
    'email': faker.email(),
} for i in range(5)]
# 批量插入
User.insert_many(fake_users).execute()

""" RETRIEVE/GET/FIND """
print("-------------RETRIEVE/GET/FIND")

user = User().select().where(User.id != 1).get()
print(user)
# User(id：2 email：bcalderon@hotmail.com username：Victoria Sullivan password：off createTime: 2019-08-15 23:25:59)

user = User.select().where(User.username.contains("meet")).get()
print(user)
# User(id：1 email：meetbill@163.com username：meetbill password：meet createTime: 2019-08-15 23:25:59)

count = User.select().filter(User.id >= 3).count()
print(count)
# 4

users = User.select().order_by(User.email)
for u in users:
    print(u)
"""
User(id：2 email：bcalderon@hotmail.com username：Victoria Sullivan password：off createTime: 2019-08-15 23:25:59)
User(id：6 email：evanscatherine@johnson.com username：Tracy Santiago password：you createTime: 2019-08-15 23:25:59)
User(id：1 email：meetbill@163.com username：meetbill password：meet createTime: 2019-08-15 23:25:59)
User(id：5 email：nking@yahoo.com username：Marissa Mckay password：last createTime: 2019-08-15 23:25:59)
User(id：4 email：thopkins@powers-booth.biz username：Brian Wise password：country createTime: 2019-08-15 23:25:59)
User(id：3 email：xaviercastillo@robinson.com username：Victoria Turner password：him createTime: 2019-08-15 23:25:59)
"""

""" UPDATE """
print("-------------UPDATE")

effect_count = User.update({User.username: "lisi", User.email: "ls@163.com"}).where(User.id == 1).execute()
print(effect_count)
# 1

""" DELETE """
print("-------------DELETE")

effect_count = User().delete_by_id(6)
print(effect_count)
# 1

effect_count = User.delete().where(User.id >= 4).execute()
print(effect_count)
# 2
```
结果：
```
-------------CREATE
-------------RETRIEVE/GET/FIND
User(id：2 email：bcalderon@hotmail.com username：Victoria Sullivan password：off createTime: 2019-08-15 23:25:59)
User(id：1 email：meetbill@163.com username：meetbill password：meet createTime: 2019-08-15 23:25:59)
4
User(id：2 email：bcalderon@hotmail.com username：Victoria Sullivan password：off createTime: 2019-08-15 23:25:59)
User(id：6 email：evanscatherine@johnson.com username：Tracy Santiago password：you createTime: 2019-08-15 23:25:59)
User(id：1 email：meetbill@163.com username：meetbill password：meet createTime: 2019-08-15 23:25:59)
User(id：5 email：nking@yahoo.com username：Marissa Mckay password：last createTime: 2019-08-15 23:25:59)
User(id：4 email：thopkins@powers-booth.biz username：Brian Wise password：country createTime: 2019-08-15 23:25:59)
User(id：3 email：xaviercastillo@robinson.com username：Victoria Turner password：him createTime: 2019-08-15 23:25:59)
-------------UPDATE
1
-------------DELETE
1
2
```

## 7 源码说明

> self._state = _ConnectionLocal()
```
# 属性
self.closed = True
self.conn = None
self.ctx = []
self.transactions = []

# 方法
reset(self)
set_connection(self, conn)

# 使用
操作 db.connect() 时
self._state.conn = mysql.connect(db=self.database, **self.connect_params)
```
> 执行命令时
```
db.execute 时，会执行 self.execute_sql，执行 self.execute_sql 时会先获取 self.cursor
获取 cursor 时，如果 self.autoconnect 设置的为 True，则会自动 connect
```
## 8 传送门

> * [详解 Python 数据库的 Connection、Cursor 两大对象](https://blog.csdn.net/guofeng93/article/details/53994112)
> * [ThreadLocal](https://www.liaoxuefeng.com/wiki/897692888725344/923057354442720)
