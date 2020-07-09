import uiautomator2 as u2
import random
import time


class Jinritoutiao(object):
    def __init__(self, app_name, run_time):
        self.driver = u2.connect_wifi("192.168.31.18")
        self.app_name = app_name
        self.run_time = run_time

    def start_app(self):
        self.driver.app_start(self.app_name, stop=True)
        time.sleep(10)

    def read(self):
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            # 通过判断某一指定类型的文章来进行阅读
            if self.driver(resourceId="com.ss.android.article.lite:id/xo").exists:
                self.driver(resourceId="com.ss.android.article.lite:id/xo").click()
                time.sleep(1)
                # 判断是否为有金币奖励的文章
                if not self.driver(resourceId="com.ss.android.article.lite:id/fs").exists:
                    print("=" * 50)
                    print(">>> 正在阅读第 %s 篇文章" % count)
                    self.driver(scrollable=True).scroll.toEnd(100)  # 通过 toEnd() 滑动屏幕到底部
                    # 剩余任务时间
                    rest_time = int(self.run_time - (time.time() - start_time))
                    h = int(rest_time / 3600)
                    m = int((rest_time - h * 3600) / 60)
                    s = int(rest_time - h * 3600 - m * 60)
                    print(">>> 剩余任务时间：{} 时 {} 分 {} 秒".format(h, m, s))
                    print("=" * 50 + "\n")
                    count += 1

                    self.driver.press("back")
                    time.sleep(1)
                    for j in range(2):
                        self.driver.swipe(500, 1000, 500, 0)
                        time.sleep(0.2)
                    time.sleep(1)
                else:
                    # 如果阅读该篇文章没有金币奖励，就返回到主界面并往下滑动寻找新的文章
                    self.driver.press("back")
                    for j in range(2):
                        self.driver.swipe(500, 1000, 500, 0)
                        time.sleep(0.2)
                    time.sleep(1)
            else:
                # 如果指定的文章类型不存在，就往下滑动屏幕，直到找到新的文章
                for j in range(2):
                    self.driver.swipe(500, 1000, 500, 0)
                    time.sleep(0.2)
                time.sleep(1)

    def watch(self):
        pass

    def run(self):
        print(">>> 启动今日头条极速版 APP")
        self.start_app()
        print(">>> 开始<阅读文章>任务")
        print(">>> 任务时间：%s 小时" % float(self.run_time / 3600))
        self.read()
        print(">>> <阅读文章>任务完成")
        # print(">>> 开始<观看视频>任务")
        # print(">>> 任务时间：%s 小时" % float(self.run_time / 3600))
        # self.watch()
        # print(">>> <观看视频>任务完成")
        print(">>> 所有任务完成，退出应用")
        self.driver.app_stop(self.app_name)


if __name__ == "__main__":
    app_name = "com.ss.android.article.lite"
    run_time = 1800
    jinritoutiao = Jinritoutiao(app_name, run_time)
    jinritoutiao.run()