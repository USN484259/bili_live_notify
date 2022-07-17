# Bilibili Live Notifier

Show notification when given live room on Bilibili starts streaming.  
写Bug的时候如果有主播开播了，就弹个通知提醒一下

### 环境 & 依赖
* Ubuntu 20.04.4 LTS
* Python 3.8
* python-gobject
* bilibili-api

### 安装 & 运行
```
sudo apt install python3
sudo apt install python-gobject
pip install bilibili_api
python3 bili_live_notify.py <live-room listing filepath> [check interval]
```

### 其他
1. 老是因为埋头写代码，错过一些直播
2. 前段时间通过DD_Monitor项目了解到bilibili-api项目
3. 于是一晚上时间整出来了这东西
4. 不会python，现查语法，能用就行，大家看着图一乐

### 引用 & 参考
* https://www.python.org
* https://bili.moyu.moe
* https://www.devdungeon.com/content/desktop-notifications-linux-python
