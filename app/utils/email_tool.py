import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Email():
    def __init__(self, username='***', password='***', smtp_server='smtp.qq.com'):
        self.smtp_server = smtp_server
        self.username = username
        self.password = password  # 对于QQ邮箱，这里应该使用授权码而不是登录密码

        self.smtp = smtplib.SMTP(self.smtp_server, 587)
        # 加密SMTP
        self.smtp.starttls()
        self.smtp.login(username, password)

    def send(self, receiver='***', title='', text='这是一封测试邮件', image='', time='', Cc=''):
        '''
        构造邮件内容
        教程  https://www.liaoxuefeng.com/wiki/1016959663602400/1017790702398272
        '''
        text = ''.join(['<p>{p}</p>'.format(p=p) for p in text.split('\n')])

        msg = MIMEText(
            '''<html>
                    <body>
                        <h1>{title}</h1>
                        <p>{text}</p>
                        <p>发布时间：{time}</p>
                    </body>
                </html>'''.format(title=title, text=text, time=time),
            _subtype='html',
            _charset='utf-8')
        # msg = MIMEText(msg, 'plain', 'utf-8')  # 中文需参数'utf-8'，单字节字符不需要
        msg['Subject'] = Header(title, 'utf-8')
        msg['From'] = f'hi <{self.username}>'
        msg['To'] = receiver
        msg['Cc'] = Cc

        # 发送邮件
        self.smtp.sendmail(self.username, receiver.split(',') + Cc.split(','), msg.as_string())
        self.smtp.quit()


if __name__ == "__main__":
    # 使用QQ邮箱和授权码
    mail = Email(username="200939540@qq.com", password="lbusspdxzvcrbjcb")
    mail.send(receiver="200939540@qq.com")