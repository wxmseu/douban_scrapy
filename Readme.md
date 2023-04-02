1. 创建douban_scrapy文件夹，切换到文件夹目录中
2. 创建虚拟环境

`python -m venv venv`

3. 进入到虚拟环境中

`.\venv\Scripts\activate`

4. 安装scrapy框架

`pip install scrapy`

5. 创建一个项目

`scrapy startproject douban`

6. 创建一个spider

`cd douban`

`scrapy genspider douban_movie movie.douban.com`

可以看到生成了这样的文件目录，之后的主要操作是在items.py，middlewares.py，pipelines.py，settings.py和spiders目录下的douban_movie.py进行编写程序

```
D:.
│  scrapy.cfg
│
└─douban
    │  items.py
    │  middlewares.py
    │  pipelines.py
    │  settings.py
    │  __init__.py
    │
    ├─spiders
    │  │  douban_movie.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          __init__.cpython-310.pyc
    │
    └─__pycache__
            settings.cpython-310.pyc
            __init__.cpython-310.pyc
```

7. 添加业务逻辑 
8. 启动爬虫

`scrapy crawl douban_movie`