## 正则表达式

<!-- vim-markdown-toc GFM -->

* [1 正则表达式](#1-正则表达式)
    * [1.1 什么是正则表达式](#11-什么是正则表达式)
    * [1.2 基本匹配](#12-基本匹配)
    * [1.3 元字符](#13-元字符)
        * [1.3.1 英文句号](#131-英文句号)
        * [1.3.2 字符集](#132-字符集)
            * [否定字符集](#否定字符集)
        * [1.3.3 重复](#133-重复)
            * [星号](#星号)
            * [加号](#加号)
            * [问号](#问号)
        * [1.3.4 花括号](#134-花括号)
        * [1.3.5 字符组](#135-字符组)
        * [1.3.6 分支结构](#136-分支结构)
        * [1.3.7 转义特殊字符](#137-转义特殊字符)
        * [1.3.8 定位符](#138-定位符)
            * [插入符号](#插入符号)
            * [美元符号](#美元符号)
    * [1.4. 简写字符集](#14-简写字符集)
    * [1.5. 断言](#15-断言)
        * [1.5.1 正向先行断言](#151-正向先行断言)
        * [1.5.2 负向先行断言](#152-负向先行断言)
        * [1.5.3 正向后行断言](#153-正向后行断言)
        * [1.5.4 负向后行断言](#154-负向后行断言)
    * [1.6. 标记](#16-标记)
        * [1.6.1 不区分大小写](#161-不区分大小写)
        * [1.6.2 全局搜索](#162-全局搜索)
        * [1.6.3 多行匹配](#163-多行匹配)
    * [1.7 福利](#17-福利)
* [2 re 模块](#2-re-模块)
* [3 compile 函数](#3-compile-函数)
    * [3.1 match 方法](#31-match-方法)
    * [3.2 search 方法](#32-search-方法)
    * [3.3 findall 方法](#33-findall-方法)
    * [3.4 finditer 方法](#34-finditer-方法)
    * [3.5 split 方法](#35-split-方法)
    * [3.6 sub 方法](#36-sub-方法)
    * [3.7 subn 方法](#37-subn-方法)
* [4 其他函数](#4-其他函数)
    * [4.1 match 函数](#41-match-函数)
    * [4.2 search 函数](#42-search-函数)
    * [4.3 findall 函数](#43-findall-函数)
    * [4.4 finditer 函数](#44-finditer-函数)
    * [4.5 split 函数](#45-split-函数)
    * [4.6 sub 函数](#46-sub-函数)
    * [4.7 subn 函数](#47-subn-函数)
* [5 到底用哪种方式](#5-到底用哪种方式)
* [6 匹配中文](#6-匹配中文)
* [7 贪婪匹配](#7-贪婪匹配)
* [8 小结](#8-小结)
* [参考资料](#参考资料)

<!-- vim-markdown-toc -->

# 1 正则表达式
## 1.1 什么是正则表达式

> 正则表达式是一种被用于从文本中检索符合某些特定模式的文本。

正则表达式是从左到右来匹配一个字符串的。"Regular Expression" 这个词太长了，我们通常使用它的缩写 "regex" 或者 "regexp"。

正则表达式可以被用来替换字符串中的文本、验证表单、基于模式匹配从一个字符串中提取字符串等等。

## 1.2 基本匹配

正则表达式只是我们用于在文本中检索字母和数字的模式。例如正则表达式 `cat`，表示：字母 `c` 后面跟着一个字母 `a`，再后面跟着一个字母 `t`。

<pre>
"cat" => The <a href="#learn-regex"><strong>cat</strong></a> sat on the mat
</pre>

正则表达式 `123` 会匹配字符串 "123"。通过将正则表达式中的每个字符逐个与要匹配的字符串中的每个字符进行比较，来完成正则匹配。
正则表达式通常区分大小写，因此正则表达式 `Cat` 与字符串 "cat" 不匹配。

<pre>
"Cat" => The cat sat on the <a href="#learn-regex"><strong>Cat</strong></a>
</pre>

## 1.3 元字符

元字符是正则表达式的基本组成元素。元字符在这里跟它通常表达的意思不一样，而是以某种特殊的含义去解释。有些元字符写在方括号内的时候有特殊含义。
元字符如下：

|元字符|描述|
|:----:|----|
|.|匹配除换行符以外的任意字符。|
|[ ]|字符类，匹配方括号中包含的任意字符。|
|[^ ]|否定字符类。匹配方括号中不包含的任意字符|
|*|匹配前面的子表达式零次或多次|
|+|匹配前面的子表达式一次或多次|
|?|匹配前面的子表达式零次或一次，或指明一个非贪婪限定符。|
|{n,m}|花括号，匹配前面字符至少 n 次，但是不超过 m 次。|
|(xyz)|字符组，按照确切的顺序匹配字符 xyz。|
|&#124;|分支结构，匹配符号之前的字符或后面的字符。|
|&#92;|转义符，它可以还原元字符原来的含义，允许你匹配保留字符 <code>[ ] ( ) { } . * + ? ^ $ \ &#124;</code>|
|^|匹配行的开始|
|$|匹配行的结束|

### 1.3.1 英文句号

英文句号 `.` 是元字符的最简单的例子。元字符 `.` 可以匹配任意单个字符。它不会匹配换行符和新行的字符。例如正则表达式 `.ar`，表示：任意字符后面跟着一个字母 `a`，
再后面跟着一个字母 `r`。

<pre>
".ar" => The <a href="#learn-regex"><strong>car</strong></a> <a href="#learn-regex"><strong>par</strong></a>ked in the <a href="#learn-regex"><strong>gar</strong></a>age.
</pre>

### 1.3.2 字符集

字符集也称为字符类。方括号被用于指定字符集。使用字符集内的连字符来指定字符范围。方括号内的字符范围的顺序并不重要。
例如正则表达式 `[Tt]he`，表示：大写 `T` 或小写 `t` ，后跟字母 `h`，再后跟字母 `e`。

<pre>
"[Tt]he" => <a href="#learn-regex"><strong>The</strong></a> car parked in <a href="#learn-regex"><strong>the</strong></a> garage.
</pre>

然而，字符集中的英文句号表示它字面的含义。正则表达式 `ar[.]`，表示小写字母 `a`，后面跟着一个字母 `r`，再后面跟着一个英文句号 `.` 字符。

<pre>
"ar[.]" => A garage is a good place to park a c<a href="#learn-regex"><strong>ar.</strong></a>
</pre>

#### 否定字符集

一般来说插入字符 `^` 表示一个字符串的开始，但是当它在方括号内出现时，它会取消字符集。例如正则表达式 `[^c]ar`，表示：除了字母 `c` 以外的任意字符，后面跟着字符 `a`，
再后面跟着一个字母 `r`。

<pre>
"[^c]ar" => The car <a href="#learn-regex"><strong>par</strong></a>ked in the <a href="#learn-regex"><strong>gar</strong></a>age.
</pre>

### 1.3.3 重复

以下元字符 `+`，`*` 或 `?` 用于指定子模式可以出现多少次。这些元字符在不同情况下的作用不同。

#### 星号

该符号 `*` 表示匹配上一个匹配规则的零次或多次。正则表达式 `a*` 表示小写字母 `a` 可以重复零次或者多次。但是它如果出现在字符集或者字符类之后，它表示整个字符集的重复。
例如正则表达式 `[a-z]*`，表示：一行中可以包含任意数量的小写字母。

<pre>
"[a-z]*" => T<a href="#learn-regex"><strong>he</strong></a> <a href="#learn-regex"><strong>car</strong></a> <a href="#learn-regex"><strong>parked</strong></a> <a href="#learn-regex"><strong>in</strong></a> <a href="#learn-regex"><strong>the</strong></a> <a href="#learn-regex"><strong>garage</strong></a> #21.
</pre>

该 `*` 符号可以与元符号 `.` 用在一起，用来匹配任意字符串 `.*`。该 `*` 符号可以与空格符 `\s` 一起使用，用来匹配一串空格字符。
例如正则表达式 `\s*cat\s*`，表示：零个或多个空格，后面跟小写字母 `c`，再后面跟小写字母 `a`，再再后面跟小写字母 `t`，后面再跟零个或多个空格。

<pre>
"\s*cat\s*" => The fat<a href="#learn-regex"><strong> cat </strong></a>sat on the <a href="#learn-regex"><strong>cat</strong></a>.
</pre>

#### 加号

该符号 `+` 匹配上一个字符的一次或多次。例如正则表达式 `c.+t`，表示：一个小写字母 `c`，后跟任意数量的字符，后跟小写字母 `t`。

<pre>
"c.+t" => The fat <a href="#learn-regex"><strong>cat sat on the mat</strong></a>.
</pre>

#### 问号

在正则表达式中，元字符 `?` 用来表示前一个字符是可选的。该符号匹配前一个字符的零次或一次。
例如正则表达式 `[T]?he`，表示：可选的大写字母 `T`，后面跟小写字母 `h`，后跟小写字母 `e`。

<pre>
"[T]he" => <a href="#learn-regex"><strong>The</strong></a> car is parked in the garage.
</pre>
<pre>
"[T]?he" => <a href="#learn-regex"><strong>The</strong></a> car is parked in t<a href="#learn-regex"><strong>he</strong></a> garage.
</pre>

### 1.3.4 花括号

在正则表达式中花括号（也被称为量词 ?) 用于指定字符或一组字符可以重复的次数。例如正则表达式 `[0-9]{2,3}`，表示：匹配至少 2 位数字但不超过 3 位 (0 到 9 范围内的字符）。

<pre>
"[0-9]{2,3}" => The number was 9.<a href="#learn-regex"><strong>999</strong></a>7 but we rounded it off to <a href="#learn-regex"><strong>10</strong></a>.0.
</pre>

我们可以省略第二个数字。例如正则表达式 `[0-9]{2,}`，表示：匹配 2 个或更多个数字。如果我们也删除逗号，则正则表达式 `[0-9]{2}`，表示：匹配正好为 2 位数的数字。

<pre>
"[0-9]{2,}" => The number was 9.<a href="#learn-regex"><strong>9997</strong></a> but we rounded it off to <a href="#learn-regex"><strong>10</strong></a>.0.
</pre>

<pre>
"[0-9]{2}" => The number was 9.<a href="#learn-regex"><strong>99</strong></a><a href="#learn-regex"><strong>97</strong></a> but we rounded it off to <a href="#learn-regex"><strong>10</strong></a>.0.
</pre>

### 1.3.5 字符组

字符组是一组写在圆括号内的子模式 `(...)`。正如我们在正则表达式中讨论的那样，如果我们把一个量词放在一个字符之后，它会重复前一个字符。
但是，如果我们把量词放在一个字符组之后，它会重复整个字符组。
例如正则表达式 `(ab)*` 表示匹配零个或多个的字符串 "ab"。我们还可以在字符组中使用元字符 `|`。例如正则表达式 `(c|g|p)ar`，表示：小写字母 `c`、`g` 或 `p` 后面跟字母 `a`，后跟字母 `r`。

<pre>
"(c|g|p)ar" => The <a href="#learn-regex"><strong>car</strong></a> is <a href="#learn-regex"><strong>par</strong></a>ked in the <a href="#learn-regex"><strong>gar</strong></a>age.
</pre>

### 1.3.6 分支结构

在正则表达式中垂直条 `|` 用来定义分支结构，分支结构就像多个表达式之间的条件。现在你可能认为这个字符集和分支机构的工作方式一样。
但是字符集和分支结构巨大的区别是字符集只在字符级别上有作用，然而分支结构在表达式级别上依然可以使用。
例如正则表达式 `(T|t)he|car`，表示：大写字母 `T` 或小写字母 `t`，后面跟小写字母 `h`，后跟小写字母 `e` 或小写字母 `c`，后跟小写字母 `a`，后跟小写字母 `r`。

<pre>
"(T|t)he|car" => <a href="#learn-regex"><strong>The</strong></a> <a href="#learn-regex"><strong>car</strong></a> is parked in <a href="#learn-regex"><strong>the</strong></a> garage.
</pre>

### 1.3.7 转义特殊字符

正则表达式中使用反斜杠 `\` 来转义下一个字符。这将允许你使用保留字符来作为匹配字符 `{ } [ ] / \ + * . $ ^ | ?`。在特殊字符前面加 `\`，就可以使用它来做匹配字符。
例如正则表达式 `.` 是用来匹配除了换行符以外的任意字符。现在要在输入字符串中匹配 `.` 字符，正则表达式 `(f|c|m)at\.?`，表示：小写字母 `f`、`c` 或者 `m` 后跟小写字母 `a`，后跟小写字母 `t`，后跟可选的 `.` 字符。

<pre>
"(f|c|m)at\.?" => The <a href="#learn-regex"><strong>fat</strong></a> <a href="#learn-regex"><strong>cat</strong></a> sat on the <a href="#learn-regex"><strong>mat.</strong></a>
</pre>

### 1.3.8 定位符

在正则表达式中，为了检查匹配符号是否是起始符号或结尾符号，我们使用定位符。
定位符有两种类型：第一种类型是 `^` 检查匹配字符是否是起始字符，第二种类型是 `$`，它检查匹配字符是否是输入字符串的最后一个字符。

#### 插入符号

插入符号 `^` 符号用于检查匹配字符是否是输入字符串的第一个字符。如果我们使用正则表达式 `^a` （如果 a 是起始符号）匹配字符串 `abc`，它会匹配到 `a`。
但是如果我们使用正则表达式 `b`，它是匹配不到任何东西的，因为在字符串 `abc` 中 "b" 不是起始字符。
让我们来看看另一个正则表达式 `^(T|t)he`，这表示：大写字母 `T` 或小写字母 `t` 是输入字符串的起始符号，后面跟着小写字母 `h`，后跟小写字母 `e`。

<pre>
"(T|t)he" => <a href="#learn-regex"><strong>The</strong></a> car is parked in <a href="#learn-regex"><strong>the</strong></a> garage.
</pre>

<pre>
"^(T|t)he" => <a href="#learn-regex"><strong>The</strong></a> car is parked in the garage.
</pre>

#### 美元符号

美元 `$` 符号用于检查匹配字符是否是输入字符串的最后一个字符。例如正则表达式 `(at\.)$`，表示：小写字母 `a`，后跟小写字母 `t`，后跟一个 `.` 字符，且这个匹配器必须是字符串的结尾。

<pre>
"(at\.)" => The fat c<a href="#learn-regex"><strong>at.</strong></a> s<a href="#learn-regex"><strong>at.</strong></a> on the m<a href="#learn-regex"><strong>at.</strong></a>
</pre>

<pre>
"(at\.)$" => The fat cat sat on the m<a href="#learn-regex"><strong>at.</strong></a>
</pre>

## 1.4. 简写字符集

正则表达式为常用的字符集和常用的正则表达式提供了简写。简写字符集如下：

|简写|描述|
|:----:|----|
|.|匹配除换行符以外的任意字符|
|\w|匹配所有字母和数字的字符：`[a-zA-Z0-9_]`|
|\W|匹配非字母和数字的字符：`[^\w]`|
|\d|匹配数字：`[0-9]`|
|\D|匹配非数字：`[^\d]`|
|\s|匹配空格符：`[\t\n\f\r\p{Z}]`|
|\S|匹配非空格符：`[^\s]`|

## 1.5. 断言

后行断言和先行断言有时候被称为断言，它们是特殊类型的 ***非捕获组*** （用于匹配模式，但不包括在匹配列表中）。当我们在一种特定模式之前或者之后有这种模式时，会优先使用断言。
例如我们想获取输入字符串 `$4.44 and $10.88` 中 `$` 字符之前的所有数字。我们可以使用这个正则表达式 `(?<=\$)[0-9\.]*`，表示：获取 `$` 字符之前的所有的数字包含 `.` 字符。
以下是正则表达式中使用的断言：

|符号|描述|
|:----:|----|
|?=|正向先行断言|
|?!|负向先行断言|
|?<=|正向后行断言|
|?<!|负向后行断言|

### 1.5.1 正向先行断言

正向先行断言认为第一部分的表达式必须是先行断言表达式。返回的匹配结果仅包含与第一部分表达式匹配的文本。
要在一个括号内定义一个正向先行断言，在括号中问号和等号是这样使用的 `(?=...)`。先行断言表达式写在括号中的等号后面。
例如正则表达式 `(T|t)he(?=\sfat)`，表示：匹配大写字母 `T` 或小写字母 `t`，后面跟字母 `h`，后跟字母 `e`。
在括号中，我们定义了正向先行断言，它会引导正则表达式引擎匹配 `The` 或 `the` 后面跟着 `fat`。

<pre>
"(T|t)he(?=\sfat)" => <a href="#learn-regex"><strong>The</strong></a> fat cat sat on the mat.
</pre>

### 1.5.2 负向先行断言

当我们需要从输入字符串中获取不匹配表达式的内容时，使用负向先行断言。负向先行断言的定义跟我们定义的正向先行断言一样，
唯一的区别是不是等号 `=`，我们使用否定符号 `!`，例如 `(?!...)`。
我们来看看下面的正则表达式 `(T|t)he(?!\sfat)`，表示：从输入字符串中获取全部 `The` 或者 `the` 且不匹配 `fat` 前面加上一个空格字符。

<pre>
"(T|t)he(?!\sfat)" => The fat cat sat on <a href="#learn-regex"><strong>the</strong></a> mat.
</pre>

### 1.5.3 正向后行断言

正向后行断言是用于获取在特定模式之前的所有匹配内容。正向后行断言表示为 `(?<=...)`。例如正则表达式 `(?<=(T|t)he\s)(fat|mat)`，表示：从输入字符串中获取在单词 `The` 或 `the` 之后的所有 `fat` 和 `mat` 单词。

<pre>
"(?<=(T|t)he\s)(fat|mat)" => The <a href="#learn-regex"><strong>fat</strong></a> cat sat on the <a href="#learn-regex"><strong>mat</strong></a>.
</pre>

### 1.5.4 负向后行断言

负向后行断言是用于获取不在特定模式之前的所有匹配的内容。负向后行断言表示为 `(?<!...)`。例如正则表达式 `(?<!(T|t)he\s)(cat)`，表示：在输入字符中获取所有不在 `The` 或 `the` 之后的所有单词 `cat`。

<pre>
"(?&lt;!(T|t)he\s)(cat)" => The cat sat on <a href="#learn-regex"><strong>cat</strong></a>.
</pre>

## 1.6. 标记

标记也称为修饰符，因为它会修改正则表达式的输出。这些标志可以以任意顺序或组合使用，并且是正则表达式的一部分。

|标记|描述|
|:----:|----|
|i|不区分大小写：将匹配设置为不区分大小写。|
|g|全局搜索：搜索整个输入字符串中的所有匹配。|
|m|多行匹配：会匹配输入字符串每一行。|

### 1.6.1 不区分大小写

`i` 修饰符用于执行不区分大小写匹配。例如正则表达式 `/The/gi`，表示：大写字母 `T`，后跟小写字母 `h`，后跟字母 `e`。
但是在正则匹配结束时 `i` 标记会告诉正则表达式引擎忽略这种情况。正如你所看到的，我们还使用了 `g` 标记，因为我们要在整个输入字符串中搜索匹配。

<pre>
"The" => <a href="#learn-regex"><strong>The</strong></a> fat cat sat on the mat.
</pre>

<pre>
"/The/gi" => <a href="#learn-regex"><strong>The</strong></a> fat cat sat on <a href="#learn-regex"><strong>the</strong></a> mat.
</pre>

### 1.6.2 全局搜索

`g` 修饰符用于执行全局匹配 （会查找所有匹配，不会在查找到第一个匹配时就停止）。
例如正则表达式 `/.(at)/g`，表示：除换行符之外的任意字符，后跟小写字母 `a`，后跟小写字母 `t`。
因为我们在正则表达式的末尾使用了 `g` 标记，它会从整个输入字符串中找到每个匹配项。

<pre>
".(at)" => The <a href="#learn-regex"><strong>fat</strong></a> cat sat on the mat.
</pre>

<pre>
"/.(at)/g" => The <a href="#learn-regex"><strong>fat</strong></a> <a href="#learn-regex"><strong>cat</strong></a> <a href="#learn-regex"><strong>sat</strong></a> on the <a href="#learn-regex"><strong>mat</strong></a>.
</pre>

### 1.6.3 多行匹配

`m` 修饰符被用来执行多行的匹配。正如我们前面讨论过的 `(^, $)`，使用定位符来检查匹配字符是输入字符串开始或者结束。但是我们希望每一行都使用定位符，所以我们就使用 `m` 修饰符。
例如正则表达式 `/at(.)?$/gm`，表示：小写字母 `a`，后跟小写字母 `t`，匹配除了换行符以外任意字符零次或一次。而且因为 `m` 标记，现在正则表达式引擎匹配字符串中每一行的末尾。

<pre>
"/.at(.)?$/" => The fat
                cat sat
                on the <a href="#learn-regex"><strong>mat.</strong></a>
</pre>

<pre>
"/.at(.)?$/gm" => The <a href="#learn-regex"><strong>fat</strong></a>
                  cat <a href="#learn-regex"><strong>sat</strong></a>
                  on the <a href="#learn-regex"><strong>mat.</strong></a>
</pre>

## 1.7 福利

* *正整数*: `^\d+$`
* *负整数*: `^-\d+$`
* *电话号码*: `^+?[\d\s]{3,}$`
* *电话代码*: `^+?[\d\s]+(?[\d\s]{10,}$`
* *整数*: `^-?\d+$`
* *用户名*: `^[\w\d_.]{4,16}$`
* *字母数字字符*: `^[a-zA-Z0-9]*$`
* *带空格的字母数字字符*: `^[a-zA-Z0-9 ]*$`
* *密码*: `^(?=^.{6,}$)((?=.*[A-Za-z0-9])(?=.*[A-Z])(?=.*[a-z]))^.*$`
* *电子邮件*: `^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})*$`
* *IPv4 地址*: `^((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))*$`
* *小写字母*: `^([a-z])*$`
* *大写字母*: `^([A-Z])*$`
* *网址*: `^(((http|https|ftp):[/\/)?([[a-zA-Z0-9][-\.])+(\.)([[a-zA-Z0-9]]){2,4}([[a-zA-Z0-9][/+=%&_\.~?\-]*))*$`
* *日期 (MM/DD/YYYY)*: `^(0?[1-9]|1[012])[- /.](0?[1-9]|[12][0-9]|3[01])[- /.](19|20)?[0-9]{2}$`
* *日期 (YYYY/MM/DD)*: `^(19|20)?[0-9]{2}[- /.](0?[1-9]|1[012])[- /.](0?[1-9]|[12][0-9]|3[01])$`

# 2 re 模块

在 Python 中，我们可以使用内置的 re 模块来使用正则表达式。

有一点需要特别注意的是，正则表达式使用 `\` 对特殊字符进行转义，比如，为了匹配字符串 'python.org'，我们需要使用正则表达式 `'python\.org'`，而 Python 的字符串本身也用 `\` 转义，所以上面的正则表达式在 Python 中应该写成 `'python\\.org'`，这会很容易陷入 `\` 的困扰中，因此，我们建议使用 Python 的原始字符串，只需加一个 r 前缀，上面的正则表达式可以写成：

```
r'python\.org'
```

re 模块提供了不少有用的函数，用以匹配字符串，比如：

- compile 函数
- match 函数
- search 函数
- findall 函数
- finditer 函数
- split 函数
- sub 函数
- subn 函数

re 模块的一般使用步骤如下：

- 使用 compile 函数将正则表达式的字符串形式编译为一个 Pattern 对象
- 通过 Pattern 对象提供的一系列方法对文本进行匹配查找，获得匹配结果（一个 Match 对象）
- 最后使用 Match 对象提供的属性和方法获得信息，根据需要进行其他的操作

# 3 compile 函数

当我们在 Python 中使用正则表达式时，re 模块内部会干两件事情：

> * (1)编译正则表达式，如果正则表达式的字符串本身不合法，会报错；
> * (2)用编译后的正则表达式去匹配字符串。

如果一个正则表达式要重复使用几千次，出于效率的考虑，我们可以预编译该正则表达式，接下来重复使用时就不需要编译这个步骤了，直接匹配：

**compile 函数用于编译正则表达式，生成一个 Pattern 对象**，它的一般使用形式如下：

```
re.compile(pattern[, flag])
```

其中，pattern 是一个字符串形式的正则表达式，flag 是一个可选参数，表示匹配模式，比如忽略大小写，多行模式等。

下面，让我们看看例子。

```python
import re

# 将正则表达式编译成 Pattern 对象
pattern = re.compile(r'\d+')
```

在上面，我们已将一个正则表达式编译成 Pattern 对象，接下来，我们就可以利用 pattern 的一系列方法对文本进行匹配查找了。Pattern 对象的一些常用方法主要有：

- match 方法
- search 方法
- findall 方法
- finditer 方法
- split 方法
- sub 方法
- subn 方法

## 3.1 match 方法

match 方法用于查找字符串的头部（也可以指定起始位置），它是一次匹配，只要找到了一个匹配的结果就返回，而不是查找所有匹配的结果。它的一般使用形式如下：

```
match(string[, pos[, endpos]])
```

其中，string 是待匹配的字符串，pos 和 endpos 是可选参数，指定字符串的起始和终点位置，默认值分别是 0 和 len （字符串长度）。因此，**当你不指定 pos 和 endpos 时，match 方法默认匹配字符串的头部**。

当匹配成功时，返回一个 Match 对象，如果没有匹配上，则返回 None。

看看例子。

```python
>>> import re
>>> pattern = re.compile(r'\d+')                    # 用于匹配至少一个数字
>>> m = pattern.match('one12twothree34four')        # 查找头部，没有匹配
>>> print m
None
>>> m = pattern.match('one12twothree34four', 2, 10) # 从'e'的位置开始匹配，没有匹配
>>> print m
None
>>> m = pattern.match('one12twothree34four', 3, 10) # 从'1'的位置开始匹配，正好匹配
>>> print m                                         # 返回一个 Match 对象
<_sre.SRE_Match object at 0x10a42aac0>
>>> m.group(0)   # 可省略 0
'12'
>>> m.start(0)   # 可省略 0
3
>>> m.end(0)     # 可省略 0
5
>>> m.span(0)    # 可省略 0
(3, 5)
```

在上面，当匹配成功时返回一个 Match 对象，其中：

- `group([group1, …])` 方法用于获得一个或多个分组匹配的字符串，当要获得整个匹配的子串时，可直接使用 `group()` 或 `group(0)`；
- `start([group])` 方法用于获取分组匹配的子串在整个字符串中的起始位置（子串第一个字符的索引），参数默认值为 0；
- `end([group])` 方法用于获取分组匹配的子串在整个字符串中的结束位置（子串最后一个字符的索引 +1），参数默认值为 0；
- `span([group])` 方法返回 `(start(group), end(group))`。

再看看一个例子：

```python
>>> import re
>>> pattern = re.compile(r'([a-z]+) ([a-z]+)', re.I)   # re.I 表示忽略大小写
>>> m = pattern.match('Hello World Wide Web')
>>> print m                               # 匹配成功，返回一个 Match 对象
<_sre.SRE_Match object at 0x10bea83e8>
>>> m.group(0)                            # 返回匹配成功的整个子串
'Hello World'
>>> m.span(0)                             # 返回匹配成功的整个子串的索引
(0, 11)
>>> m.group(1)                            # 返回第一个分组匹配成功的子串
'Hello'
>>> m.span(1)                             # 返回第一个分组匹配成功的子串的索引
(0, 5)
>>> m.group(2)                            # 返回第二个分组匹配成功的子串
'World'
>>> m.span(2)                             # 返回第二个分组匹配成功的子串
(6, 11)
>>> m.groups()                            # 等价于 (m.group(1), m.group(2), ...)
('Hello', 'World')
>>> m.group(3)                            # 不存在第三个分组
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: no such group
```

## 3.2 search 方法

search 方法用于查找字符串的任何位置，它也是一次匹配，只要找到了一个匹配的结果就返回，而不是查找所有匹配的结果，它的一般使用形式如下：

```
search(string[, pos[, endpos]])
```

其中，string 是待匹配的字符串，pos 和 endpos 是可选参数，指定字符串的起始和终点位置，默认值分别是 0 和 len （字符串长度）。

当匹配成功时，返回一个 Match 对象，如果没有匹配上，则返回 None。

让我们看看例子：

```python
>>> import re
>>> pattern = re.compile('\d+')
>>> m = pattern.search('one12twothree34four')  # 这里如果使用 match 方法则不匹配
>>> m
<_sre.SRE_Match object at 0x10cc03ac0>
>>> m.group()
'12'
>>> m = pattern.search('one12twothree34four', 10, 30)  # 指定字符串区间
>>> m
<_sre.SRE_Match object at 0x10cc03b28>
>>> m.group()
'34'
>>> m.span()
(13, 15)
```

再来看一个例子：

```python
# -*- coding: utf-8 -*-

import re

# 将正则表达式编译成 Pattern 对象
pattern = re.compile(r'\d+')

# 使用 search() 查找匹配的子串，不存在匹配的子串时将返回 None
# 这里使用 match() 无法成功匹配
m = pattern.search('hello 123456 789')

if m:
    # 使用 Match 获得分组信息
    print 'matching string:',m.group()
    print 'position:',m.span()
```

执行结果：

```
matching string: 123456
position: (6, 12)
```

## 3.3 findall 方法

上面的 match 和 search 方法都是一次匹配，只要找到了一个匹配的结果就返回。然而，在大多数时候，我们需要搜索整个字符串，获得所有匹配的结果。

findall 方法的使用形式如下：

```
findall(string[, pos[, endpos]])
```

其中，string 是待匹配的字符串，pos 和 endpos 是可选参数，指定字符串的起始和终点位置，默认值分别是 0 和 len （字符串长度）。

findall 以列表形式返回全部能匹配的子串，如果没有匹配，则返回一个空列表。

看看例子：

```python
import re

pattern = re.compile(r'\d+')   # 查找数字
result1 = pattern.findall('hello 123456 789')
result2 = pattern.findall('one1two2three3four4', 0, 10)

print result1
print result2
```

执行结果：

```
['123456', '789']
['1', '2']
```

## 3.4 finditer 方法

finditer 方法的行为跟 findall 的行为类似，也是搜索整个字符串，获得所有匹配的结果。但它返回一个顺序访问每一个匹配结果（Match 对象）的迭代器。

看看例子：

```python
# -*- coding: utf-8 -*-

import re

pattern = re.compile(r'\d+')

result_iter1 = pattern.finditer('hello 123456 789')
result_iter2 = pattern.finditer('one1two2three3four4', 0, 10)

print type(result_iter1)
print type(result_iter2)

print 'result1...'
for m1 in result_iter1:   # m1 是 Match 对象
    print 'matching string: {}, position: {}'.format(m1.group(), m1.span())

print 'result2...'
for m2 in result_iter2:
    print 'matching string: {}, position: {}'.format(m2.group(), m2.span())
```

执行结果：

```
<type 'callable-iterator'>
<type 'callable-iterator'>
result1...
matching string: 123456, position: (6, 12)
matching string: 789, position: (13, 16)
result2...
matching string: 1, position: (3, 4)
matching string: 2, position: (7, 8)
```

## 3.5 split 方法

split 方法按照能够匹配的子串将字符串分割后返回列表，它的使用形式如下：

```
split(string[, maxsplit])
```

其中，maxsplit 用于指定最大分割次数，不指定将全部分割。

看看例子：

```python
import re

p = re.compile(r'[\s\,\;]+')
print p.split('a,b;; c   d')
```

执行结果：

```
['a', 'b', 'c', 'd']
```

## 3.6 sub 方法

sub 方法用于替换。它的使用形式如下：

```
sub(repl, string[, count])
```

其中，repl 可以是字符串也可以是一个函数：

- 如果 repl 是字符串，则会使用 repl 去替换字符串每一个匹配的子串，并返回替换后的字符串，另外，repl 还可以使用 `\id` 的形式来引用分组，但不能使用编号 0；
- 如果 repl 是函数，这个方法应当只接受一个参数（Match 对象），并返回一个字符串用于替换（返回的字符串中不能再引用分组）。

count 用于指定最多替换次数，不指定时全部替换。

看看例子：

```python
import re

p = re.compile(r'(\w+) (\w+)')
s = 'hello 123, hello 456'

def func(m):
    return 'hi' + ' ' + m.group(2)

print p.sub(r'hello world', s)  # 使用 'hello world' 替换 'hello 123' 和 'hello 456'
print p.sub(r'\2 \1', s)        # 引用分组
print p.sub(func, s)
print p.sub(func, s, 1)         # 最多替换一次
```

执行结果：

```
hello world, hello world
123 hello, 456 hello
hi 123, hi 456
hi 123, hello 456
```

## 3.7 subn 方法

subn 方法跟 sub 方法的行为类似，也用于替换。它的使用形式如下：

```
subn(repl, string[, count])
```

它返回一个元组：

```
(sub(repl, string[, count]), 替换次数）
```

元组有两个元素，第一个元素是使用 sub 方法的结果，第二个元素返回原字符串被替换的次数。

看看例子：

```
import re

p = re.compile(r'(\w+) (\w+)')
s = 'hello 123, hello 456'

def func(m):
    return 'hi' + ' ' + m.group(2)

print p.subn(r'hello world', s)
print p.subn(r'\2 \1', s)
print p.subn(func, s)
print p.subn(func, s, 1)
```

执行结果：

```
('hello world, hello world', 2)
('123 hello, 456 hello', 2)
('hi 123, hi 456', 2)
('hi 123, hello 456', 1)
```

# 4 其他函数

事实上，使用 compile 函数生成的 Pattern 对象的一系列方法跟 re 模块的多数函数是对应的，但在使用上有细微差别。

## 4.1 match 函数

match 函数的使用形式如下：

```
re.match(pattern, string[, flags]):
```

其中，pattern 是正则表达式的字符串形式，比如 `\d+`, `[a-z]+`。

而 Pattern 对象的 match 方法使用形式是：

```
match(string[, pos[, endpos]])
```

可以看到，match 函数不能指定字符串的区间，它只能搜索头部，看看例子：

```python
import re

m1 = re.match(r'\d+', 'One12twothree34four')
if m1:
    print 'matching string:',m1.group()
else:
    print 'm1 is:',m1

m2 = re.match(r'\d+', '12twothree34four')
if m2:
    print 'matching string:', m2.group()
else:
    print 'm2 is:',m2
```

执行结果：

```
m1 is: None
matching string: 12
```

## 4.2 search 函数

search 函数的使用形式如下：

```
re.search(pattern, string[, flags])
```

search 函数不能指定字符串的搜索区间，用法跟 Pattern 对象的 search 方法类似。

## 4.3 findall 函数

findall 函数的使用形式如下：

```
re.findall(pattern, string[, flags])
```

findall 函数不能指定字符串的搜索区间，用法跟 Pattern 对象的 findall 方法类似。

看看例子：

```python
import re

print re.findall(r'\d+', 'hello 12345 789')

# 输出
['12345', '789']
```

## 4.4 finditer 函数

finditer 函数的使用方法跟 Pattern 的 finditer 方法类似，形式如下：

```
re.finditer(pattern, string[, flags])
```

## 4.5 split 函数

split 函数的使用形式如下：

```
re.split(pattern, string[, maxsplit])
```

## 4.6 sub 函数

sub 函数的使用形式如下：

```
re.sub(pattern, repl, string[, count])
```

## 4.7 subn 函数

subn 函数的使用形式如下：

```
re.subn(pattern, repl, string[, count])
```

# 5 到底用哪种方式

从上文可以看到，使用 re 模块有两种方式：

- 使用 re.compile 函数生成一个 Pattern 对象，然后使用 Pattern 对象的一系列方法对文本进行匹配查找；
- 直接使用 re.match, re.search 和 re.findall 等函数直接对文本匹配查找；

下面，我们用一个例子展示这两种方法。

先看第 1 种用法：

```python
import re

# 将正则表达式先编译成 Pattern 对象
pattern = re.compile(r'\d+')

print pattern.match('123, 123')
print pattern.search('234, 234')
print pattern.findall('345, 345')
```

再看第 2 种用法：

```python
import re

print re.match(r'\d+', '123, 123')
print re.search(r'\d+', '234, 234')
print re.findall(r'\d+', '345, 345')
```

如果一个正则表达式需要用到多次（比如上面的 `\d+`），在多种场合经常需要被用到，出于效率的考虑，我们应该预先编译该正则表达式，生成一个 Pattern 对象，再使用该对象的一系列方法对需要匹配的文件进行匹配；而如果直接使用 re.match, re.search 等函数，每次传入一个正则表达式，它都会被编译一次，效率就会大打折扣。

因此，我们推荐使用第 1 种用法。

# 6 匹配中文

在某些情况下，我们想匹配文本中的汉字，有一点需要注意的是，[中文的 unicode 编码范围](http://blog.oasisfeng.com/2006/10/19/full-cjk-unicode-range/) 主要在 `[\u4e00-\u9fa5]`，这里说主要是因为这个范围并不完整，比如没有包括全角（中文）标点，不过，在大部分情况下，应该是够用的。

假设现在想把字符串 `title = u'你好，hello，世界'` 中的中文提取出来，可以这么做：

```python
# -*- coding: utf-8 -*-

import re

title = u'你好，hello，世界'
pattern = re.compile(ur'[\u4e00-\u9fa5]+')
result = pattern.findall(title)

print result
```

注意到，我们在正则表达式前面加上了两个前缀 `ur`，其中 `r` 表示使用原始字符串，`u` 表示是 unicode 字符串。

执行结果：

```
[u'\u4f60\u597d', u'\u4e16\u754c']
```

# 7 贪婪匹配

在 Python 中，正则匹配默认是**贪婪匹配**（在少数语言中可能是非贪婪），也就是**匹配尽可能多的字符**。

比如，我们想找出字符串中的所有 `div` 块：

```python
import re

content = 'aa<div>test1</div>bb<div>test2</div>cc'
pattern = re.compile(r'<div>.*</div>')
result = pattern.findall(content)

print result
```

执行结果：

```
['<div>test1</div>bb<div>test2</div>']
```

由于正则匹配是贪婪匹配，也就是尽可能多的匹配，因此，在成功匹配到第一个 `</div>` 时，它还会向右尝试匹配，查看是否还有更长的可以成功匹配的子串。

如果我们想非贪婪匹配，可以加一个 `?`，如下：

```python
import re

content = 'aa<div>test1</div>bb<div>test2</div>cc'
pattern = re.compile(r'<div>.*?</div>')    # 加上 ?
result = pattern.findall(content)

print result
```

结果：

```
['<div>test1</div>', '<div>test2</div>']
```

# 8 小结

- re 模块的一般使用步骤如下：
    - 使用 compile 函数将正则表达式的字符串形式编译为一个 Pattern 对象；
    - 通过 Pattern 对象提供的一系列方法对文本进行匹配查找，获得匹配结果（一个 Match 对象）；
    - 最后使用 Match 对象提供的属性和方法获得信息，根据需要进行其他的操作；
- Python 的正则匹配默认是贪婪匹配。

# 参考资料

- [Python 正则表达式指南](http://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html)
- [正则表达式 - 廖雪峰的官方网站](http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832260566c26442c671fa489ebc6fe85badda25cd000)


