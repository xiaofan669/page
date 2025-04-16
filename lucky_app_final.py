import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
import sys
import ctypes

def get_resource_path(relative_path):
    """ 获取资源的绝对路径，兼容打包后和开发环境 """
    try:
        # 打包后的资源路径
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境的资源路径
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def open_html_file(html_file):
    try:
        # 获取HTML文件路径（自动适应不同电脑）
        html_path = get_resource_path(html_file)
        
        if not os.path.exists(html_path):
            messagebox.showerror("错误", f"找不到文件: {html_file}")
            return
        
        # 用默认浏览器打开
        webbrowser.open_new(html_path)
        
    except Exception as e:
        messagebox.showerror("错误", f"无法打开文件: {str(e)}")

def create_gui():
    root = tk.Tk()
    root.title("命运选择器")
    root.geometry("300x150")
    root.resizable(False, False)
    
    # 设置窗口图标（可选）
    try:
        icon_path = get_resource_path("app.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except:
        pass
    
    tk.Label(root, text="请选择你的命运:", 
           font=("微软雅黑", 14)).pack(pady=10)
    
    tk.Button(root, text="Lucky", 
             command=lambda: open_html_file("Lucky.HTML"),
             bg="green", fg="white", width=15).pack(pady=5)
    
    tk.Button(root, text="UnLucky",
             command=lambda: open_html_file("UnLucky.HTML"),
             bg="red", fg="white", width=15).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()