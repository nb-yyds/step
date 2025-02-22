# -*- coding: utf8 -*-
import math
import traceback
# 必须这样写，才能调用now等方法
from datetime import datetime
# 定义类
from collections import namedtuple
import re


import json
import random
import re
import time
import os

import requests

# 暴露时，需要先在定义，这里面的字符串是固定的写法，比如full_time
TimeInfo = namedtuple('TimeInfo', ['full_time', 'hour', 'minute'])


# 获取北京时间
def get_beijing_time():
    # 通过 pytz 包获取时间，但是这个包经常报错
    # target_timezone = pytz.timezone('Asia/Shanghai')
    # # 获取当前时间
    # return datetime.now().astimezone(target_timezone)

    # 换成调接口获取时间
    hea = {'User-Agent': 'Mozilla/5.0'}
    url = r'https://apps.game.qq.com/CommArticle/app/reg/gdate.php'
    r = requests.get(url=url, headers=hea)
    print(f"==========================================")
    print(f"调用接口获取北京时间为：{r}")
    if r.status_code == 200:
        # 数据为：var json_curdate = '2024-12-10 01:36:38';
        result = r.text
        # 正则表达式
        # pattern = re.compile('\\d{4}-\\d{2}-\\d{2} (\\d{2}):\\d{2}:\\d{2}')
        pattern = re.compile(r'\d{4}-\d{2}-\d{2} (\d{2}):(\d{2}):\d{2}')

        # 搜索匹配项
        find = re.search(pattern, result)
        # 返回的 find 是一个 re.Match 对象。要从中提取匹配到的字符串，可以使用 group() 方法。
        print(f"搜索匹配项为：{find}")

        # 检测是找到匹配项
        if find:
            # 提取完整时间字符串
            fullTime = find.group()
            print("完整时间字符串:", fullTime)

            # 提取小时和分钟
            # 提取小时和分钟（使用正则表达式）
            time_pattern = r"(\d{2}):(\d{2}):\d{2}"  # 匹配 'hh:mm:ss' 格式的时间
            time_match = re.search(time_pattern, fullTime)
            if time_match:
                hour = time_match.group(1)  # 获取小时
                minute = time_match.group(2)  # 获取分钟
            else:
                return None

            # 打印结果
            print(f"==========================================")
            print(f"解析接口的北京时间为：{fullTime} --- {hour}小时 --- {minute}")
            # return datetime.now()
            # return TimeInfo(int(hour), int(minute), fullTime)
            return TimeInfo(
                full_time=fullTime,
                hour=int(hour),
                minute=int(minute),
            )
        else:
            print("解析北京时间字符串失败！")
            return None
    else:
        print("获取北京时间的接口响应失败！")
        return None


# 格式化时间
def format_now():
    # 获取当前的日期和时间
    fullTime = time_bj.full_time
    return fullTime


# 获取默认值转int
def get_int_value_default(_config: dict, _key, default):
    _config.setdefault(_key, default)
    return int(_config.get(_key))


