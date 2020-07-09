# import packages
from packages import *
import time


class AutoRead():
    def __init__(self):
        # self.app_name_list = ["com.songheng.eastnews", "com.ss.android.ugc.aweme.lite", "com.cashtoutiao",
        #                       "com.ss.android.ugc.livelite", "com.ss.android.article.lite", "com.kuaishou.nebula",
        #                       "com.lechuan.mdwz", "com.qujianpan.client.fast", "com.zhangku.qukandian",
        #                       "com.jifen.qukan", "com.jm.video", "com.coohua.xinwenzhuan", "cn.youth.news",
        #                       "com.ldzs.zhangxin", ]
        # self.app_name_zh_list = ["东方头条", "抖音极速版", "惠头条", "火山极速版", "今日头条极速版", "快手极速版",
        #                          "米读极速版", "趣键盘极速版", "趣看点", "趣头条", "刷宝", "淘新闻", "中青看点",
        #                          "蚂蚁看点", ]
        self.run_time = 2500
        self.task_list = {
            "东方头条": DongfangNews.DongfangNews("com.songheng.eastnews", self.run_time),
            "抖音极速版": Douyin.Douyin("com.ss.android.ugc.aweme.lite", self.run_time),
            "惠头条": Huitoutiao.Huitoutiao("com.cashtoutiao", self.run_time),
            "火山极速版": Huoshan.Huoshan("com.ss.android.ugc.livelite", self.run_time),
            "今日头条极速版": Jinritoutiao.Jinritoutiao("com.ss.android.article.lite", self.run_time),
            "快手极速版": Kuaishou.Kuaishou("com.kuaishou.nebula", self.run_time),
            "米读极速版": Midu.Midu("com.lechuan.mdwz", self.run_time),
            "趣键盘极速版": Qujianpan.Qujianpan("com.qujianpan.client.fast", self.run_time),
            "趣看点": Qukandian.Qukandian("com.zhangku.qukandian", self.run_time),
            "趣头条": Qutoutiao.Qutoutiao("com.jifen.qukan", self.run_time),
            "刷宝": Shuabao.Shuabao("com.jm.video", self.run_time),
            "淘新闻": TaoNews.TaoNews("com.coohua.xinwenzhuan", self.run_time),
            "中青看点": Zhongqingkandian.Zhongqingkandian("cn.youth.news", self.run_time),
            "蚂蚁看点": Antkandian.Antkandian("com.ldzs.zhangxin", self.run_time),
        }

    def run(self):
        keys = [key for key in self.task_list.keys()]
        # print(">>> 任务列表：", "，".join(self.self.app_name_zh_list))
        print(">>> 任务列表：", "，".join(keys))
        time.sleep(1)
        for i in range(len(keys)):
            print(">>> 执行<%s>任务" % keys[i])
            self.task_list[keys[i]].run()
            print(">>> <%s>任务执行完毕" % keys[i])
            print(">>> 切换到下一个任务")
            time.sleep(60)
        print(">>> 所有任务执行完毕")


if __name__ == "__main__":
    autoread = AutoRead()
    autoread.run()
