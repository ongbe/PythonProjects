import uiautomator2 as u2
import time


class Zhongqingkandian(object):
    def __init__(self, app_name, run_time):
        self.driver = u2.connect_wifi("192.168.31.18")
        self.app_name = app_name
        self.run_time = run_time

    def start_app(self):
        self.driver.app_start(self.app_name, stop=True)
        time.sleep(10)
        # 切换到“热点”栏
        self.driver.xpath('//*[@text="热点"]').click()
        time.sleep(2)

    def read(self):
        print(">>> 开始阅读文章")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            time.sleep(0.5)
            UIWidget = self.driver(resourceId="cn.youth.news:id/xx").child(className="android.widget.LinearLayout", instance=1)
            if not UIWidget.child(resourceId="cn.youth.news:id/a9g").exists:
                UIWidget.click()
                print("=" * 50)
                print(">>> 正在阅读第 %s 篇文章" % count)
                # 阅读文章
                for j in range(5):
                    self.driver.swipe(500, 1000, 500, 0)
                    time.sleep(5)
                print(">>> 阅读完成")
                # 获取剩余任务时间
                rest_time = int(self.run_time - (time.time() - start_time)) / 2
                h = int(rest_time / 3600)
                m = int((rest_time - h * 3600) / 60)
                s = int(rest_time - h * 3600 - m * 60)
                print(">>> 任务剩余时间：{} 时 {} 分 {} 秒".format(h, m, s))
                print("=" * 50 + "\n")
                # 返回上一界面
                self.driver.press("back")
                time.sleep(0.2)
                # 向下滑动
                self.driver.swipe(500, 1500, 500, 0, 0.5)
                time.sleep(0.2)
                count += 1
            else:
                self.driver.swipe(500, 1500, 500, 0)
                time.sleep(0.2)

    def watch(self):
        # 切换到视频栏
        self.driver(resourceId="cn.youth.news:id/a01").click()
        time.sleep(1)
        print(">>> 开始刷视频")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            print("=" * 50)
            if not self.driver(resourceId="cn.youth.news:id/a_y").exists:
                print(">>> 正在刷第 %s 个视频" % count)
                # 获取视频总时长，样式： xx:xx
                total_time = self.driver(resourceId="cn.youth.news:id/aea").get_text()
                print(">>> 视频时长：", total_time)
                total_time = int(total_time.split(":")[0]) * 60 + int(total_time.split(":")[1])
                # 点击播放视频
                self.driver(resourceId="cn.youth.news:id/ml").click()
                # 等待视频播放完
                # 同一个页面最多只有 300 秒时间可以获得金币，因此判断一下视频时长是否在 300 秒以内
                if total_time <= 300:
                    time.sleep(total_time)
                else:
                    time.sleep(300)
                print(">>> 视频播放完毕")
                # 获取剩余任务时间
                rest_time = int(self.run_time - (time.time() - start_time)) / 2
                h = int(rest_time / 3600)
                m = int((rest_time - h * 3600) / 60)
                s = int(rest_time - h * 3600 - m * 60)
                print(">>> 任务剩余时间：{} 时 {} 分 {} 秒".format(h, m, s))
                print("=" * 50 + "\n")
                # 点击返回到上一界面
                self.driver.press("back")
                # 向下滑动，寻找新的视频
                self.driver.swipe(500, 1000, 500, 0)
                time.sleep(0.2)
                count += 1
            else:
                # 判断是不是广告
                if self.driver(resourceId="cn.youth.news:id/a_y").get_text()[:2] == "广告":
                    print(">>> 跳过广告")
                    print("=" * 50 + "\n")
                    self.driver.swipe(500, 1000, 500, 0, 0.5)
                    time.sleep(0.2)

    def run(self):
        print(">>> 启动中青看点 APP")
        self.start_app()
        # self.read()
        # print(">>> 文章阅读完毕")
        self.watch()
        print(">>> 视频播放完毕")
        print(">>> 退出应用")
        self.driver.app_stop(self.app_name)


if __name__ == "__main__":
    app_name = "cn.youth.news"
    run_time = 1800
    zhongqingkandian = Zhongqingkandian(app_name, run_time)
    zhongqingkandian.run()