# 获取当前时间对应的最大和最小步数
def get_min_max_by_time(hour=None, minute=None, fullTime=None):
    if hour is None:
        hour = time_bj.hour
    if minute is None:
        minute = time_bj.minute
    if fullTime is None:
        fullTime = time_bj.full_time

    print(f"==========================================")
    print(f"当前北京时间为：完整时间：{fullTime} ---- {hour}小时 --- {minute}分钟 --- ")
    print(f"==========================================")
    print(f"刷步区间值：\n早上9-13点区间步数：1.6w以下\n下午13-18点区间步数：2-2.3w\n晚上18-23点区间步数：2.3w以上")
    print(f"==========================================")

    # 0点为执行高峰，排队可能会延后一两小时才执行
    # 设置的actions自动执行时间为：cron: '0 1,5,10 * * *'
    # 对应的北京时间为：早上9点、下午13点、18点
    # 默认值
    step = None

    # 早上：一般在9:30分触发
    if 7 <= hour < 13:
        step = random.randint(8000, 18000)
    # 下午：一般在13：50分触发
    elif 13 <= hour < 18:
        step = random.randint(20000, 23000)
    # 晚上
    elif 18 <= hour < 23:
        step = random.randint(23100, 26000)
    # 其他
    else:
        # (1000 * (14 + 1)) / 10 = 1500
        # (1000 * (14 + 2)) / 10 = 1600
        # (1000 * (14 + 3)) / 10 = 1600
        step = max(1000 * (hour + minute) // 10, 1)
        


    # 最小值、最大值
    min_step = step
    max_step = (step + 100)
    print(f"当前执行时间：{hour} --- 最小值：{min_step} --- 最大值：{max_step}")
    return int(min_step), int(max_step)



# 虚拟ip地址
def fake_ip():
    # 随便找的国内IP段：223.64.0.0 - 223.117.255.255
    return f"{223}.{random.randint(64, 117)}.{random.randint(0, 255)}.{random.randint(0, 255)}"


# 账号脱敏
def desensitize_user_name(user):
    # 长度小于8
    if len(user) <= 8:
        ln = max(math.floor(len(user) / 3), 1)
        return f'{user[:ln]}***{user[-ln:]}'
    # 长度大于8，取前面2个，后面6个
    return f'{user[:2]}****{user[-7:]}'


# 获取时间戳
def get_time():
    current_time = get_beijing_time()
    return "%.0f" % (current_time.timestamp() * 1000)


# 获取登录code
def get_access_token(location):
    code_pattern = re.compile("(?<=access=).*?(?=&)")
    result = code_pattern.findall(location)
    if result is None or len(result) == 0:
        return None
    return result[0]


# pushplus消息推送
def push_plus(title, content):
    requestUrl = f"http://www.pushplus.plus/send"
    data = {
        "token": PUSH_PLUS_TOKEN,
        "title": title,
        "content": content,
        "template": "html",
        "channel": "wechat"
    }
    try:
        response = requests.post(requestUrl, data=data)
        if response.status_code == 200:
            json_res = response.json()
            print(f"pushplus推送完毕：{json_res['code']}-{json_res['msg']}")
        else:
            print("pushplus推送失败")
    except:
        print("pushplus推送异常")


class MiMotionRunner:
    def __init__(self, _user, _passwd):
        user = str(_user)
        password = str(_passwd)
        self.invalid = False
        self.log_str = ""
        if user == '' or password == '':
            self.error = "用户名或密码填写有误！"
            self.invalid = True
            pass
        self.password = password
        if ("+86" in user) or "@" in user:
            user = user
        else:
            user = "+86" + user
        if "+86" in user:
            self.is_phone = True
        else:
            self.is_phone = False
        self.user = user
        self.fake_ip_addr = fake_ip()
        self.log_str += f"创建虚拟ip地址：{self.fake_ip_addr}\n"


    # 主函数
    def login_and_post_step(self, min_step, max_step):
        if self.invalid:
            return "账号或密码配置有误", False

        step = str(random.randint(min_step, max_step))
        self.log_str += f"已设置为随机步数范围({min_step}~{max_step}) 随机值:{step}\n"

        # 完整时间
        date_str = time_bj.full_time
        # 使用 strptime 解析字符串为 datetime 对象
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        # 时间戳
        t = dt.timestamp()

        # 请求地址
        url = f'https://api.faithxy.com/motion/api/motion/Xiaomi?t={t}'
        head = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "api.faithxy.com",
            "Referer": "http://8.140.250.130/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "X-Forwarded-For": self.fake_ip_addr
        }

        data = {
            "phone": f"{self.user}",
            "pwd": f"{self.password}",
            "num": f"{step}",
        }

        print(f"准备发送请求：当前完整时间为：{date_str}, 账号信息：{desensitize_user_name(self.user)}")

        response = requests.post(url, data=data, headers=head)
        json_res = response.json()
        print(f"请求地址：{url}, \n接口响应数据：{response}, \njson格式：{json_res}")

        return f"修改步数（{step}）[" + json_res['msg'] + "]", True



