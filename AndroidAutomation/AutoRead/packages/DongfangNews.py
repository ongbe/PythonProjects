import uiautomator2 as u2
import time


class DongfangNews(object):
    def __init__(self, app_name, run_time):
        self.driver = u2.connect("192.168.31.18")
        self.app_name = app_name
        self.run_time = run_time

    def start_app(self):
        self.driver.app_start(self.app_name, stop=True)
        # 点击进入页面的跳过按钮
        # if self.driver.xpath('//*[@resource-id="com.songheng.eastnews:id/ahh"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]').wait(timeout=1):
        #     self.driver.xpath('//*[@resource-id="com.songheng.eastnews:id/ahh"]/android.widget.FrameLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]').click()
        # if self.driver.xpath('//*[@resource-id="com.miui.systemAdSolution:id/view_skip"]').wait(timeout=1):
        #     self.driver.xpath('//*[@resource-id="com.miui.systemAdSolution:id/view_skip"]').click()
        time.sleep(10)

    def read(self):
        print(">>> 开始阅读文章")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            if self.driver(resourceId="com.songheng.eastnews:id/a4z").exists:
                print("=" * 50)
                print(">>> 正在阅读第 %s 篇文章" % count)

                self.driver(resourceId="com.songheng.eastnews:id/a4z").click()
                time.sleep(2)
                # 向下滑动 3 次，模拟阅读文章
                for i in range(5):
                    self.driver.swipe(500, 1000, 500, 200)
                    time.sleep(5)

                self.driver.press("back")  # 回到主界面
                time.sleep(0.2)
                # 向下滑动 2 次，找到新的文章
                for i in range(2):
                    self.driver.swipe(500, 1000, 500, 0)
                    time.sleep(0.2)
                time.sleep(0.2)

                rest_time = int(self.run_time - (time.time() - start_time))
                h = int(rest_time / 3600)
                m = int((rest_time - h * 3600) / 60)
                s = int(rest_time - h * 3600 - m * 60)
                print(">>> 任务剩余时间：{} 时 {} 分 {} 秒".format(h, m, s))
                print("=" * 50 + "\n")
                count += 1
            else:
                for i in range(2):
                    self.driver.swipe(500, 1000, 500, 0)
                    time.sleep(0.2)

    def watch(self):
        # 切换到视频栏
        self.driver(resourceId="com.songheng.eastnews:id/a_s").click()
        time.sleep(0.5)
        print(">>> 开始刷视频")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            # 判断播放键是否存在（根据这个判断是不是广告）
            if self.driver(resourceId="com.songheng.eastnews:id/wm").exists:
                self.driver(resourceId="com.songheng.eastnews:id/wm").click()
                print("=" * 50)
                print(">>> 正在播放第 %d 个视频" % count)
                # 暂停 2 秒后再点击以获得视频时长
                time.sleep(2)
                self.driver.click(300, 400)
                # 获取视频时长
                time_widget = self.driver(resourceId="com.songheng.eastnews:id/d6").get_text()
                # 将视频时长转换成秒数
                total_time = int(time_widget.split(":")[0]) * 60 + int(time_widget.split(":")[1])
                # 判断视频时长是否超过 30 秒（因为 右下角的圈转够大约 30 秒后就会转的很慢，等转完的话会比较费时间）
                if total_time <= 30:
                    time.sleep(total_time - 2)
                else:
                    time.sleep(30 - 2)
                print(">>> 视频播放完毕")
                # 获取剩余任务时间
                rest_time = int(self.run_time - (time.time() - start_time))
                h = int(rest_time / 3600)
                m = int((rest_time - h * 3600) / 60)
                s = int(rest_time - h * 3600 - m * 60)
                print(">>> 任务剩余时间：{} 时 {} 分 {} 秒".format(h, m, s))
                print("=" * 50 + "\n")
                # 回到上一界面
                self.driver.press("back")
                time.sleep(0.2)
                # 往下滑动
                self.driver.swipe(500, 1000, 500, 0)
                time.sleep(0.2)
                count += 1
            else:
                # 如果页面的第一个视频是广告的话就向下滚动
                self.driver.swipe(500, 1000, 500, 0)
                time.sleep(0.2)

    def run(self):
        print(">>> 启动东方头条 APP")
        self.start_app()
        # self.read()
        # print(">>> 文章阅读完成")
        self.watch()
        print(">>> 视频观看完毕")
        print(">>> 退出应用")
        self.driver.app_stop(self.app_name)


if __name__ == "__main__":
    app_name = "com.songheng.eastnews"
    run_time = 1800
    dongfangnews = DongfangNews(app_name, run_time)
    dongfangnews.run()