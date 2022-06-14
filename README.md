# TrafficFlask
### 摘要：

1. 利用YOLOv4进行交通道路车流量统计；
2. 利用Python-Flask进行web端编写；
3. 利用MySQL存储道路车流量数据

### 总体设计：

1. 总体设计概念图

   <img src="D:\PycharmProjects_\TrafficFlask\README.assets\overall_design_flow_chart.png" alt="overall_design_flow_chart" style="zoom:80%;" />

2. 实现功能

   1. 用户登录：进入系统前，通过用户登录系统进行身份验证，只有通过身份验证才可以进入系统进行各种操作。对用户账号与密码实行保密存储，防止入侵后被盗取。
   2. 摄像头读取显示：在用户点击地图图标和链接后跳转到摄像头所对应的实时视频。满足摄像头视频的实时读取与查看。
   3. 视频帧预测分析：利用多线程的手段，对所有摄像头产生的视频进行实时检测与分析，产生预测框与预测数据，并对分析视频帧进行保存。满足对大量摄像头的并发式预测与查询。
   4. 前端交互：提供用户与系统的交互界面。需要界面美观，交互性好。
   5. 数据库连接操作：提供系统与数据库的操作接口，可以对数据库进行增删改查操作。满足实时性与并发性要求。

3. 运行设计：

   <img src="D:\PycharmProjects_\TrafficFlask\README.assets\run_design.png" alt="run_design" style="zoom:80%;" />

### 总体设计

1. 介绍页面

   <img src="D:\PycharmProjects_\TrafficFlask\README.assets\pre_page_.png" alt="pre_page_" style="zoom:67%;" />

   项目说明展示

2. 登录页面

   <img src="D:\PycharmProjects_\TrafficFlask\README.assets\login_page.png" alt="login_page" style="zoom:67%;" />

   web登录验证

3. 摄像头显示页面

   <img src="D:\PycharmProjects_\TrafficFlask\README.assets\main_page.png" alt="main_page" style="zoom:67%;" />

   1. 内嵌百度地图API，配合javasprit可以实现点图点击事件打开摄像头视频；
   2. 右侧按钮点击事件打开摄像头视频。

4. 摄像头视频播放页面

   <img src="D:\PycharmProjects_\TrafficFlask\README.assets\camers_show_page.png" alt="camers_show_page" style="zoom:67%;" />

   1. 播放当前摄像头对应的监控视频；
   2. 点击查看检测详情，调用数据库进行数据显示。

5. 数据显示页面

   <img src="D:\PycharmProjects_\TrafficFlask\README.assets\data_show_page.png" alt="data_show_page" style="zoom:67%;" />

   展示当前监控路口的车流量情况。

6. 多线程并发多视频检测

   <img src="D:\PycharmProjects_\TrafficFlask\README.assets\test.png" alt="test" style="zoom:67%;" />

   在Flask中开启多线程，进行多个视频的同时检测。

   