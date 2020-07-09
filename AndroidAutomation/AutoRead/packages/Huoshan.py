import uiautomator2 as u2
import time
import random


class Huoshan(object):
    def __init__(self, app_name, run_time):
        self.app_name = app_name
        self.driver = u2.connect_wifi("192.168.31.18")
        self.run_time = run_time

    def start_app(self):
        self.driver.app_start(self.app_name, stop=True)
        time.sleep(5)  # 暂停 5 秒，等待进入主界面
        if self.driver.xpath("//*[@resource-id=\"com.ss.android.ugc.livelite:id/r4\"]").exists:
            self.driver.xpath("//*[@resource-id=\"com.ss.android.ugc.livelite:id/r4\"]").click()

    def watch(self):
        time.sleep(random.randint(5, 8))  # 随机观看 5-8 秒视频
        # 滑动视频
        self.driver.swipe(500, 1700, 500, 20, 0.5)
        # 随机点赞和关注
        self.random_like_and_attention()

    def random_like_and_attention(self):
        # 随机的几率调小一点
        if random.random() - 0.9 > 0:
            # 如果点赞按钮存在就随机点赞
            if self.driver.xpath('//*[@resource-id="com.kuaishou.nebula:id/like_button"]/android.widget.RelativeLayout[1]').exists:
                self.driver.xpath('//*[@resource-id="com.kuaishou.nebula:id/like_button"]/android.widget.RelativeLayout[1]').click()
        time.sleep(0.5)
        if random.random() - 0.9 > 0:
            # 如果关注按钮存在就随机关注
            if self.driver(resourceId="com.kuaishou.nebula:id/slide_play_right_follow_button").exists:
                self.driver(resourceId="com.kuaishou.nebula:id/slide_play_right_follow_button").click()

    def run(self):
        print(">>> 启动火山极速版 APP")
        self.start_app()
        print(">>> 开始执行<小视频>任务")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time <= self.run_time:
            print("=" * 50)
            print(">>> 正在刷第 %s 个视频" % count)
            self.watch()
            rest_time = int(self.run_time - (time.time() - start_time))
            h = int(rest_time / 3600)
            m = int((rest_time - h * 3600) / 60)
            s = int(rest_time - h * 3600 - m * 60)
            print(">>> 剩余任务时间：{} 时 {} 分 {} 秒".format(h, m, s))
            print("=" * 50 + "\n")
            count += 1
        print(">>> <小视频>任务执行完毕，共刷 %s 个视频" % count)
        print(">>> 退出应用")
        self.driver.app_stop(self.app_name)


if __name__ == "__main__":
    app_name = "com.ss.android.ugc.livelite"
    run_time = 1800  # 指定 1 个小时的运行时间
    huoshan = Huoshan(app_name, run_time)
    huoshan.run()