# 启动主函数
def push_to_push_plus(exec_results, summary):
    # 判断是否需要pushplus推送
    if PUSH_PLUS_TOKEN is not None and PUSH_PLUS_TOKEN != '' and PUSH_PLUS_TOKEN != 'NO':
        if PUSH_PLUS_HOUR is not None and PUSH_PLUS_HOUR.isdigit():
            if time_bj.hour != int(PUSH_PLUS_HOUR):
                print(f"当前设置push_plus推送整点为：{PUSH_PLUS_HOUR}, 当前整点为：{time_bj.hour}，跳过推送")
                return
        html = f'<div>{summary}</div>'
        if len(exec_results) >= PUSH_PLUS_MAX:
            html += '<div>账号数量过多，详细情况请前往github actions中查看</div>'
        else:
            html += '<ul>'
            for exec_result in exec_results:
                success = exec_result['success']
                if success is not None and success is True:
                    html += f'<li><span>账号：{exec_result["user"]}</span>刷步数成功，接口返回：{exec_result["msg"]}</li>'
                else:
                    html += f'<li><span>账号：{exec_result["user"]}</span>刷步数失败，失败原因：{exec_result["msg"]}</li>'
            html += '</ul>'
        push_plus(f"{format_now()} 刷步数通知", html)


def run_single_account(total, idx, user_mi, passwd_mi):
    idx_info = ""
    if idx is not None:
        idx_info = f"[{idx+1}/{total}]"
    log_str = f"[{format_now()}]\n{idx_info}账号：{desensitize_user_name(user_mi)}"
    try:
        runner = MiMotionRunner(user_mi, passwd_mi)
        exec_msg, success = runner.login_and_post_step(min_step, max_step)
        log_str += runner.log_str
        log_str += f'{exec_msg}\n'
        exec_result = {"user": user_mi, "success": success,
                       "msg": exec_msg}
    except:
        log_str += f"执行异常:{traceback.format_exc()}\n"
        log_str += traceback.format_exc()
        exec_result = {"user": user_mi, "success": False,
                       "msg": f"执行异常:{traceback.format_exc()}"}
    print(log_str)
    return exec_result


def execute():
    user_list = users.split('#')
    passwd_list = passwords.split('#')
    exec_results = []
    if len(user_list) == len(passwd_list):
        idx, total = 0, len(user_list)
        if use_concurrent:
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                exec_results = executor.map(lambda x: run_single_account(total, x[0], *x[1]), enumerate(zip(user_list, passwd_list)))
        else:
            for user_mi, passwd_mi in zip(user_list, passwd_list):
                exec_results.append(run_single_account(total, idx, user_mi, passwd_mi))
                idx += 1
                if idx < total:
                    # 每个账号之间间隔一定时间请求一次，避免接口请求过于频繁导致异常
                    time.sleep(sleep_seconds)

        success_count = 0
        push_results = []
        for result in exec_results:
            push_results.append(result)
            if result['success'] is True:
                success_count += 1
        summary = f"\n执行账号总数{total}，成功：{success_count}，失败：{total - success_count}"
        print(summary)
        push_to_push_plus(push_results, summary)
    else:
        print(f"账号数长度[{len(user_list)}]和密码数长度[{len(passwd_list)}]不匹配，跳过执行")
        exit(1)


if __name__ == "__main__":
    # 北京时间
    time_bj = get_beijing_time()
    if os.environ.__contains__("CONFIG") is False:
        print("未配置CONFIG变量，无法执行")
        exit(1)
    else:
        # region 初始化参数
        config = dict()
        try:
            config = dict(json.loads(os.environ.get("CONFIG")))
        except:
            print("CONFIG格式不正确，请检查Secret配置，请严格按照JSON格式：使用双引号包裹字段和值，逗号不能多也不能少")
            traceback.print_exc()
            exit(1)
        PUSH_PLUS_TOKEN = config.get('PUSH_PLUS_TOKEN')
        PUSH_PLUS_HOUR = config.get('PUSH_PLUS_HOUR')
        PUSH_PLUS_MAX = get_int_value_default(config, 'PUSH_PLUS_MAX', 30)
        sleep_seconds = config.get('SLEEP_GAP')
        if sleep_seconds is None or sleep_seconds == '':
            sleep_seconds = 5
        sleep_seconds = float(sleep_seconds)
        users = config.get('USER')
        passwords = config.get('PWD')
        if users is None or passwords is None:
            print("未正确配置账号密码，无法执行")
            exit(1)
        min_step, max_step = get_min_max_by_time()
        use_concurrent = config.get('USE_CONCURRENT')
        if use_concurrent is not None and use_concurrent == 'True':
            use_concurrent = True
        else:
            print(f"多账号执行间隔：{sleep_seconds}")
            use_concurrent = False
        # endregion
        execute()
