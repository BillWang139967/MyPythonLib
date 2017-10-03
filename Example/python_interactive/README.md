## Python 交互式解释器自动补全

在使用 Python 解释器的时候由于有太多的内置函数，如果没有自动补全功能会给我们带来很大程度的不便。
通过在编辑一个文件有以下内容文件名~/.pythonstartup.py

```
import readline, rlcompleter
readline.parse_and_bind("tab: complete")
```

这样我们再~/.bashrc 文件中添加
export PYTHONSTARTUP=~/.pythonstartup.py
就可以让以后我们打开 python 交互式解释器的时候可以自动加载上面的语句。
方便以后的交互式操作。

操作方法
```
#curl -o pythonstartup.sh https://raw.githubusercontent.com/BillWang139967/MyPythonLib/master/Example/python_interactive/pythonstartup.sh
#sh pythonstartup.sh
#. ~/.bashrc
```

