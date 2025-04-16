import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
import ctypes
import win32gui # type: ignore
import win32con # type: ignore

hwnd = win32gui.FindWindow(None, "记事本")  # 替换为你的窗口标题
def check_files_exist():
    base_path = r"C:\Users\dell\Desktop\helloweba_guaguaka"
    required_files = ["Lucky.HTML", "UnLucky.HTML"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(os.path.join(base_path, file)):
            missing_files.append(file)
    
    return missing_files

def get_screen_resolution():
    try:
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    except:
        return 1366, 768  # Win7默认回退分辨率

def open_html_windows(html_file):
    try:
        screen_width, screen_height = get_screen_resolution()
        window_width = screen_width // 1
        
        base_path = r"C:\Users\dell\Desktop\helloweba_guaguaka"
        full_path = os.path.join(base_path, html_file)
        
        if not os.path.exists(full_path):
            messagebox.showerror("错误", f"找不到文件: {full_path}")
            return
        
        # 尝试用默认浏览器打开3个窗口
        for i in range(1):
            webbrowser.open_new(full_path)
            win32gui.MoveWindow(hwnd, 100, 200, 800, 600, True)
        
    except Exception as e:
        messagebox.showerror("错误", f"打开窗口失败: {str(e)}")

def create_gui():
    # 首先检查必要文件
    missing_files = check_files_exist()
    if missing_files:
        messagebox.showerror("文件缺失", f"缺少必要文件:\n{', '.join(missing_files)}\n请将这些文件放置在桌面helloweba_guaguaka文件夹中")
        return
    
    root = tk.Tk()
    root.title("选择你的命运")
    root.geometry("300x150")
    
    label = tk.Label(root, text="请选择你的命运:", font=("Arial", 14))
    label.pack(pady=10)
    
    lucky_btn = tk.Button(root, text="Lucky", command=lambda: open_html_windows("Lucky.HTML"), 
                         bg="green", fg="white", width=15)
    lucky_btn.pack(pady=5)
    
    unlucky_btn = tk.Button(root, text="UnLucky", command=lambda: open_html_windows("UnLucky.HTML"), 
                           bg="red", fg="white", width=15)
    unlucky_btn.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()