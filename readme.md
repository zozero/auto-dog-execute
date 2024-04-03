<p align="center">
  <img src="./资源存放屋/auto-dog.png" alt="自动化小犬" />
</p>
<h2 align="center">自动化小犬——执行端</h2>

<h3 align="center">你的手机模拟器是你的狗子，现在请让你狗子变得成熟吧！</h3>

## 功能

- 这是自动化小犬的执行端，你可以点击[这里](https://github.com/zozero/auto-dog)，前往自动化小犬用户界面。
- 它实现了对各种行为的执行，也实现了对寻找到骨头（坐标）的方法，项目核心。
- 它拥有强有力的四肢，并且它已经经过多次更新。
- 希望它能够对你生活有所帮助。

## 安装

### 方法一

这是最简单的方法，你只需要点击下载[百度网盘]()里的`自动化小犬完整版.zip`文件就可以直接使用。

解压后双击运行`接入口.exe`，然后在双击运行`自动化小犬.exe`，最后打开你的模拟器。

如果你打算在其他地方下载的话，点击[谷歌]()。

### 方法二
下载源代码
```bash
$ git clone https://github.com/zozero/auto-dog-execute.git
```
进入目录
```bash
$ cd auto-dog-execute 
```
点击[这里]()下载已经打包的exe文件，点击[百度网盘]()，也可以下载需要的文件。

将下载好的`接入口.exe`文件复制到`auto-dog-execute`目录中，然后双击运行。默认是本地的地址：`127.0.0.1:8888`。

##### 额外

你可以打开cmd命令行，这样你可以添加两个参数，例如：`接入口.exe 127.0.0.1 8866`，其中第一个参数`127.0.0.1`是启动地址，第二个`8866`是端口。它们用空格隔开。

### 方法三
首先前往这里下载[python conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html)，直接下载这个版本<b>Anaconda Distribution installer for Windows</b>

然后前往这里[下载编辑器](https://www.jetbrains.com/pycharm/download/?section=windows)，网页下面有社区版的下载地址，我们下载的是社区版，它已经足够用了。

下载源代码
```bash
$ git clone https://github.com/zozero/auto-dog-execute.git
```
安装依赖
```bash
$ cd auto-dog-execute 
```
```bash
$ pip install -r requirements.txt
```
运行
```bash
$ uvicorn 接入口:快捷应用程序接口 --reload --port 8888
```

## 视频教程


## 文件说明

### 项目文件屋

里面存放了各个项目的文件。

每一个项目下面都有任务间、图片间、方法间、步骤间四个文件夹。

### 核心对象屋

里面包含了整个项目的精华内容。内容就不详细说明，有需要可以自行看看。

这里就不得不提一下[计算机可视化开源库（opencv）](https://docs.opencv.org/4.5.5/index.html)。很强大。

### [接入口.py](%BD%D3%C8%EB%BF%DA.py)

这个文件才是项目的入口。

拉到文件最下面，直接运行它。
当然你也可以使用unvicorn的命令来运行。
```bash
$ uvicorn 接入口:快捷应用程序接口 --reload --port 8888
```

## 分享

你可以分享你的项目，你只需要复制`项目文件屋`目录的文件夹，整个目录复制到你的好友电脑里面，在放置到`项目文件屋`里面，就可以正常使用了。


## 注意

该项目只适合个人使用，因为它没有做任何权限管理，切勿将其暴露在公网当中，尽可能在局域网内使用它。

如果非要这么做，请务必在路由器管理界面中指定来源的ip地址或者媒体存取控制位址（mac地址），这样可以直接避免未知来源的电脑访问到你的程序。（请搜索“端口转发”相关的知识。）

如果你使用的是手机，最好找一台没有任何个人信息和财产的无用手机。

## 赞助
<p align="center">
    <img src="./资源存放屋/捐赠.png" alt="捐赠" style="border-radius:50%" />
</p>  
<h3 align="center">贫穷常伴吾身，急需救援一波</h3>

## 许可证

许可证是特别的，你几乎可以无条件使用这个开源库。你可以在这里[查看](许可证)许可证。