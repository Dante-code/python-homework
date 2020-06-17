from mttkinter.mtTkinter import *
import school
import eleinstitute
import threading
import time
import detectcsv


def spider_gui():
    """
    爬虫GUI界面
    :return:
    """

    def init_run(s: str):
        """
        运行爬虫的函数
        :param s: 输入要执行的参数。选择爬全校还是爬电院
        :return:
        """

        # 启动子进程，并保证父进程结束时子进程跟着结束
        th[s].setDaemon(True)
        th[s].start()

        # 消去爬虫按钮，防止用户多次点击导致程序频繁多次创建子进程。
        choose_button_ele.destroy()
        choose_button_all.destroy()
        jump_button.destroy()

        Label(wd, text="正在爬取数据请稍等").grid()
        pass

    def detect():
        """
        检测当前目录下是否有目标文件
        :return:
        """
        text = detectcsv.to_str()
        detect_label = Label(wd, bg='white', width=35, height=5, text=text)
        detect_label.place(x=450, y=250, anchor='center')

        # 开启一个定时器，一段时间后把刚刚生成的Label清理掉
        timer = threading.Timer(2, detect_label.destroy)
        timer.setDaemon(True)
        timer.start()

        pass

    def jump_to_othergui():
        """
        结束当前的GUI界面，跳到搜索的GUI界面
        :return:
        """
        from searchGUI import MY_GUI
        # -----------结束当前窗口
        wd.quit()
        wd.destroy()
        # -----------
        # 实例化对象启动另一个GUI窗口
        MY_GUI().init_window_name.mainloop()
        pass

    th = {
        # 多线程对象
        '电院': threading.Thread(target=eleinstitute.main),
        '全校': threading.Thread(target=school.main)
    }

    # 实例化一个TK对象
    wd = Tk()
    wd.title('启动')
    # 设置窗口大小
    wd.geometry('600x338')
    # ------------------- 锁定窗口大小
    wd.minsize(600, 338)
    wd.maxsize(600, 338)
    # -------------------

    canvas = Canvas(wd, bd=0, highlightthickness=0, width=600, height=338)  # 实例化一个canvas对象

    # ------------------- 实例化四个Button对象
    choose_button_ele = Button(wd, text='爬取电院老师信息', bg="lightblue", width=25, height=1,
                               command=lambda: init_run('电院'))
    choose_button_all = Button(wd, text='爬取全校老师信息', bg="lightblue", width=25, height=1,
                               command=lambda: init_run('全校'))
    detect_button = Button(wd, text='检查当前目录是否有目标文件', bg='PaleVioletRed', width=25, height=1,
                           command=lambda: detect())
    jump_button = Button(wd, text='跳转到搜索窗口', bg='PaleVioletRed', width=25, height=1,
                         command=lambda: jump_to_othergui())
    # -------------------

    # 加载图片
    img = PhotoImage(file='img/spider_setting.gif')
    canvas.create_image(0, 0, anchor='nw', image=img)

    # -------------------- 进行place布局
    choose_button_ele.place(x=100, y=100)
    choose_button_all.place(x=100, y=150)
    detect_button.place(x=100, y=200)
    jump_button.place(x=100, y=50)
    canvas.place(x=0, y=0)
    # --------------------

    # ---------------------开始刷新页面
    flag = 0
    status = True
    while status:
        try:
            wd.update()  # 不断刷新页面
        except:
            break
        #观测当前爬虫程序是否正在运行
        isrun = th['电院'].is_alive() | th['全校'].is_alive()
        if status == isrun and flag == 0:
            #刚开始启动程序的时候 爬虫程序处于待命状态，而并不是爬虫程序结束之后的状态
            #status == isrun 代表爬虫已经开始。子进程状态改变，需要记录一次
            flag = 1
            pass
        if status != isrun and flag == 1:
            #flag = 1代表之前子线程发生了一次状态的改变
            #现在又发生了一次改变，这说明爬虫程序结束了
            jump_to_othergui()
            break
        #调慢刷新速度
        time.sleep(0.1)
    # ---------------------

    '''
    从上面循环出来的条件：
        1.完成了一次爬虫程序,然后跳到另一个GUI界面上
        2.执行了jump_to_othergui()。爬虫GUI被销毁,wd.update()报错,从except的break跳出
    执行try/except 保证程序不会报错终止
    '''
    pass
