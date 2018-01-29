import time
import traceback
from splinter.browser import Browser

# 用户名，密码
username = "username"
passwd = "passwd"

# 起始地址的cookies,在cookie中查找。下面是北京到鹤壁东
starts = "%u5317%u4EAC%2CBJP"
ends = "%u9E64%u58C1%u4E1C%2CHFF"
dtime = "2018-1-18"

# 车次，选择第几趟，从1数
order = 15

# 设定网址
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"

#设置预定抢票时间(时间格式固定)
plan_time = "Sat Dec 23 11:42:00 2017"

# 登录
def login():
    b.find_by_text(u"登录").click()
    time.sleep(1)
    b.fill("loginUserDTO.user_name", username)
    time.sleep(1)
    b.fill("userDTO.password", passwd)
    time.sleep(1)

    print("选择验证码")
    while True:
        if b.url != initmy_url:
            time.sleep(0.5)
        else:
            break

# 购票
def huoche():
    global b
    b = Browser(driver_name="chrome")
    # 返回购票页面
    b.visit(ticket_url)
    while b.is_text_present(u"登录"):
        time.sleep(1)
        login()
        if b.url == initmy_url:
            print('已登陆')
            break

    while True:
        print('正在等待预定时间')
        local_time = time.time()  # 当前时间的时间戳
        plan_time_stamp = time.mktime(time.strptime(plan_time, "%a %b %d %H:%M:%S %Y"))  # 计划时间的时间戳
        time_difference = local_time - plan_time_stamp  # 时间差值
        if time_difference < 0:
            time.sleep(1)
        else:
            break

    try:
        print("时间到，进入购票页面...")
        # 跳回购票页面
        b.visit(ticket_url)

        # 加载查询信息
        b.cookies.add({"_jc_save_fromStation": starts})
        b.cookies.add({"_jc_save_toStation": ends})
        b.cookies.add({"_jc_save_fromDate": dtime})
        b.reload()
        time.sleep(1)

        count = 0
        # 循环点击预订
        while b.url == ticket_url:
            b.find_by_text(u"查询").click()
            # 程序自动点击查询后，结果如下：
            count += 1
            print("循环点击查询... 第 %s 次" % count)
            time.sleep(1)
            b.find_by_text("预订")[order - 1].click()
            print('已点击预定')
            time.sleep(1)
            #这里的乘客默认选择第一个
            b.find_by_id('normalPassenger_0')[0].click()
            print('已选择乘客')
            time.sleep(1)
            #这里的席别对应select中option的value值
            b.find_option_by_value(0).click()
            print('已选择席别')
            time.sleep(1)
            b.find_by_id('submitOrder_id')[0].click()
            print('已提交订单,待确认')
            time.sleep(1)
            b.find_by_id('qr_submit_id')[0].click()
            print('已确认,请前去付款')
        time.sleep(1)

        print("结束")

    except Exception as e:
        print(traceback.print_exc())

if __name__ == "__main__":
    huoche()
