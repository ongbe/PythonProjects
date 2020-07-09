import uiautomator2 as u2
import time


class Qukandian(object):
    def __init__(self, app_name, run_time):
        self.driver = u2.connect_wifi("192.168.31.18")
        self.app_name = app_name
        self.run_time = run_time

    def start_app(self):
        self.driver.app_start(self.app_name, stop=True)
        # 点击界面上的跳过按钮
        if self.driver(resourceId="com.zhangku.qukandian:id/launch_layout_time").wait():
            self.driver(resourceId="com.zhangku.qukandian:id/launch_layout_time").click()
        # 关闭主界面上的弹窗（如果有）
        if self.driver(resourceId="com.zhangku.qukandian:id/dialog_operate_close").wait(timeout=1):
            self.driver(resourceId="com.zhangku.qukandian:id/dialog_operate_close").click()
        if self.driver(resourceId="com.zhangku.qukandian:id/dialog_recommend_daily_dismiss").wait(timeout=1):
            self.driver(resourceId="com.zhangku.qukandian:id/dialog_recommend_daily_dismiss").click()
        self.driver.swipe(500, 500, 500, 1700)  # 刷新一下
        time.sleep(2)
        # 点击推荐页的第一个新闻
        self.driver.xpath("//*[@resource-id=\"com.zhangku.qukandian:id/base_refresh_recyclerview\"]/android.widget.LinearLayout[1]").wait().click()

    def read(self):
        # 等待弹窗加载完成后（如果有）点击关闭
        if self.driver.xpath("//*[@resource-id=\"com.zhangku.qukandian:id/url_webview\"]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]").wait(timeout=3):
            self.driver.xpath('//*[@resource-id=\"com.zhangku.qukandian:id/url_webview\"]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]').click()
        # 滑 3 次左下角的圈就转完了
        for i in range(3):
            self.driver.swipe(500, 1000, 500, 0, 0.5)
            time.sleep(7)
        self.driver(scrollable=True).scroll.toEnd()  # 滑到页面底部
        # 点击最后一条资讯
        self.driver.xpath("//*[@resource-id=\"com.zhangku.qukandian:id/RecyclerView\"]/android.widget.RelativeLayout").all()[-1].click()

    def run(self):
        print(">>> 启动趣看点 APP")
        self.start_app()
        print(">>> 开始执行<阅读>任务")
        print(">>> 任务时长：%s 小时" % float(self.run_time / 3600))
        start_time = time.time()
        count = 1
        while time.time() - start_time <= self.run_time:
            print("=" * 50)
            print(">>> 正在阅读第 %s 篇文章" % count)
            self.read()
            rest_time = int(self.run_time - (time.time() - start_time))
            h = int(rest_time / 3600)
            m = int((rest_time - h * 3600) / 60)
            s = int(rest_time - h * 3600 - m * 60)
            print("剩余任务时间：{} 时 {} 分 {} 秒".format(h, m, s))
            print("=" * 50 + "\n")
            count += 1
        print(">>> <阅读>执行完毕，共刷 %s 篇文章" % count)
        print(">>> 退出应用")
        self.driver.app_stop(self.app_name)


if __name__ == "__main__":
    app_name = "com.zhangku.qukandian"
    run_time = 1800  # 运行 0.5 小时
    qukandian = Qukandian(app_name, run_time)
    qukandian.run()