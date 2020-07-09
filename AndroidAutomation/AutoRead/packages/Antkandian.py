import uiautomator2 as u2
import time


class Antkandian(object):
    def __init__(self, app_name, run_time):
        self.app_name = app_name
        self.run_time = run_time
        self.driver = u2.connect_wifi("192.168.31.18")

    def start_app(self):
        self.driver.app_start(self.app_name, stop=True)
        if self.driver(resourceId="com.ldzs.zhangxin:id/iv_close").wait(timeout=20):
            self.driver(resourceId="com.ldzs.zhangxin:id/iv_close").click()

    def read(self):
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            # 判断指定的文章是否存在，以免点进广告
            # 文章和广告的 resourceId是不同的，按理说根据 resourceId 就可以判断是否为广告，但是指定了 resourceId 居然也会点进广告，
            # 这让我有点想不明白，所以又加了一个 className 的限定条件
            if self.driver(resourceId="com.ldzs.zhangxin:id/lr_more_article", className="android.widget.RelativeLayout").exists:
                print("=" * 50)
                print(">>> 正在阅读第 %s 篇文章" % count)
                # 存在就点击进去阅读
                self.driver(resourceId="com.ldzs.zhangxin:id/lr_more_article", className="android.widget.RelativeLayout").click()
                time.sleep(1)
                # 模拟阅读文章，往下滑动 5 次屏幕
                for j in range(10):
                    self.driver.swipe(500, 1000, 500, 0)
                    # 看到一定次数后，会出现金蛋，不把金蛋消掉就不会产生收益
                    if not self.driver(resourceId="com.ldzs.zhangxin:id/coin_front_text_image").exists:
                        if self.driver(resourceId="com.ldzs.zhangxin:id/news_income_container").exists:
                            self.driver(resourceId="com.ldzs.zhangxin:id/news_income_container").click()
                            time.sleep(3)
                            self.driver.xpath('//*[@resource-id="com.ldzs.zhangxin:id/ad_placeholder"]/android.widget.FrameLayout[1]').click()
                    else:
                        time.sleep(5)
                    # if count % 10 == 0:
                    #     self.driver(resourceId="com.ldzs.zhangxin:id/news_income_container").click()
                    #     time.sleep(3)
                    #     self.driver.xpath('//*[@resource-id="com.ldzs.zhangxin:id/ad_placeholder"]/android.widget.FrameLayout[1]').click()
                    # else:
                    #     time.sleep(3)
                    # time.sleep(5)

                rest_time = int(self.run_time - (time.time() - start_time))
                h = int(rest_time / 3600)
                m = int((rest_time - h * 3600) / 60)
                s = int(rest_time - h * 3600 - m * 60)
                print(">>> 阅读完毕")
                print(">>> 任务剩余时间：{} 时 {} 分 {} 秒".format(h, m, s))
                print("=" * 50 + "\n")
                count += 1

                # 返回主界面
                self.driver.press("back")
                time.sleep(0.5)
                # 向下滑动屏幕，寻找新的文章
                for j in range(2):
                    self.driver.swipe(500, 1000, 500, 0)
                    time.sleep(0.2)
                time.sleep(0.5)
            else:
                # 如果指定的文章不存在，就向下滑动屏幕，寻找新的文章
                for j in range(2):
                    self.driver.swipe(500, 1000, 500, 0)
                    time.sleep(0.2)
                time.sleep(0.5)

    def watch(self):
        # 切换到视频栏
        self.driver(resourceId="com.ldzs.zhangxin:id/tv_find_tab").click()
        time.sleep(1)
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            # 判断是视频还是广告
            if self.driver(resourceId="com.ldzs.zhangxin:id/iv_article_video").exists:
                print("=" * 50)
                print(">>> 正在观看第 %s 个视频" % count)
                time_widget = self.driver(resourceId="com.ldzs.zhangxin:id/tv_video_time").get_text()
                total_time = int(time_widget.split(":")[0] * 60 + int(time_widget.split(":")[1]))
                self.driver(resourceId="com.ldzs.zhangxin:id/iv_article_video").click()
                for k in range(int(total_time / 5)):
                    # 看到一定次数后，会出现金蛋，不把金蛋消掉就不会产生收益
                    if self.driver(resourceId="com.ldzs.zhangxin:id/news_income_container").exists:
                        self.driver(resourceId="com.ldzs.zhangxin:id/news_income_container").click()
                        time.sleep(3)
                        self.driver.xpath('//*[@resource-id="com.ldzs.zhangxin:id/ad_placeholder"]/android.widget.FrameLayout[1]').click()
                    else:
                        time.sleep(5)

                rest_time = int(self.run_time - (time.time() - start_time))
                h = int(rest_time / 3600)
                m = int((rest_time - h * 3600) / 60)
                s = int(rest_time - h * 3600 - m * 60)
                print(">>> 视频观看完毕")
                print(">>> 任务剩余时间：{} 时 {} 分 {} 秒".format(h, m, s))
                print("=" * 50 + "\n")
                count += 1

                # time.sleep(total_time)
                self.driver.press("back")
                time.sleep(0.5)
                for j in range(2):
                    self.driver.swipe(500, 1000, 500, 0)
                    time.sleep(0.2)
                time.sleep(0.5)
            else:
                for j in range(2):
                    self.driver.swipe(500, 1000, 500, 0)
                    time.sleep(0.2)
                time.sleep(0.5)

    def run(self):
        print(">>> 启动蚂蚁看点 APP")
        self.start_app()
        print(">>> 开始<阅读文章>")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        self.read()
        print(">>> <阅读文章>完成")
        print(">>> 开始<观看视频>")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        print(">>> <观看视频>完成")
        print(">>> 所有任务执行完毕")
        print(">>> 退出应用")
        self.driver.app_stop(self.app_name)


if __name__ == "__main__":
    app_name = "com.ldzs.zhangxin"
    run_time = 1800
    antkandian = Antkandian(app_name, run_time)
    antkandian.run()