## 概述

flask_web是一个前后端分离的后台管理系统，具备登录注册，图表管理等功能。

1. front前端使用vue技术，借鉴https://github.com/bay1/vue-admin-flask-example；
   可以通过https://github.com/taylorchen709/vue-admin进行插件的补充；
   最终框架element-ui（饿了么）
2. backend使用Python flask框架，数据库使用sqlite。

## 安装

```
// 安装前端
cd front
// npm 安装node-sass可能会报错，先使用淘宝镜像源安装
npm config set sass_binary_site https://npm.taobao.org/mirrors/node-sass/ 
npm install node-sass

PS D:\python\flask_web\front> npm install

// 安装后台
cd backend
pip install -r requirements.txt

//运行
PS D:\python\flask_web\backend> python .\manage.py
PS D:\python\flask_web\front> npm run dev

```

## 效果图

![image-20200614234935369](C:\Users\张文超\AppData\Roaming\Typora\typora-user-images\image-20200614234935369.png)

![image-20200614235054259](C:\Users\张文超\AppData\Roaming\Typora\typora-user-images\image-20200614235054259.png)

![image-20200614235120342](C:\Users\张文超\AppData\Roaming\Typora\typora-user-images\image-20200614235120342.png)

