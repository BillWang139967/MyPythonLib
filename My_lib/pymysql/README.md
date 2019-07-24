### python 操作 mysql 数据库

<!-- vim-markdown-toc GFM -->

* [1 PyMySQL 安装](#1-pymysql-安装)
* [2 连接数据库](#2-连接数据库)
* [3 数据库操作](#3-数据库操作)
    * [3.1 创建数据库表](#31-创建数据库表)
    * [3.2 数据库插入操作](#32-数据库插入操作)
    * [3.3 数据库查询操作](#33-数据库查询操作)
    * [3.4 数据库更新操作](#34-数据库更新操作)
    * [3.5 删除操作](#35-删除操作)
* [4 异常](#4-异常)

<!-- vim-markdown-toc -->

## 1 PyMySQL 安装

在使用 PyMySQL 之前，我们需要确保 PyMySQL 已安装 , 我们可以使用以下命令安装最新版的 PyMySQL：

```shell
$ pip install PyMySQL
```

如果你的系统不支持 pip 命令，可以使用以下方式安装：

```shell
$ git clone https://github.com/PyMySQL/PyMySQL
$ cd PyMySQL/
$ python setup.py install
```

如果需要制定版本号，可以使用 curl 命令来安装：

```shell
$ # X.X 为 PyMySQL 的版本号
$ curl -L https://github.com/PyMySQL/PyMySQL/tarball/pymysql-X.X | tar xz
$ cd PyMySQL*
$ python setup.py install
```

## 2 连接数据库

```python
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost","root","root","test" )

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据。
data = cursor.fetchone()

print ("Database version : %s " % data)

# 关闭数据库连接
db.close()
```
## 3 数据库操作
### 3.1 创建数据库表

```python
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost","root","root","test" )

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

# 使用预处理语句创建表
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,
         SEX CHAR(1),
         INCOME FLOAT )"""

cursor.execute(sql)

# 关闭数据库连接
db.close()
```

### 3.2 数据库插入操作

```python
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost","root","root","test" )

# 使用 cursor() 方法获取操作游标
cursor = db.cursor()

# SQL 插入语句
sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
try:
   # 执行 sql 语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # 如果发生错误则回滚
   db.rollback()

# 关闭数据库连接
db.close()
```

### 3.3 数据库查询操作

Python 查询 Mysql 使用 fetchone() 方法获取单条数据，使用 fetchall() 方法获取多条数据。

```python
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost","root","root","test" )

# 使用 cursor() 方法获取操作游标
cursor = db.cursor()

# SQL 查询语句
sql = '''SELECT * FROM EMPLOYEE WHERE INCOME > 1000'''
try:
   # 执行 SQL 语句
   cursor.execute(sql)

   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      fname = row[0]
      lname = row[1]
      age = row[2]
      sex = row[3]
      income = row[4]
       # 打印结果
      print ("fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
             (fname, lname, age, sex, income ))
   """
   # 执行 SQL 语句，并接收 execute() 返回值
   print("影响了 %d 条数据" % cursor.execute(sql))
   # 获取单条记录列表，返回值是元组
   print (cursor.fetchone())
   """
except:
   print ("Error: unable to fecth data")

# 关闭数据库连接
db.close()
```

### 3.4 数据库更新操作

以下实例将 TESTDB 表中的 SEX 字段全部修改为 'M'，AGE 字段递增 1

```python
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost","root","root","test" )

# 使用 cursor() 方法获取操作游标
cursor = db.cursor()

# SQL 更新语句
sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
try:
   # 执行 SQL 语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # 发生错误时回滚
   db.rollback()

# 关闭数据库连接
db.close()
```

### 3.5 删除操作

```
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost","root","root","test" )

# 使用 cursor() 方法获取操作游标
cursor = db.cursor()

# SQL 删除语句
sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)
try:
   # 执行 SQL 语句
   cursor.execute(sql)
   # 提交修改
   db.commit()
except:
   # 发生错误时回滚
   db.rollback()

# 关闭连接
db.close()
```

## 4 异常
事务应该具有 4 个属性：原子性、一致性、隔离性、持久性。这四个属性通常称为 ACID 特性。Python DB API 2.0 的事务提供了两个方法 commit 或 rollback。

DB API 中定义了一些数据库操作的错误及异常，下表列出了这些错误和异常：

| 异常              | 描述                                                         |
| ----------------- | ------------------------------------------------------------ |
| Warning           | 当有严重警告时触发，例如插入数据是被截断等等。必须是 StandardError 的子类。 |
| Error             | 警告以外所有其他错误类。必须是 StandardError 的子类。        |
| InterfaceError    | 当有数据库接口模块本身的错误（而不是数据库的错误）发生时触发。 必须是 Error 的子类。 |
| DatabaseError     | 和数据库有关的错误发生时触发。 必须是 Error 的子类。           |
| DataError         | 当有数据处理时的错误发生时触发，例如：除零错误，数据超范围等等。 必须是 DatabaseError 的子类。 |
| OperationalError  | 指非用户控制的，而是操作数据库时发生的错误。例如：连接意外断开、 数据库名未找到、事务处理失败、内存分配错误等等操作数据库是发生的错误。 必须是 DatabaseError 的子类。 |
| IntegrityError    | 完整性相关的错误，例如外键检查失败等。必须是 DatabaseError 子类。 |
| InternalError     | 数据库的内部错误，例如游标（cursor）失效了、事务同步失败等等。 必须是 DatabaseError 子类。 |
| ProgrammingError  | 程序错误，例如数据表（table）没找到或已存在、SQL 语句语法错误、 参数数量错误等等。必须是 DatabaseError 的子类。 |
| NotSupportedError | 不支持错误，指使用了数据库不支持的函数或 API 等。例如在连接对象上 使用.rollback() 函数，然而数据库并不支持事务或者事务已关闭。 必须是 DatabaseError 的子类。 |

