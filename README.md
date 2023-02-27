# 实验数据处理脚本使用说明

<cneter>

|版本号|创建时间|更改说明|编辑人|
|:---:|:---:|:---:|:---:|
|v1.0|2023.02.24|文档创建||

</center>

相关版本依赖：

|说明文档|批处理脚本|主程序|
|:---:|:---:|:---:|
|实验数据处理脚本(v1.0)|startup.bat(v1.0)|main.py(v1.0)|

<div STYLE="page-break-after:always;"></div>


<!-- TOC -->

- [实验数据处理脚本使用说明](#%E5%AE%9E%E9%AA%8C%E6%95%B0%E6%8D%AE%E5%A4%84%E7%90%86%E8%84%9A%E6%9C%AC%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)
    - [一.环境安装](#%E4%B8%80%E7%8E%AF%E5%A2%83%E5%AE%89%E8%A3%85)
        - [软件及版本要求](#%E8%BD%AF%E4%BB%B6%E5%8F%8A%E7%89%88%E6%9C%AC%E8%A6%81%E6%B1%82)
        - [软件安装](#%E8%BD%AF%E4%BB%B6%E5%AE%89%E8%A3%85)
    - [二.程序运行](#%E4%BA%8C%E7%A8%8B%E5%BA%8F%E8%BF%90%E8%A1%8C)
    - [三.输出说明](#%E4%B8%89%E8%BE%93%E5%87%BA%E8%AF%B4%E6%98%8E)

<!-- /TOC -->

## 一.环境安装

### 1.软件及版本要求

|软件|版本|备注|
|:---:|:---:|:---:|
|windows|7,8,10,11|除非古董机否则默认电脑及系统均为x64|
|python|3.x||
|pip||使用最新版本|

1. 下载[python-3.8.5-amd64.exe](https://www.python.org/ftp/python/3.8.5/python-3.8.5-amd64.exe)
2. 下载[pip-23.0.1.tar.gz](https://files.pythonhosted.org/packages/6b/8b/0b16094553ecc680e43ded8f920c3873b01b1da79a54274c98f08cb29fca/pip-23.0.1.tar.gz)

### 2.软件安装

#### 1. 安装python3.8.5

别急着点完成，提前说一声图省事**务必勾选Add to PATH**。

双击`python-3.8.5-amd64.exe`，一步一步装就行了。

装好之后，按`win+R`在运行框中输入`cmd`进入控制台，输入`python --version`，如果显示python及3.8.5版本信息，说明python安装完成，如果显示未找到python，大概率是没有勾选Add to PATH，自行百度`python 添加环境变量`。

#### 2. 安装pip包管理器

解压下载的`pip-23.0.1.tar.gz`，假设解压路径为`D:\software\pip-23.0.1`（setup.py文件所在目录）。

在控制台输入以下命令进行安装：

```bat
cd /d D:\software\pip-23.0.1
python setup.py install
```

#### 3. 安装依赖包

在控制台输入以下命令安装：

```bat
pip install numpy -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple
pip install matplotlib -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple
pip install scipy -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com/simple
```

## 二.程序运行

程序运行有以下几点要求：

1. 数据文件名应当按a.b.txt格式命名，其中a代表第a组，a相同的文件数据会画在同一张图，a和b均为数字；
2. 数据文件应当在同一个文件夹下；
3. 脚本所在文件夹script应当与数据文件夹在同级目录。

例如以下目录结构：

```
├── 1224                        #数据所在文件夹
│   ├── 1.1.txt                 #数据文件
│   ├── l.2.txt
│   ├── ...
│   ├── 16.8.txt
│   └── 16.9.txt
├── 1224_out                    #输出数据所在文件夹
│   ├── 1.1.txt                 #输出数据文件
│   ├── l.2.txt
│   ├── ...
│   ├── 16.9.txt
│   └── result.txt              #输出数据结果文件
└── script
    ├── main.py
    ├── startup.py
    └── 实验数据处理脚本使用说明.pdf
```

双击startup.py，输入数据所在文件的索引号，开始数据处理和画图。

在弹出的控制台输入回车，会关闭画板和程序。

## 三.输出说明

1. 输出文件所在文件夹名为输入文件夹名+"_out"，第二次输出为+"_out0"，依次递增；
2. 值得注意的一点，**假如存在1224_out，1224_out1两个文件夹，下次输出为1224_out0而不是1224_out2**；
3. 为了保证数据安全，程序不会删除任何文件，废弃的输出文件夹请手动删除。