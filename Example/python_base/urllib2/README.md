# 异常处理

<!-- vim-markdown-toc GFM -->
* [URLError 异常](#urlerror-异常)
* [HTTPError](#httperror)
* [捕获异常](#捕获异常)

<!-- vim-markdown-toc -->

当 urlopen() 不能处理响应时会引起 URLError 异常。HTTPError 异常是 URLError 的一个子类，只有在访问 HTTP 类型的 URL 时才会引起。

## URLError 异常

通常引起 URLError 的原因是：

* 无网络连接（没有到目标服务器的路由）
* 访问的目标服务器不存在

在这种情况下，异常对象会有 reason 属性（是一个（错误码、错误原因）的元组）

## HTTPError

每一个从服务器返回的 HTTP 响应都有一个状态码。其中，有的状态码表示服务器不能完成相应的请求，默认的处理程序可以为我们处理一些这样的状态码（如返回的响应是重定向，urllib2 会自动为我们从重定向后的页面中获取信息）。有些状态码，urllib2 模块不能帮我们处理，那么 urlopen 函数就会引起 HTTPError 异常，其中典型的有 404/401。
HTTPError 异常的实例有整数类型的 code 属性，表示服务器返回的错误状态码。
urllib2 模块默认的处理程序可以处理重定向（状态码是 300 范围），而且状态码在 100-299 范围内表示成功。因此，能够引起 HTTPError 异常的状态码范围是：400-599.
当引起错误时，服务器会返回 HTTP 错误码和错误页面。你可以将 HTPError 实例作为返回页面，这意味着，HTTPError 实例不仅有 code 属性，还有 read、geturl、info 等方法。

## 捕获异常

HTTPError 必须排在 URLError 的前面，因为 HTTPError 是 URLError 的子类对象，在网访问中引发的所有异常要么是 URLError 类要么是其子类，如果我们将 URLError 排在 HTTPError 的前面，那么将导致 HTTPError 异常将永远不会被触发，因为 Python 在捕获异常时是按照从前往后的顺序挨个匹配的
