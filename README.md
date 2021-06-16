## 方式1：Github Actions
### Step1. Fork 本代码库

### Step2. 注册163邮箱

默认采用163邮箱，如有需要，自行更改[main.yml](.github/workflows/main.yml)文件

注册163邮箱后在设置界面开启POP3/SMTP服务，并记下授权码

[![2q1hrD.png](https://z3.ax1x.com/2021/06/15/2q1hrD.png)](https://imgtu.com/i/2q1hrD)

### Step3. 配置 Secret

在 Settings - Secrets 页面添加如下内容：



|       名称        | 内容                                                         |
| :---------------: | ------------------------------------------------------------ |
|    `USERNAME`     | 学号                                                         |
|    `PASSWORD`     | 密码                                                         |
|       `PAT`       | 可选，在运行前同步上游仓库，拉取最新的代码，建议配置此选项。[PAT获取教程，务必勾选repo和workflow](https://docs.github.com/cn/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) |
|  `MAIL_USERNAME`  | 可选，163邮箱账号，用于发送运行结果                          |
|  `MAIL_PASSWORD`  | 可选，163邮箱授权码                                          |
|      `SCKEY`      | 可选，旧版Server酱微信推送的SCKEY，详细见[官网](http://sc.ftqq.com/3.version) |
| `PUSH_PLUS_TOKEN` | 可选，微信扫码登录后一对一推送或一对多推送下面的token，详细见[官网](https://www.pushplus.plus/) |
|     `APP_ID`      | 可选，配置以使用百度OCR识别验证码登录                        |
|     `API_KEY`     | 同上                                                         |
|   `SECRET_KEY`    | 同上                                                         |



[![2q1cP1.png](https://z3.ax1x.com/2021/06/15/2q1cP1.png)](https://imgtu.com/i/2q1cP1)

添加后效果：

[![2q3VLF.png](https://z3.ax1x.com/2021/06/15/2q3VLF.png)](https://imgtu.com/i/2q3VLF)

### Step4. 开启workflow

[![2q8aBF.jpg](https://z3.ax1x.com/2021/06/15/2q8aBF.jpg)](https://imgtu.com/i/2q8aBF)

### Step5. 运行效果

默认每天早上8：30分开始打卡，并推送运行结果。

如需修改打卡时间，在[main.yml](.github/workflows/main.yml)文件修改Cron 表达式即可

> P.S：Github Actions 默认采用的是国际标准时间，与北京时间相差8小时，修改时注意转换

邮件默认发送到`MAIL_USERNAME`字段填写的邮箱，如有需要，可以在[main.yml](.github/workflows/main.yml)文件修改发送的目的邮箱地址或者在163邮箱设置里添加邮件自动转发到指定地址

[![2q8hAH.jpg](https://z3.ax1x.com/2021/06/15/2q8hAH.jpg)](https://imgtu.com/i/2q8hAH)

## 方式2：
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
## 方式3：云函数部署
>> 腾讯云函数有免费额度，不需要充值  

### 1、登录[腾讯云](https://cloud.tencent.com/)
如果没有用的过话先注册，实名认证  

![20210412123452](https://img.chaney.top/images/20210412123452.png)

### 2、创建[云函数](https://console.cloud.tencent.com/scf/list)
>> 只需修改截图部分，其他默认即可  

**2.1 新建**  
选择自定义创建，运行环境选择```python3.6```  
函数代码选择本地上传zip包，代码包[下载地址](https://github.com/Chaney1024/YQTB/releases/download/scf/yqtb.zip)  

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
