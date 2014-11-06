wb -- 微博命令行工具
==========

帮助文件全面改版中，目前不保证正确性和完整性。

## 简介：
基于 [lxyu/weibo](https://github.com/lxyu/weibo) 项目作为SDK开发的应用。安装使用需要使用Python 2.7版本。能够支持Linux/Mac/Windows平台。

## 下载：
- [下载最新版](https://zhanglintc.github.io/download/xiaobawang.zip)（过旧）
- [查看历史版本](https://github.com/zhanglintc/xiaobawang/releases)（过旧）

## 使用：

#### Linux/Mac：
克隆本项目到本地，或者获取zip解压后，使用命令：
    
    python wb.py -option argument

通过命令行来使用本工具。

为了方便，可以使用`alias`命令来为本项目设置别名，例如：

    alias python wb.py wb
    
然后将此`alias`存入`~/.bash_profile`，这样以后就可以直接调用`wb`了。

#### Windows：
同样克隆被项目或者获取zip解压到本地后，使用命令：
    
    python wb.py -option argument

来调用本工具。

鉴于Windows没有别名功能，在Windows下可以使用`wb.cmd`来调用本工具。将文件最后一行：

    python wb.py %parameter%
    
中的`wb.py`配置为相应的绝对路径，然后将`wb.cmd`放置到系统的任何一个`PATH`路径下，也就能够像Linux/Mac一样直接使用`wb`命令使用本工具了。

## 补充：
我正在想。。。