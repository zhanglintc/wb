Power_wb -- 微博命令行工具
==========

## 简介：
基于 [lxyu/weibo](https://github.com/lxyu/weibo) 项目作为SDK开发的应用。安装使用需要使用Python 2.7版本。能够支持Linux/Mac/Windows平台。
运行中若报错，缺少相应的Python模块，请使用`pip`命令安装。

关于`pip`的安装，请移步[这里](https://github.com/zhanglintc/tools-lite/tree/master/misc/pip_install)。

## 下载：
- 下载最新v0.2版，点击[这里](https://zhanglintc.github.io/download/wb.zip)
- 查看历史版本：点击[这里](https://github.com/zhanglintc/xiaobawang/releases)

## 安装：

#### Linux/Mac/Windows：
克隆本项目，或者获取zip文件解压到本地后，进入你所使用的操作系统文件夹下，运行对应的`install.py`即可安装，然后就可以在命令行中使用`wb`了，具体可以参照相应系统文件夹下的`README.md`文件。

## 使用：

####简单举例：

登录微博：

    wb -a # 登录微博账户

发表微博：

    wb -p "你的微博" #发表新微博，也可以使用-t参数

查看微博：

    wb -g N # 获取最新的N条微博，默认5条

其他功能开发中，请关注更新。