import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QVBoxLayout, QWidget, QDesktopWidget)
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QFont, QPalette, QColor

class DraggableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drag_start_position = None
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_start_position is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = None
            event.accept()

class LotteryProgram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.idle_timer = QTimer(self)
        self.idle_time = 20000  # 20秒闲置时间
        self.setupIdleTimer()
        
    def initUI(self):
        # 主窗口设置
        self.setWindowTitle('抽奖程序')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Editor标签
        editor_label = QLabel('Editor: <a href="https://github.com/xiaofan669/web-school.card">XiaoFan669</a>')
        editor_label.setOpenExternalLinks(True)
        editor_label.setAlignment(Qt.AlignCenter)
        editor_label.setFont(QFont('Arial', 12))
        layout.addWidget(editor_label)
        
        # 抽奖结果显示标签
        self.result_label = QLabel('准备开始抽奖...')
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(self.result_label)
        
        # 停止按钮
        self.stop_button = QPushButton('停止抽奖')
        self.stop_button.setFont(QFont('Arial', 14))
        self.stop_button.clicked.connect(self.stopLottery)
        layout.addWidget(self.stop_button)
        
        # 抽奖选项
        self.options = ['英译汉20', '英译汉30', '汉译英20', '汉译英30', '听音选词40', '听音选词50']
        self.current_index = 0
        self.is_rolling = False
        
        # 抽奖定时器
        self.roll_timer = QTimer(self)
        self.roll_timer.timeout.connect(self.rollOption)
        
        # 窗口居中
        self.centerWindow()
        
        # 开始抽奖
        self.startLottery()
        
    def centerWindow(self):
        # 窗口居中 - 兼容Windows 7的写法
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
        
    def startLottery(self):
        self.is_rolling = True
        self.roll_timer.start(50)  # 50ms切换一次
        
    def rollOption(self):
        self.current_index = (self.current_index + 1) % len(self.options)
        self.result_label.setText(self.options[self.current_index])
        
    def stopLottery(self):
        if self.is_rolling:
            self.roll_timer.stop()
            self.is_rolling = False
            selected_option = self.options[self.current_index]
            self.showResult(selected_option)
            
    def showResult(self, result):
        # 创建全屏结果窗口 - 兼容Windows 7的写法
        self.result_window = QMainWindow()
        self.result_window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.result_window.setWindowOpacity(0.5)
        
        # 设置全屏
        screen = QApplication.desktop().screenGeometry()
        self.result_window.setGeometry(screen)
        
        # 添加结果标签
        result_label = QLabel(result, self.result_window)
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setFont(QFont('Arial', 48, QFont.Bold))
        result_label.setGeometry(QRect(0, 0, screen.width(), screen.height()))
        
        # 显示窗口
        self.result_window.show()
        
        # 2秒后关闭结果窗口
        QTimer.singleShot(2000, self.result_window.close)
        
        # 重置闲置计时器
        self.resetIdleTimer()
        
    def setupIdleTimer(self):
        self.idle_timer.timeout.connect(self.handleIdleTimeout)
        self.resetIdleTimer()
        
    def resetIdleTimer(self):
        self.idle_timer.stop()
        self.idle_timer.start(self.idle_time)
        
    def handleIdleTimeout(self):
        # 闲置超时处理：最小化窗口并显示浮动窗口
        self.showMinimized()
        self.showFloatingWindow()
        
    def showFloatingWindow(self):
        # 创建浮动窗口 - 兼容Windows 7的写法
        self.floating_window = DraggableWindow()
        self.floating_window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        
        # 设置窗口大小
        window_width = 100
        window_height = 100
        self.floating_window.setFixedSize(window_width, window_height)
        
        # 计算初始位置（右侧居中）
        screen = QApplication.desktop().screenGeometry()
        initial_x = screen.width() - window_width
        initial_y = (screen.height() - window_height) // 2
        self.floating_window.move(initial_x, initial_y)
        
        # 添加点击区域
        click_label = QLabel('<a href="#" style="text-decoration:none; color:black; font-size:48px;">转</a>')
        click_label.setAlignment(Qt.AlignCenter)
        click_label.setOpenExternalLinks(False)
        click_label.linkActivated.connect(self.restoreMainWindow)
        
        # 设置透明背景
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255, 180))
        self.floating_window.setPalette(palette)
        self.floating_window.setAutoFillBackground(True)
        
        # 设置布局
        central_widget = QWidget()
        self.floating_window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(click_label)
        
        # 显示浮动窗口
        self.floating_window.show()
        
    def restoreMainWindow(self):
        # 关闭浮动窗口并恢复主窗口
        if hasattr(self, 'floating_window'):
            self.floating_window.close()
            del self.floating_window
            
        self.showNormal()
        self.activateWindow()
        self.startLottery()
        self.resetIdleTimer()
        
    def changeEvent(self, event):
        # 窗口状态变化事件
        if event.type() == event.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                self.idle_timer.stop()
                QTimer.singleShot(1000, self.showFloatingWindow)
                
    def mouseMoveEvent(self, event):
        # 重置闲置计时器
        self.resetIdleTimer()
        
    def keyPressEvent(self, event):
        # 重置闲置计时器
        self.resetIdleTimer()
        
    def closeEvent(self, event):
        # 关闭所有窗口
        if hasattr(self, 'result_window'):
            self.result_window.close()
        if hasattr(self, 'floating_window'):
            self.floating_window.close()
        event.accept()

if __name__ == '__main__':
    # Windows 系统兼容性设置
    if sys.platform == 'win32':
        import ctypes
        try:
            # 尝试Windows 8.1+的API
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError):
            try:
                # 回退到Windows Vista/7的API
                ctypes.windll.user32.SetProcessDPIAware()
            except (AttributeError, OSError):
                pass  # 如果都不支持，就忽略
    
    app = QApplication(sys.argv)
    # 设置Windows 7兼容的样式
    app.setStyle('Fusion')
    lottery = LotteryProgram()
    lottery.show()
    sys.exit(app.exec_())