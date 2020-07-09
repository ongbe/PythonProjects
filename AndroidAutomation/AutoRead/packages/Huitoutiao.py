import uiautomator2 as u2
import time


class Huitoutiao(object):
    def __init__(self, app_name, run_time):
        self.driver = u2.connect_wifi("192.168.31.18")
        self.app_name = app_name
        self.run_time = run_time

    def start_app(self):
        self.driver.app_start(self.app_name, stop=True)
        # 点击跳过
        if self.driver.xpath('//*[@resource-id="com.cashtoutiao:id/splash_count_down_tv"]').wait():
            self.driver.xpath('//*[@resource-id="com.cashtoutiao:id/splash_count_down_tv"]').click()
        time.sleep(1)
        # 切换到视频栏
        self.driver.xpath('//*[@resource-id="com.cashtoutiao:id/tabs"]/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]').click()
        time.sleep(1)

    def watch(self):
        # 判断视频是否为广告
        if self.driver(resourceId="com.cashtoutiao:id/src").get_text()[-2:] == "广告":
            self.driver.swipe(500, 1000, 500, 310, 0.5)  # 是广告的话就继续往下滑
        else:
            # 在点击播放视频之前获取视频时长
            total_time = self.driver(resourceId="com.cashtoutiao:id/tv_list_video_duration").get_text()
            print(">>> 视频时长：", total_time)
            # 点击播放视频
            self.driver(resourceId="com.cashtoutiao:id/alivc_player_state").click()
            # 判断视频开头有无广告，有就点击跳过
            if self.driver.xpath('//*[@resource-id="com.cashtoutiao:id/tv_skip_ad"]').wait(timeout=3):
                self.driver.xpath('//*[@resource-id="com.cashtoutiao:id/tv_skip_ad"]').click()
            # 等待视频播放完成
            time.sleep(int(total_time.split(":")[0]) * 60 + int(total_time.split(":")[1]))
            self.driver.press("back")  # 播放完后退回到上一界面
            self.driver.swipe(500, 1000, 500, 0, 0.5)

    def run(self):
        print(">>> 启动惠头条 APP")
        self.start_app()
        print(">>> 开始执行<视频>任务")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time < self.run_time:
            print("=" * 50)
            print(">>> 正在观看第 %s 个视频" % count)
            self.watch()
            print(">>> 视频观看完成")

            rest_time = int(self.run_time - (time.time() - start_time))
            h = int(rest_time / 3600)
            m = int((rest_time - h * 3600) / 60)
            s = int(rest_time - h * 3600 - m * 60)
            print(">>> 任务剩余时间：{} 时 {} 分 {} 秒".format(h, m, s))
            print("=" * 50 + "\n")
            count += 1
        print(">>> <视频>任务执行完毕，共观看 %s 个视频" % count)
        print(">>> 退出程序")
        self.driver.app_stop(self.app_name)


if __name__ == "__main__":
    app_name = "com.cashtoutiao"
    run_time = 1800
    huitoutiao = Huitoutiao(app_name, run_time)
    huitoutiao.run()