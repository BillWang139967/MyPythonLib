## validator


<!-- vim-markdown-toc GFM -->

* [1 功能](#1-功能)
* [2 同类软件](#2-同类软件)
* [3 使用方法](#3-使用方法)
* [4 方法说明](#4-方法说明)

<!-- vim-markdown-toc -->

## 1 功能

参数校验

[validator](https://github.com/mansam/validator.py)

## 2 同类软件

> * https://github.com/keleshev/schema
> * https://github.com/kvesteri/validators

## 3 使用方法

```
from validator import Required, Not, Truthy, Blank, Range, Equals, In, validate

# let's say that my dictionary needs to meet the following rules...
rules = {
    "foo": [Required, Equals(123)],
    "bar": [Required, Truthy()],
    "baz": [In(["spam", "eggs", "bacon"])],
    "qux": [Not(Range(1, 100))] # by default, Range is inclusive
}

# then this following dict would pass:
passes = {
    "foo": 123,
    "bar": True, # or a non-empty string, or a non-zero int, etc...
    "baz": "spam",
    "qux": 101
}
print validate(rules, passes)
# (True, {})

# but this one would fail
fails = {
    "foo": 321,
    "bar": False, # or 0, or [], or an empty string, etc...
    "baz": "barf",
    "qux": 99
}
print validate(rules, fails)
# (False,
#  {
#  'foo': ["must be equal to '123'"],
#  'bar': ['must be True-equivalent value'],
#  'baz': ["must be one of ['spam', 'eggs', 'bacon']"],
#  'qux': ['must not fall between 1 and 100']
#  })
```

## 4 方法说明

> * key 检查
>   * Required
> * value 检查
>   * 常规
>     * In: 检查 value 是否在给的列表中，如：`"field": [In([1, 2, 3])]`
>     * Truthy: 检查  value 是否有值或为 Ture，如：`"field": [Truthy()]`
>     * Not: 检测 value 不在所给的条件中
>     * Equals: 检查 value 是否为某值，如：`Equals`
>   * 数字
>     * GreaterThan: 检查 value 是否 > 某数字，如：`"field": [GreaterThan(10)]`
>     * Range：检查 self.start <= value <= self.end，如：`"field": [Range(0, 10)]`
>   * 字符串
>     * Blank: 检查 value 是否为`''`,如：`"field": [Blank()]`
>     * Length：字符串长度是否在所给条件之间，如：`"field": [Length(0, maximum=5)]`
>     * Contains：字符串中是否有某个字符串，如：`"field": [Contains("test")]`
>   * 列表
>     * Contains：列表中是否有某个元素，如：`"field": [Contains(3)]`
