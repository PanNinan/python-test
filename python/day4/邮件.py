from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP


def main():
    # 请自行修改下面的邮件发送者和接收者
    sender = '982397045@qq.com'
    receivers = ['393956371@qq.com', '753710287@qq.com', 'panninan@126.com', '18761697746@163.com']
    message = MIMEText('用Python发送邮件的示例代码.', 'plain', 'utf-8')
    message['From'] = Header('潘', 'utf-8')
    message['To'] = Header('X-X:)', 'utf-8')
    message['Subject'] = Header('示例代码实验邮件', 'utf-8')
    smtper = SMTP('smtp.qq.com')
    # 请自行修改下面的登录口令
    smtper.login(sender, 'pyqerahaiepybcag')
    smtper.sendmail(sender, receivers, message.as_string())
    print('邮件发送完成!')


if __name__ == '__main__':
    main()
