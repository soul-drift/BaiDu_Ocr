import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from aip import AipOcr
import os

""" 我的 APPID AK SK """
APP_ID = '你的 App ID'
API_KEY = '你的 Api Key'
SECRET_KEY = '你的 Secret Key'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def recognize_and_save(a, b):
    """ 识别图片中的文字并保存到文件 """
    # 读取文件
    def get_file_content(filePath):
        with open(filePath, "rb") as fp:
            return fp.read()

    # 自己使用时根据自己的实际地址进行修改
    image = get_file_content(a)

    # 调用通用文字识别（标准版）
    result = client.basicGeneral(image)

    def handel_data(data):
        """ 提取结果 """
        data ='\n'.join([i['words'] for i in data['words_result']])
        return data

    result = handel_data(result)

    # 自己使用时根据自己的实际地址进行修改
    file = open(b, "w")

    # 将文本写入文件
    file.write(result)

    # 关闭文件
    file.close()

# 创建一个窗口对象
window = tk.Tk()

# 设置窗口标题
window.title("图片上传")

# 创建一个函数，用于选择文件
def choose_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        # 打开图片文件并展示在窗口中
        image = Image.open(file_path)
        # 限制图片的大小为最大700x700像素
        image.thumbnail((700, 700))
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo

# 创建一个函数，用于获取选中的图片地址
def get_file_path():
    global file_path,image_path,output_path
    image_path=file_path
    # 获取文件名和扩展名
    file_name, file_ext = os.path.splitext(file_path)
    # 替换扩展名为 "_output.txt"
    output_path = file_name + "_output.txt"
    recognize_and_save(image_path, output_path)
    messagebox.showinfo("成功", "请在图片所在文件夹查看识别结果")

# 创建一个按钮，用于选择文件
btn = tk.Button(window, text="选择文件", command=choose_file, width=10)
btn.grid(row=0, column=0, padx=10, pady=10)

# 创建一个按钮，用于获取选中的图片地址
btn_get_path = tk.Button(window, text="识别并保存", command=get_file_path, width=10)
btn_get_path.grid(row=0, column=1, padx=10, pady=10)

# 将两个按钮居中排列
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# 创建一个标签，用于展示图片
image_label = tk.Label(window)
image_label.grid(row=1, column=0, columnspan=2, pady=10)

# 设置窗口大小和位置
window.geometry("800x700+500+400")

# 运行窗口
window.mainloop()