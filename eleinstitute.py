# -*-coding:gb2312-*-

from selenium import webdriver
import selenium


def buildTojson(info: str, name):
    '''
    :param info: 一个字符串，以换行符分割各项，内部以:分开
    :param name: 一个列表，[老师姓名，点击数]
    :return: 返回一个封装好的字典
    '''
    form = '姓名：' + name[0] + ','
    form += '职称：'
    form += info.replace('\n', ',') + ','
    form += '点击量：' + name[1]
    return form


def getinfo(webdriver):
    '''
    选中老师主页中容纳老师个人信息的标签
    :return: 返回一个web-element 对象
    '''
    try:
        info = webdriver.find_element_by_css_selector('.t_jbxx_nr')
    except selenium.common.exceptions.NoSuchElementException:
        try:
            info = webdriver.find_element_by_css_selector('.jjside')
        except selenium.common.exceptions.NoSuchElementException:
            try:
                info = webdriver.find_element_by_css_selector('.jbxx')
            except selenium.common.exceptions.NoSuchElementException:
                info = webdriver.find_element_by_css_selector('.gdt')
    return info


def load_csc(d):
    ls = []
    for line in d:
        ls.append(line.split(','))
    # del ls[28], ls[56], ls[280]  #处理个别异常
    # 获得label和二维字典列表dic
    label = []
    dic = []
    for line in ls:
        temp = {}
        for i in line:
            try:
                temp[i.split('：')[0]] = i.split('：')[1]
                if i.split('：')[0] not in label:
                    label.append(i.split('：')[0])
            except:
                continue
        dic.append(temp)

        # 重新写入列表dic
    with open('电院老师信息.csv', 'w+', encoding='ANSI') as fw:
        fw.write(','.join(label) + '\n')  # 标题
        for line in dic:
            temp = ''
            for key in label:
                temp += line.get(key, '无') + ','  # 每一行
            fw.write(temp[:-1] + '\n')

    with open('点击量最高的前十位老师.csv', 'w+', encoding='ANSI') as fw:
        fw.write(','.join(label) + '\n')
        topTen = sorted(dic, key=lambda info: int(info['点击量']), reverse=True)
        for line in topTen[:10]:
            temp = ''
            for key in label:
                temp += line.get(key, '无') + ','
            fw.write(temp[:-1] + '\n')

def main():

    wd = webdriver.Chrome('chromedriver.exe')

    # --------------- 实际运行网址
    wd.get(
        'https://faculty.xidian.edu.cn/xyjslb.jsp?urltype=tsites.CollegeTeacherList&wbtreeid=1001&st=0&id=1583&lang=zh_CN#collegeteacher')
    # ---------------

    # --------------- 测试专用网址
    # wd.get(
    #     'https://faculty.xidian.edu.cn/xyjslb.jsp?totalpage=16&PAGENUM=16&urltype=tsites.CollegeTeacherList&wbtreeid=1001&st=0&id=1583&lang=zh_CN'
    # )
    # ---------------
    wd.implicitly_wait(10)  # 隐式等待10s

    d = []  # 定义一个列表，列表每一项都是一个字典
    '''
    d: 最后写进去的字典
    '''
    try:
        while True:
            elementsa = wd.find_elements_by_css_selector('.sypics')  # 得到a标签
            elementsname = wd.find_elements_by_css_selector('.name')  # 得到span标签
            print(len(elementsa))  # 输出当前页面老师个数

            for name, ele in zip(elementsname, elementsa):
                nametext = name.text
                ele.click()  # 点开了超链接，打开了一个新窗口
                wd.switch_to.window(wd.window_handles[-1])  # 进入a标签超链接所指向的那个页面窗口
                info = getinfo(wd)  # 得到容纳信息的标签

                form = buildTojson(info.text, nametext.split('\n'))
                d.append(form)

                wd.close()  # 把老师个人页面页面关了
                wd.switch_to.window(wd.window_handles[0])  # 又返回原来的页面

            # 下一页
            wd.get(wd.find_elements_by_css_selector('.Next')[0].get_attribute('href'))
            # 当到最后一页时就直接通过报错进入except然后写入json文件

    except Exception as error:
        # 把错误输出来。可有可无
        print(error)
        # 关闭页面
        wd.close()

    #关闭驱动程序
    load_csc(d)
    wd.quit()
    wd.stop_client()

