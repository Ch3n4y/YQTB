## 方式1
1、下载代码  
```shell
git clone https://github.com/Chaney1024/YQTB.git
```
2、安装依赖
```shell
cd YQTB && pip3 install -r requirements.txt
```
3、修改```index.py```文件中的学号密码  
  

4、测试执行  
```shell
python3 index.py
```
5、使用linux自带定时任务```crontab```  
```shell
crontab -e
```
最后一行添加(注意修改绝对路径```path```)  
```shell
30 8,10 * * * python3 /path/index.py
```
```30 8,10 * * *``` 表示每天8:30,10:30各执行一次
## 方式2：云函数部署
>> 腾讯云函数有免费额度，不需要充值  

### 1、登录[腾讯云](https://cloud.tencent.com/)
如果没有用的过话先注册，实名认证  

![20210412123452](https://img.chaney.top/images/20210412123452.png)

### 2、创建[云函数](https://console.cloud.tencent.com/scf/list)
>> 只需修改截图部分，其他默认即可  

**2.1 新建**  
选择自定义创建，运行环境选择```python3.6```  
函数代码选择本地上传zip包，代码包[下载地址](https://4n3y-1259527519.cos.ap-guangzhou.myqcloud.com/yqtb.zip)  

![20210412122136](https://img.chaney.top/images/20210412122136.png)

**2.2 展开高级配置**  
修改默认超时时间，一般设置90s  
按图示配置环境变量  ```USERNAME```、```PASSWORD```  
 ![20210412122715](https://img.chaney.top/images/20210412122715.png)  

 **2.3 展开触发器配置**  
触发版本选择```$LATEST```  
自定义定时触发周期 ```0 30 8 * * * *``` 表示每天8:30打卡  
详细配置可查看[Cron 表达式](https://cloud.tencent.com/document/product/583/9708#cron-.E8.A1.A8.E8.BE.BE.E5.BC.8F)  
![20210412124622](https://img.chaney.top/images/20210412124622.png)  
**完成**