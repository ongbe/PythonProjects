import uiautomator2 as u2
import time
import random


class TaoNews(object):
    def __init__(self, app_name, run_time):
        self.driver = u2.connect_wifi("192.168.31.18")
        # self.driver.settings["operation_delay"] = (0.5, 0.5)
        self.app_name = app_name
        self.run_time = run_time

    def start_app(self):
        # 启动 APP
        self.driver.app_start(self.app_name, stop=True)
        # 点击跳过等待页面
        if self.driver(resourceId="com.coohua.xinwenzhuan:id/tt_splash_skip_btn").wait():
            self.driver(resourceId="com.coohua.xinwenzhuan:id/tt_splash_skip_btn").click()
        time.sleep(2)

    def read_news(self):
        # 新闻阅读类不是很想写，主要是广告太多，有些不好判断
        # 判断第一条新闻是否存在
        if self.driver(resourceId="com.coohua.xinwenzhuan:id/tab_news_hot_item_img").wait():
            # 存在就点进去
            self.driver(resourceId="com.coohua.xinwenzhuan:id/tab_news_hot_item_img").click()
            start_time = time.time()
            count = 1
            while time.time() - start_time <= self.run_time:
                print(">>> 正在阅读第 %s 条新" % count)
                # 等待文章加载完
                if self.driver.xpath('//*[@resource-id="content"]/android.view.View[1]').wait():
                    # 开始阅读
                    for i in range(5):
                        self.driver.swipe(500, 1200, 500, 200, 0.5)
                        time.sleep(random.randint(3, 5))  # 暂停，阅读 3-5 秒
                    self.driver(scrollable=True).scroll.toEnd()  # 滑到页面底部
                    self.driver.xpath('')  # 点击下一条新闻
                count += 1

    def watch_videoes(self):
        # 切换到视频栏目
        self.driver(resourceId="com.coohua.xinwenzhuan:id/home_tab").child(clickable=True)[1].click()
        time.sleep(2)
        print(">>> 开始执行<视频>任务")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            # 如果视频的播放键存在（用这个来判断是视频还是广告）
            if self.driver(resourceId="com.coohua.xinwenzhuan:id/play").exists:
                # 点击播放视频
                self.driver(resourceId="com.coohua.xinwenzhuan:id/play").click()

                print("=" * 50)
                print(">>> 正在播放第 %s 个视频" % count)

                for j in range(30):
                    # 关闭弹窗（如果有）
                    if self.driver(resourceId="com.coohua.xinwenzhuan:id/gold_ad_iv_close").exists:
                        self.driver(resourceId="com.coohua.xinwenzhuan:id/gold_ad_iv_close").click()
                    if self.driver(resourceId="com.coohua.xinwenzhuan:id/ad_close").exists:
                        self.driver(resourceId="com.coohua.xinwenzhuan:id/ad_close").click()
                    time.sleep(1)
                print(">>> 第 %s 个视频播放完成" % count)

                rest_time = int(self.run_time - (time.time() - start_time))
                h = int(rest_time / 3600)
                m = int((rest_time - h * 3600) / 60)
                s = int(rest_time - h * 3600 - m * 60)
                print(">>> 剩余任务时间：{} 时 {} 分 {} 秒".format(h, m, s))
                print("=" * 50 + "\n")

                self.driver.press("back")  # 视频播放完后点击返回
                self.driver.swipe(500, 1000, 500, 0, 0.5)
                time.sleep(1)
            else:
                # 播放键不存在表明是广告，这样就继续往下滑，直到找到视频
                self.driver.swipe(500, 1000, 500, 0, 0.5)
                time.sleep(1)
            count += 1
        print(">>> <视频>任务完成，正在切换到<小视频>任务")

    def watch_small_videoes(self):
        # 切换到小视频栏
        self.driver.xpath('//*[@resource-id="com.coohua.xinwenzhuan:id/home_tab"]/android.widget.LinearLayout[1]/android.support.v7.app.ActionBar-Tab[3]').click()
        time.sleep(2)
        print(">>> 开始执行<小视频>任务")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            print("=" * 50)
            print(">>> 正在刷第 %s 个小视频" % count)

            rest_time = int(self.run_time - (time.time() - start_time))
            h = int(rest_time / 3600)
            m = int((rest_time - h * 3600) / 60)
            s = int(rest_time - h * 3600 - m * 60)
            print(">>> 剩余任务时间：{} 时 {} 分 {} 秒".format(h, m, s))
            print("=" * 50 + "\n")

            time.sleep(random.randint(6, 8))  # 随机播放 6-8 秒视频
            self.driver.swipe(500, 1000, 500, 0, 0.5)
            count += 1
        print(">>> <小视频>任务完成")

    def run(self):
        print(">>> 启动淘新闻 APP")
        self.start_app()
        # self.read_news()
        self.watch_videoes()
        self.watch_small_videoes()
        print(">>> 所有任务完成")
        print(">>> 退出应用")
        self.driver.app_stop(self.app_name)


if __name__ == "__main__":
    app_name = "com.coohua.xinwenzhuan"
    run_time = 1800
    taonews = TaoNews(app_name, run_time)
    taonews.run()
