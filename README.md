## 这里计划写一个多线程爬虫

#### 目前已有功能
- 1. 根据作文分类整理
- 2. 文本内容存储在分类文件夹中的txt文本中

#### 存在的问题
- 1. 已经搜索的网站会再次搜索 资源浪费
- 2. 只有文本存储没有存储数据库 不便查找
- 3. 频繁爬虫导致被网站封禁IP

### 依赖项
- 1. Python3.7
- 2. request_html
- 3. threading
- 4. queue


### 使用方法
```bash
# 安装依赖
pip3 install -r requirements.txt

# 运行程序
python3 poll.py
```

### 目录结构
```
.
├── poll.py　#线程管理
├── README.md # 说明文件
├── requirements.txt #依赖项
├── server.py #爬虫主函数
`-- txt # 作文存放的目录
```


