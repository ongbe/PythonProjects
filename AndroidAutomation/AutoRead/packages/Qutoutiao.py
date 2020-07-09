import uiautomator2 as u2
import time


class Qutoutiao(object):
    def __init__(self, app_name, run_time):
        self.driver = u2.connect_wifi("192.168.31.18")
        # self.driver.settings["operation_delay"] = (0.5, 0.5)  # 设置操作延时
        self.app_name = app_name
        self.run_time = run_time

    def start_app(self):
        self.driver.app_start(self.app_name, stop=True)
        # 点击跳过
        if self.driver(resourceId="com.jifen.qukan:id/oy").wait():
            self.driver(resourceId="com.jifen.qukan:id/oy").click()
        # 关闭弹窗（如果有）
        if self.driver(resourceId="com.jifen.qukan:id/a8n").wait():
            self.driver(resourceId="com.jifen.qukan:id/a8n").click()
        time.sleep(2)
        self.driver.swipe(500, 500, 500, 1700)  # 先刷新一下主页的内容
        time.sleep(2)

    def read(self):
        print(">>> 开始执行<阅读>任务")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            print("=" * 50)
            print(">>> 正在刷第 %s 个视频" % count)
            # 判断视频的播放键是否存在，存在就点击进去观看
            if self.driver(resourceId="com.jifen.qukan:id/aqv").exists:
                # 判断播放键下面的视频时长是否存在
                if self.driver(resourceId="com.jifen.qukan:id/aqv").child(resourceId="com.jifen.qukan:id/am1").exists:
                    item = self.driver(resourceId="com.jifen.qukan:id/aqv").child(resourceId="com.jifen.qukan:id/am1").get_text()  # 获取视频的播放时间
                    total_time = int(item.split(":")[0]) * 60 + int(item.split(":")[1])
                    print(">>> 视频时长：", total_time)
                    # 点击播放
                    self.driver(resourceId="com.jifen.qukan:id/aqv").child(resourceId="com.jifen.qukan:id/am0").click()
                    time.sleep(total_time)  # 等待视频播放完
                    self.driver.press("back")
                    self.driver.swipe(500, 1700, 500, 0)
                    rest_time = int(self.run_time - (time.time() - start_time))
                    h = int(rest_time / 3600)
                    m = int((rest_time - h * 3600) / 60)
                    s = int(rest_time - h * 3600 - m * 60)
                    print(">>> 剩余任务时间：{} 时 {} 分 {} 秒".format(h, m, s))
                    print("=" * 50 + "\n")
                    count += 1
            else:
                # 不存在就往下滑
                self.driver.swipe(500, 1700, 500, 0)
                time.sleep(2)
        print(">>> <阅读>任务执行完毕，共刷 %s 个视频" % count)

    def watch(self):
        print(">>> 开始执行<视频>任务")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            print("=" * 50)
            print(">>> 正在刷第 %s 个视频" % count)
            if self.driver(resourceId="com.jifen.qukan:id/bq5").exists:
                self.driver(resourceId="com.jifen.qukan:id/bq5").click()
                time.sleep(1)
                self.driver.click(497, 419)   # 点击一下视频
                total_time = self.driver(resourceId="com.jifen.qukan:id/bzs").get_text().split("/")[1]
                time.sleep(int(total_time.split(":")[0]) * 60 + int(total_time.split(":")[1]))
                rest_time = int(self.run_time - (time.time() - start_time))
                h = int(rest_time / 3600)
                m = int((rest_time - h * 3600) / 60)
                s = int(rest_time - h * 3600 - m * 60)
                print(">>> 剩余任务时间：{} 时 {} 分 {} 秒".format(h, m, s))
                print("=" * 50 + "\n")
                count += 1
            else:
                self.driver.swipe(500, 1000, 500, 0, 0.5)
                time.sleep(0.2)
        print(">>> <视频>任务执行完毕，共刷 %s 个视频" % count)

    def run(self):
        print(">>> 启动趣头条 APP")
        self.start_app()
        # self.read()
        # print(">>> 切换到<视频>任务")
        self.watch()
        print(">>> 所有任务执行完毕")
        print(">>> 退出程序")
        self.driver.app_stop(self.app_name)


if __name__ == "__main__":
    app_name = "com.jifen.qukan"
    run_time = 1800
    qutoutiao = Qutoutiao(app_name, run_time)
    qutoutiao.run()