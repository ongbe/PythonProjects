#!/usr/bin/python3
'''
license_code qvdmckmmzdpygjdi
'''
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(status_code):
    if status_code:
        message = MIMEText('金币领取成功！')  # 邮件内容
    else:
        message = MIMEText('领取失败！请手动登陆领取')
    message['From'] = Header('小号')  # 邮件发送者名字
    message['To'] = Header('雷书飞')  # 邮件接收者名字
    message['Subject'] = Header('互帮帮金币领取通知')  # 邮件主题

    mail = smtplib.SMTP()
    mail.connect("smtp.qq.com")  # 连接 qq 邮箱
    mail.login("1344424539@qq.com", "qvdmckmmzdpygjdi")  # 账号和授权码
    mail.sendmail("1344424539@qq.com", ["2279981038@qq.com"], message.as_string())  # 发送账号、接收账号和邮件信息
