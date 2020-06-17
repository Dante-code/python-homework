# from tkinter import *
from mttkinter.mtTkinter import *
import re
from functools import reduce
from spiderGUI import spider_gui
import time
import detectcsv


class MY_GUI():
    batch_size = 42  # 一页的教师数
    page_idx = 0  # 页面索引

    def __init__(self):
        """
        初始化对象
        """
        # 实例化一个Tk对象
        self.init_window_name = Tk()
        # 初始化窗口
        self.set_init_window()
        self.init_basic_layout()
        self.init_window_name.mainloop()

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("西电教师信息")  # 窗口名
        # 设置窗口大小
        self.init_window_name.geometry('665x675')
        # ------------------- 锁定窗口大小
        self.init_window_name.maxsize(665, 675)
        self.init_window_name.minsize(665, 675)
        # -------------------

        self.teacher1_info_button = []

        # 实例化一个canvas对象
        self.canvas = Canvas(self.init_window_name, bd=0,
                             highlightthickness=0, width=1920, height=1080)
        # 加载图片
        self.img = PhotoImage(file='img/search_setting.gif')
        self.canvas.create_image(0, 0, anchor='nw', image=self.img)
        # 标签
        self.result_data_label = Label(self.canvas, text="教师详细信息")
        # 处理结果展示
        self.result_data_Text = Text(self.canvas, width=70, height=43)
        # 搜索框
        self.search_data_Text = Text(self.canvas, width=70, height=10)
        self.search_data_label = Label(self.canvas, text="搜索框")
        self.how_to_use_button = Button(self.canvas, text='使用教程', bg="lightblue", width=20, height=2,
                                        command=self.how_to_use, font=('Arial', 10))
        # 搜索按钮创造
        self.search_button = Button(self.canvas, text="搜索", bg="lightblue", width=20, height=2,
                                    command=self.search, font=('Arial', 10))
        # 清屏按钮创造
        self.clear_all_button = Button(self.canvas, text="清屏", bg="lightblue", width=20, height=2,
                                       command=self.clear, font=('Arial', 10))

        # 创造一个菜单栏
        self.menu = Menu(self.init_window_name)
        # 创建一个子菜单
        self.child_menu = Menu(self.menu, tearoff=0)
        # 为子菜单添加组件
        self.add_pattern_for_child_menu()

        # 为主菜单添加组件
        self.menu.add_cascade(label='查看目标文件', menu=self.child_menu)
        self.menu.add_command(label="我的爬虫", command=lambda: self.turn_othergui())
        self.menu.add_command(label="退出", command=lambda: self.init_window_name.destroy())

    def turn_othergui(self):
        self.init_window_name.destroy()
        spider_gui()
        pass

    def add_pattern_for_child_menu(self):
        """
        为子菜单添加组件
        :return:
        """

        ans = detectcsv.detect()  # 查看当前目录是否有目标文件
        flag = 1
        self.ans = ans

        # ------------------ 定义一个函数来遍历ans
        def func(self):
            flag = 1
            for key, val in ans.items():
                if val:
                    # 如果有，则创建一个Label
                    self.show_this_file(key)
                    flag = 0
            return flag

        # 如果flag仍然为1，则说明没有目标文件
        flag = func(self)
        if flag:
            self.child_menu.add_command(label='当前目录没有目标文件可供读取，请前往“我的爬虫”')
            pass

    def show_this_file(self, key):
        """
        为子菜单创造Label
        :param key: 文件名字
        :return:
        """
        # 绑定读取文件的事件
        self.child_menu.add_command(label=key, command=lambda: self.readfile(path=key))
        pass

    def create_turnpage_button(self):
        Button(self.canvas, text='上一页', bg='lightblue', width=10,
               command=lambda: self.turn_page('back')
               ).grid(row=0, column=0)

        Button(self.canvas, text='下一页', bg='lightblue', width=10,
               command=lambda: self.turn_page('next')
               ).grid(row=0, column=5)
        pass

    def readfile(self, path: str):
        """
        读取目标文件
        :param path: 文件路径
        :return:
        """
        # 改变窗口的大小
        self.init_window_name.geometry('1145x681+180+70')
        # ------------------- 锁定窗口大小
        self.init_window_name.minsize(1145, 681)
        self.init_window_name.maxsize(1145, 681)
        # -------------------
        # 创造翻页的按钮
        self.create_turnpage_button()

        # -------------------- 开始读取文件
        with open(path, 'r', encoding='ANSI') as file:
            pattern = re.compile(r'[,\n]')
            '''
            self.file 读入csv文件，并创建一个二维列表来储存老师的信息
            注意这里的csv文件必须是最初的csv文件
            self.dic  创建一个字典，存放  (key)老师名字与(value)索引的键值对。减少search函数的搜索时间
            '''
            self.file = [pattern.split(fr)[:-1] for fr in file.readlines()]
            # 得到总教师数
            self.totalnum = len(self.file)

            self.dic = {teacher[0]: idx for idx, teacher in enumerate(self.file)}
            file.close()
            pass
        pass
        # --------------------
        # 刷新页面
        self.page_idx = 0
        self.refresh_page()

    def create_button(self, name, num):
        """
        用来创造老师按钮的函数
        :param name: 老师的名字
        :param num: 老师的索引号
        :return:
        """
        # 绑定一个显示老师信息的方法
        self.teacher1_info_button.append(Button(self.canvas, text=name, bg="lightblue", width=10,
                                           command=lambda: self.show_teacher_info(
                                               name)))
        self.teacher1_info_button[len(self.teacher1_info_button)-1].grid(row=num // 6 + 2, column=num % 6 + 0)

    def init_basic_layout(self):
        self.init_window_name.config(menu=self.menu)
        self.canvas.place(x=0, y=0)
        self.clear_all_button.grid(row=17, column=22)
        self.result_data_label.grid(row=0, column=12)
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.search_data_Text.grid(row=10, column=12, rowspan=16, columnspan=10)
        self.how_to_use_button.grid(row=1, column=22)
        self.search_button.grid(row=18, column=22)
        pass

    def how_to_use(self):
        self.clear()
        how_to_use_info = '''
注意：
1 每次出现的教师信息会打印在顶端，而非底端
2 点击按钮出现对应老师信息，

3 清屏按钮在右下角,若不想清除全部信息请直接框选希望删除的信息,
  后backspace删除（这个文本框里的文本都是可以随意更改的）
4 右下角搜索框使用方法：
  输入想要查询的老师名字， 点击 搜索 ,在右上输出框显示老师信息
  请保证搜索框中只有一个老师名字,带来不便还请谅解

5 谢谢使用
'''
        self.result_data_Text.insert(1.0, how_to_use_info)

    def refresh_page(self):
        """
        刷新页面用的
        :return:
        """
        # 开始的索引
        start = self.page_idx * self.batch_size
        # 结束的索引
        end = start + self.batch_size

        # 防止越界
        if end >= self.totalnum:
            end = self.totalnum

        # 根据索引构成区间，创造老师的按钮
        if self.teacher1_info_button:
            for button in self.teacher1_info_button:
                button.destroy()
            self.teacher1_info_button.clear()
        for idx in range(start, end):
            self.create_button(self.file[idx][0], idx % self.batch_size)
            pass
        pass

    def turn_page(self, command: str):
        """
        翻页函数
        :param command: 指令 next下一页  back上一页
        :return:
        """
        if command == 'next':
            if self.page_idx < self.totalnum // self.batch_size:
                self.page_idx += 1
                self.refresh_page()
        elif command == 'back':
            if self.page_idx > 0:
                self.page_idx -= 1
                self.refresh_page()
        pass

    def show_teacher_info(self, name):
        """
        显示老师信息
        :param name: 老师的姓名
        :return:
        """
        self.clear()
        num = self.dic[name]
        info = '\n' + reduce(lambda x, y: x + '\n' + y if y != '无' else x + '', self.file[num]) + '\n'
        self.result_data_Text.insert(1.0, info)
        pass

    def search(self):
        """
        搜索老师的信息
        :return:
        """

        name = self.search_data_Text.get(1.0, END).strip().replace("\n", "")
        try:
            result = self.show_teacher_info(name)
        except:
            self.result_data_Text.delete(1.0, END)
            self.result_data_Text.insert(1.0, "输入有误或程序发生未知异常")

    def clear(self):
        """
        清空
        :return:
        """
        self.result_data_Text.delete(1.0, END)
