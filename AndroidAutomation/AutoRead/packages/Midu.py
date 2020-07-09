import uiautomator2 as u2
import time


class Midu(object):
    def __init__(self, app_name, run_time):
        self.driver = u2.connect_wifi("192.168.31.18")
        self.app_name = app_name
        self.run_time = run_time
        self.driver.settings["wait_timeout"] = 10  # 设置元素等待时间
        # self.driver.settings["operation_delay"] = (0.2, 0.2)  # 配置点击前延时 0.2s，点击后延时 0.2s

    def start_app(self):
        self.driver.app_start(self.app_name, stop=True)
        # 点击跳过
        self.driver.xpath('//*[@resource-id="com.lechuan.mdwz:id/jl"]/android.widget.LinearLayout[1]/android.widget.TextView').wait().click()
        time.sleep(1)
        # 关闭弹窗（如果有）
        if self.driver(resourceId="com.lechuan.mdwz:id/gg").wait(timeout=1):
            self.driver(resourceId="com.lechuan.mdwz:id/gg").click()
        time.sleep(1)
        # 点击全部在读
        self.driver.xpath('//*[@text="全部在读"]').wait().click()
        time.sleep(1)
        # 点击开始阅读
        self.driver.xpath('//*[@text="立即阅读"]').wait().click()
        time.sleep(1)

    def read(self):
        self.driver.swipe_ext("left")  # 屏幕左滑
        time.sleep(0.8)  # 暂停 0.8 秒

    def run(self):
        print(">>> 启动米读极速版 APP")
        self.start_app()
        print(">>> 开始执行<阅读>任务")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time <= self.run_time:
            print("=" * 50)
            print(">>> 正在阅读第 %s 页小说" % count)
            # 开始阅读
            self.read()
            rest_time = int(self.run_time - (time.time() - start_time))
            h = int(rest_time / 3600)
            m = int((rest_time - h * 3600) / 60)
            s = int(rest_time - h * 3600 - m * 60)
            print(">>> 剩余任务时间：{} 时 {} 分 {} 秒".format(h, m, s))
            print("=" * 50 + "\n")
            count += 1
        print(">>> <阅读>执行完毕，共阅读 %s 页小说" % count)
        print(">>> 退出应用")
        self.driver.app_stop(self.app_name)


if __name__ == "__main__":
    app_name = "com.lechuan.mdwz"
    run_time = 1800  # 指定运行时间
    midu = Midu(app_name, run_time)
    midu.run()
