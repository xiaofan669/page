import os
import tkinter as tk
from tkinter import messagebox
import webbrowser
import platform
import pyautogui  # 确保已导入

def modify_html_file(file_path):
    """修改HTML文件，添加最大化窗口的JavaScript代码"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经添加过最大化代码
        if 'window.resizeTo' not in content:
            # 在第一个</body>标签前插入最大化代码
            js_code = """
<script>
// 最大化窗口
window.moveTo(0, 0);
if (window.outerWidth < screen.width || window.outerHeight < screen.height) {
    window.resizeTo(screen.width, screen.height);
}
</script>
"""
            content = content.replace('</body>', js_code + '</body>', 1)
            
            # 写入修改后的内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    except Exception as e:
        print(f"修改HTML文件时出错: {str(e)}")

def open_html_file(filename):
    try:
        # 获取当前exe所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, filename)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            messagebox.showerror("错误", f"找不到文件: {filename}")
            return
            
        
        # 使用默认浏览器打开HTML文件
        webbrowser.open(file_path)
        
    except Exception as e:
        messagebox.showerror("错误", f"打开文件时出错: {str(e)}")

def on_lucky():
    open_html_file("Lucky.html")

def on_unlucky():
    open_html_file("UnLucky.html")

def create_gui():
    root = tk.Tk()
    root.title("选择你的命运")
    
    # 设置窗口大小（固定大小）
    root.geometry("600x400")  # 设置固定大小
    
    # 不置顶
    root.attributes('-topmost', False)
    
    # 创建主框架
    frame = tk.Frame(root)
    frame.pack(expand=True, fill='both')
    
    # 添加说明标签
    label = tk.Label(frame, text="请选择你的命运:", font=('Arial', 24))
    label.pack(pady=(50, 30))
    
    # 创建按钮框架
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=20)
    
    # 添加奖励按钮
    lucky_btn = tk.Button(
        button_frame, 
        text="奖励 Lucky", 
        command=on_lucky,
        bg='green', 
        fg='white',
        font=('Arial', 18),
        width=15,
        height=3
    )
    lucky_btn.pack(side='left', padx=20)
    
    # 添加惩罚按钮
    unlucky_btn = tk.Button(
        button_frame, 
        text="惩罚 UnLucky", 
        command=on_unlucky,
        bg='red', 
        fg='white',
        font=('Arial', 18),
        width=15,
        height=3
    )
    unlucky_btn.pack(side='left', padx=20)
    
    # 添加退出按钮
    exit_btn = tk.Button(
        frame, 
        text="退出", 
        command=root.destroy,
        font=('Arial', 14),
        width=10,
        height=1
    )
    exit_btn.pack(pady=50)
    
    return root

if __name__ == "__main__":
    # 检查操作系统是否为Windows
    if platform.system() != 'Windows':
        print("此程序仅支持Windows系统")
        exit(1)
        
    app = create_gui()
    app.mainloop()