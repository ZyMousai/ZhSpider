# ZhSpider
### 本项目为知乎Spider
### 说明
  1. core为核心代码
  2. result为输出结果
  3. template为输入存放地
  4. main为入口
  5. 环解为：python3.5以上

### 使用说明

1. 安装node.js 并设置环境变量 按照下面这个连接的教材来就可以了

    https://www.jb51.net/article/202203.htm

   安装好node.js  切换到util\x-zse-96目录下执行以下命令 出现

   ```vue
   npm install jsdom
   ```

2. 安装python的模块

   在项目文件夹寻找requirements.txt文件，然后执行以下命令:

   ```python
   pip install -r requriements.txt
   ```

3. 设置cookie文件

   把登录好的cookie放在.\template\cookie.txt中 没有此文件 自己创建即可

4. 启动项目

   在主目录下执行以下命令即可启动项目

   ```python
   python main.py
   ```

5. 在设置好cookie 抓取不到数据的时候 把util/headers.py中d_c0其中值替换一下

   这个值可以在cookie中找到

   1 先找到cookie的中d_c0的值
   
   ![](https://raw.githubusercontent.com/zyp0529/img/main/image-20211204173017252.png)
   
   2 找到util/headers.py文件
   
   ![](https://raw.githubusercontent.com/zyp0529/img/main/DC55828F-215C-4f02-BB3F-37FDAC9BDD55.png)

​	 3把cookie中找到的d_c0的值替换到 gen_header函数中d_c0的值中

​		![](https://raw.githubusercontent.com/zyp0529/img/main/7F6029E1-BAC1-45ea-8B95-09570A63637C.png)

​    4 最后在启动脚本跑就可以了 
