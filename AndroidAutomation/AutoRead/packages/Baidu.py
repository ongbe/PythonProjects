import uiautomator2 as u2
import time


class Baidu(object):
    def __init__(self, app_name, run_time):
        self.app_name = app_name
        self.run_time = run_time
        self.driver = u2.connect_wifi("192.168.31.18")

    def start_app(self):
        self.driver.app_start(self.app_name, stop=True)
        time.sleep(5)

    def read(self):
        # 暂时不做，主要是百度这个 B 太坑爹了，广告和正常文章的属性名全是一样的，不好定位
        pass

    def watch(self):
        # 切换到视频栏
        if self.driver.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[2]').exists:
            self.driver.xpath('//*[@resource-id="android:id/tabs"]/android.widget.FrameLayout[2]').click()
            time.sleep(1)
        # 更新一下视频内容
        self.driver.swipe(500, 500, 500, 1500)
        time.sleep(2)
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            if self.driver(resourceId="com.baidu.searchbox.lite:id/awh").exists:
                self.driver.swipe(500, 1000, 500, 300)
                time.sleep(0.2)
            else:
                self.driver(resourceId="com.baidu.searchbox.lite:id/b53").click()
                time.sleep(1)
                self.driver.swipe(500, 1000, 500, 300)
                time.sleep(0.2)

    def watch_small_video(self):
        if self.driver(resourceId="com.baidu.searchbox.lite:id/avl", text="小视频").wait():
            # 切换到小视频栏
            self.driver(resourceId="com.baidu.searchbox.lite:id/avl", text="小视频").click()
            time.sleep(1)
        # 点击第一个视频
        self.driver(className="android.widget.RelativeLayout").click()
        time.sleep(1)
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            print("=" * 50)
            print(">>> 正在观看第 %s 个视频" % count)
            # 观看 10 秒
            time.sleep(10)
            self.driver.swipe(500, 1500, 500, 0)

            rest_time = int(self.run_time - (time.time() - start_time))
            h = int(rest_time / 3600)
            m = int((rest_time - h * 3600) / 60)
            s = int(rest_time - h * 3600 - m * 60)
            print(">>> 任务剩余时间：{} 时 {} 分 {} 秒".format(h, m, s))
            print("=" * 50 + "\n")
            count += 1

    def run(self):
        print(">>> 启动百度极速版 APP")
        self.start_app()
        print(">>> 开始刷小视频")
        print(">>> 任务时间：%s 小时" % float(self.run_time / 3600))
        self.watch_small_video()
        print(">>> 小视频任务执行完毕")
        print(">>> 退出程序")
        self.driver.app_stop(self.app_name)


if __name__ == "__main__":
    app_name = "com.baidu.searchbox.lite"
    run_time = 1800
    baidu = Baidu(app_name, run_time)
    baidu.run()