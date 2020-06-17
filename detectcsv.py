import os
def detect():
    listdir = os.listdir(os.getcwd())
    ans = {
        '电院老师信息.csv': False,
        '全校老师信息.csv': False,
        '点击量最高的前十位老师.csv': False
    }
    for file in listdir:
        if file == '点击量最高的前十位老师.csv':
            ans['点击量最高的前十位老师.csv'] = True
        elif file == '全校老师信息.csv':
            ans['全校老师信息.csv'] = True
        elif file == '电院老师信息.csv':
            ans['电院老师信息.csv'] = True
    return ans

def to_str():
    ans = detect()
    text = ''
    for key, val in ans.items():
        if val == False:
            text += key + '不在当前路径' + '\n'
        else:
            text += key + '就在当前路径' + '\n'
        pass

    return text