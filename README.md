wb -- 微博命令行工具
==========

## 简介：
基于 [lxyu/weibo](https://github.com/lxyu/weibo) 项目作为SDK开发的应用. 安装使用前请**确保**本机安装有[Python 2.7.x](https://www.python.org/downloads/), 而不是Python 3.x.x.

能够支持**Linux/Mac/Windows**平台. 运行中若报错, 缺少相应的Python模块, 请使用`pip`命令安装.

关于`pip`的安装, 请移步[这里](https://github.com/zhanglintc/tools-lite/tree/master/misc/pip_install).

**2015.01.08** `setup.py`已经添加依靠`./bin/pip.exe`以及`./requirements.txt`自动下载依赖模块的功能, 以期实现全自动安装.

## 下载：
- 下载最新v0.2版, 点击[这里](https://zhanglintc.github.io/download/wb.zip)
- 查看历史版本：点击[这里](https://github.com/zhanglintc/xiaobawang/releases)

## 安装：

#### Linux/Mac/Windows：
克隆本项目到本地, 或者获取zip文件解压到本地后, 使用命令`python setup.py`即可安装, 然后在命令行中输入`wb`, 若出现相应提示即表明安装成功.

## 使用：

```
    wb -a               # 登录微博账户
    wb -d               # 删除登录信息
    wb -c N             # 获取最新的N条微博, 默认5条
    wb -g N             # 获取最新的N条微博, 默认5条
    wb -p "微博内容"     # 发表新微博, 也可以使用-t参数
    wb -r N "回复内容"   # 回复屏幕显示的第N条微博(或回复), 使用该命令前请务必先使用wb -c或wb - g功能
    wb -h               # 获取帮助信息
```

其他功能开发中, 敬请关注更新.


