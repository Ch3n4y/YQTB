## 方式1：本地执行
```shell
pip3 install -r requirements.txt
python3 index.py
```

## 方式2：服务器定时任务
安装依赖
```shell
pip3 install -r requirements.txt
```
使用linux自带定时任务```crontab```  
```shell
crontab -e
```
最后一行添加(注意修改绝对路径```path```)  
```shell
30 8,10 * * * python3 /path/index.py
```
```30 8,10 * * *``` 表示每天8:30,10:30各执行一次

## 方式3：云函数部署
***未完待续***
