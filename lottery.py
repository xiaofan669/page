import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QVBoxLayout, QWidget, QDesktopWidget)
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QRect, QPoint
from PyQt5.QtGui import QFont, QPalette, QColor, QCursor
from PyQt5.Qt import QMouseEvent

class DraggableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drag_start_position = None

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
        self.idle_time = 10000  # 10秒闲置时间
        self.setupIdleTimer()
        
    def initUI(self):
        # 主窗口设置
        self.setWindowTitle('抽奖程序')
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Editor标签
        editor_label = QLabel('Editor: <a href="https://github.com/xiaofan669/web-school.card">XiaoFan669</a>''<p>当前版本：v1.0(0427版)</p>''<p>请在10秒钟内点击“停止抽奖”,不然程序将报错!</p>')
        editor_label.setOpenExternalLinks(True)
        editor_label.setAlignment(Qt.AlignCenter)
        editor_label.setFont(QFont('Genshin Impact 233', 12))
        layout.addWidget(editor_label)
        
        # 抽奖结果显示标签
        self.result_label = QLabel('准备开始抽奖...')
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont('Genshin Impact 233', 24, QFont.Bold))
        layout.addWidget(self.result_label)
        
        # 停止按钮
        self.stop_button = QPushButton('停止抽奖')
        self.stop_button.setFont(QFont('Genshin Impact 233', 14))
        self.stop_button.clicked.connect(self.stopLottery)
        layout.addWidget(self.stop_button)
        
        # 抽奖选项
        self.options = ['英译汉20', '英译汉30', '汉译英20', '汉译英30', '听音选词40', '听音选词50','听音选词30','听音选义20','听音选义30']
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
        # 窗口居中
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
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
        # 创建全屏结果窗口
        self.result_window = QMainWindow()
        self.result_window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.result_window.setWindowOpacity(0.5)
        
        # 设置全屏
        screen_geometry = QApplication.desktop().screenGeometry()
        self.result_window.setGeometry(screen_geometry)
        
        # 添加结果标签
        result_label = QLabel(result, self.result_window)
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setFont(QFont('Genshin Impact 233', 48, QFont.Bold))
        
        # 设置标签大小与窗口相同
        result_label.setGeometry(QRect(0, 0, screen_geometry.width(), screen_geometry.height()))
        
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
        # 创建浮动窗口
        self.floating_window = DraggableWindow()
        self.floating_window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.floating_window.setWindowTitle('浮动窗口')
        
        # 设置窗口大小
        window_width = 100
        window_height = 100
        self.floating_window.setFixedSize(window_width, window_height)
        
        # 计算初始位置（右侧居中）
        screen_geometry = QApplication.desktop().availableGeometry()
        initial_x = screen_geometry.width() - window_width
        initial_y = (screen_geometry.height() - window_height) // 2
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
    app = QApplication(sys.argv)
    lottery = LotteryProgram()
    lottery.show()
    sys.exit(app.exec_())