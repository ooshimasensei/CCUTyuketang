Based on：[https://github.com/xrervip/AutoYuketangforHIT](https://github.com/xrervip/AutoYuketangforHIT)

# AutoYuketang
基于Selenium ChromeDriver模拟操作实现自动看雨课堂网课视频
## Installation
1. 安装Chrome及对应版本[ChromeDriver](https://chromedriver.chromium.org/home)并配置环境变量；
2. 安装[Selenium](https://www.selenium.dev/)：

		pip install selenium


## Usage
1. 配置`config.json`，`URL`为要刷课程的成绩单界面的url；`HOME_URL`为登录主页的url；

	```json
	[{
		"URL":"https://your.domain.cn/pro/lms/xxxxxxxxxxx/12345678/score",
		"HOME_URL":"https://your.domain.cn/pro/portal/home"
	}]
	```
2. (可选)配置`cookie.json`，将`domain`修改为对应的域名，扫码登陆后在视频界面查看对应cookie的值并填入`value`；

	```json
	[{
		"domain": "your.domain.cn",
		"name": "sessionid",
		"path": "/",
		"value": ""
	},
	{
		"domain": "your.domain.cn",
		"name": "csrftoken",
		"path": "/",
		"value": ""
	},
	{
		"domain": "your.domain.cn",
		"name": "platform_id",
		"path": "/",
		"value": ""
	},
	{
		"domain": "your.domain.cn",
		"name": "university_id",
		"path": "/",
		"value": ""
	},
	{
		"domain": "your.domain.cn",
		"name": "xtbz",
		"path": "/",
		"value": ""
	},
	{
		"domain": "your.domain.cn",
		"name": "platform_type",
		"path": "/",
		"value": ""
	}]
	```
3. 启动python脚本：
	```bash
	python yuketang.py
	```
	若配置了`cookie.json`则可以使用cookie登录：
	```bash
	python yuketang.py -CookieMode
	```
4. 脚本将自动先爬取所有视频链接，之后自动播放并开启二倍速；
5. 可以通过运行多个脚本实现同时刷不同网课。

<style>
pre {
  overflow-y: auto;
  max-height: 100px;
}
</style>


