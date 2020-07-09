import uiautomator2 as u2
import time
import random


class Qujianpan(object):
    def __init__(self, app_name, run_time):
        self.driver = u2.connect_wifi("192.168.31.18")
        self.app_name = app_name
        self.run_time = run_time

    def start_app(self):
        self.driver.app_start(self.app_name, stop=True)
        # 如果由弹窗就点击关闭
        if self.driver.xpath('//*[@resource-id="com.qujianpan.client.fast:id/tv_go_setting"]').wait():
            self.driver.xpath('//*[@resource-id="com.qujianpan.client.fast:id/tv_go_setting"]').click()
            time.sleep(1)
            self.driver.press("back")
            time.sleep(1)
        # 切换到短视频栏目
        self.driver.xpath('//*[@resource-id="com.qujianpan.client.fast:id/tl_home"]/android.widget.LinearLayout[1]/android.support.v7.app.ActionBar-Tab[4]').click()
        time.sleep(1)

    def watch(self):
        self.driver.swipe(500, 1000, 500, 0, 0.5)
        time.sleep(random.randint(6, 8))

    def run(self):
        print(">>> 启动趣键盘极速版 APP")
        self.start_app()
        print(">>> 开始执行<小视频>任务")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            print("=" * 50)
            print(">>> 正在刷第 %s 个视频" % count)
            self.watch()
            rest_time = int(self.run_time - (time.time() - start_time))
            h = int(rest_time / 3600)
            m = int((rest_time - h * 3600) / 60)
            s = int(rest_time - h * 3600 - m * 60)
            print("剩余任务时间：{} 时 {} 分 {} 秒".format(h, m, s))
            print("=" * 50 + "\n")
            count += 1
        print(">>> <小视频>任务执行完毕，共刷 %s 个视频" % count)
        print(">>> 退出程序")
        self.driver.app_stop(self.app_name)


if __name__ == "__main__":
    app_name = "com.qujianpan.client.fast"
    run_time = 1800
    qujianpan = Qujianpan(app_name, run_time)
    qujianpan.run()