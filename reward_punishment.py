import os
import tkinter as tk
from tkinter import messagebox
import webbrowser
import platform
import sys

def modify_html_file(file_path):
    """修改HTML文件，添加最大化窗口的JavaScript代码（兼容Windows 7）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经添加过最大化代码
        if 'window.resizeTo' not in content:
            # 使用兼容性更好的全屏代码
            js_code = """
<script>
// 兼容Windows 7的全屏代码
function resizeWindow() {
    try {
        window.moveTo(0, 0);
        if (document.all) {
            top.window.resizeTo(screen.availWidth, screen.availHeight);
        } else if (window.launch) {
            window.launch().then(function() {
                window.resizeTo(screen.availWidth, screen.availHeight);
            });
        } else {
            window.resizeTo(screen.width, screen.height);
        }
    } catch(e) {
        console.log("全屏错误: " + e.message);
    }
}
window.onload = resizeWindow;
</script>
"""
            content = content.replace('</body>', js_code + '</body>', 1)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    except Exception as e:
        print(f"修改HTML文件时出错: {str(e)}")

def open_html_file(filename):
    try:
        # 获取当前脚本所在目录
        if getattr(sys, 'frozen', False):
            # 打包后的exe文件路径
            base_path = os.path.dirname(sys.executable)
        else:
            # 脚本文件路径
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        file_path = os.path.join(base_path, filename)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            messagebox.showerror("错误", f"找不到文件: {filename}")
            return
            
        # 修改HTML文件
        modify_html_file(file_path)
        
        # Windows 7兼容的打开方式
        if platform.release() == '7':
            os.startfile(file_path)
        else:
            webbrowser.open(file_path)
        
    except Exception as e:
        messagebox.showerror("错误", f"打开文件时出错: {str(e)}")

def on_lucky():
    open_html_file("Lucky.html")

def on_unlucky():
    open_html_file("UnLucky.html")

def create_gui():
    try:
        root = tk.Tk()
        root.title("选择你的命运 - Windows 7兼容版")
        
        # 设置窗口大小（固定大小）
        root.geometry("600x400")
        
        # 禁用最大化按钮
        root.resizable(False, False)
        
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
            height=3,
            activebackground='darkgreen'
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
            height=3,
            activebackground='darkred'
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
        
    except Exception as e:
        messagebox.showerror("初始化错误", f"创建界面时出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # 检查操作系统是否为Windows
    if platform.system() != 'Windows':
        messagebox.showerror("系统错误", "此程序仅支持Windows系统")
        sys.exit(1)
        
    # Windows 7兼容性设置
    if platform.release() == '7':
        try:
            # 设置兼容模式
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass
    
    try:
        app = create_gui()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("运行时错误", f"程序运行时出错: {str(e)}")
        sys.exit(1)