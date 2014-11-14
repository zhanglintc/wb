wb -- 微博命令行工具
==========

帮助文件全面改版中，目前不保证正确性和完整性。

## 简介：
基于 [lxyu/weibo](https://github.com/lxyu/weibo) 项目作为SDK开发的应用。安装使用需要使用Python 2.7版本。能够支持Linux/Mac/Windows平台。

运行中若报错缺少相应的Python模块，请使用`pip`命令安装。

关于`pip`的安装，请移步[这里](https://github.com/zhanglintc/tools-lite/tree/master/misc/pip_install)。

## 下载：
- [下载最新版](https://zhanglintc.github.io/download/wb.zip)
- [查看历史版本](https://github.com/zhanglintc/xiaobawang/releases)

## 安装：

#### Linux/Mac/Windows：：
克隆本项目到本地，或者获取zip解压后，进入相应操作系统的文件夹下，运行`install.py`，具体可以参照对应的`README.md`

## 使用：

举例：

    wb -a

登录新浪微博

    wb -p
    wb -t

发送新微博

    wb -g

获取最新微博（默认5条，倒序）


