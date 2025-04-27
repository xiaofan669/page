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
        # 先初始化计时器
        self.idle_timer = QTimer(self)
        self.auto_stop_timer = QTimer(self)
        self.roll_timer = QTimer(self)
        
        # 然后初始化UI
        self.initUI()
        
        # 最后设置计时器
        self.setupTimers()

    def initUI(self):
        # 主窗口设置
        self.setWindowTitle('抽奖程序')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Editor标签
        editor_label = QLabel('Editor: <a href="https://github.com/xiaofan669/web-school.card">XiaoFan669</a>''<p style="color:purple;">当前版本：v1.2(0428版) <a style="color:red;">请点击下方按钮抽取PK项目，一切交给命运！</p>''<p style="color:green;">若想继续使用且不遮挡屏幕，请点击最小化按钮。最小化后如果还想继续抽奖请点击桌面右侧”转“字。</p>')
        editor_label.setOpenExternalLinks(True)
        editor_label.setAlignment(Qt.AlignCenter)
        editor_label.setFont(QFont('Genshin Impact 233', 12))
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
        self.options = ['英译汉20 (常规)', '英译汉30 (常规)', '汉译英20 (常规)', '汉译英30 (常规)', '听音选词40 (抢答)', '听音选词50 (抢答)','听音选词30 (抢答)','中英速配30秒 (限时)','中英速配60秒 (限时)','中英速配120秒 (限时)','看中拼词10 (常规)','看中拼词20 (常规)']
        self.current_index = 0
        self.is_rolling = False
        
        # 窗口居中
        self.centerWindow()
        
    def centerWindow(self):
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())
        
    def setupTimers(self):
        # 闲置计时器 (改为12秒)
        self.idle_timer.timeout.connect(self.handleIdleTimeout)
        self.idle_timer.start(12000)  # 修改为12000毫秒(12秒)
        
        # 自动停止计时器 (9.5秒)
        self.auto_stop_timer.timeout.connect(self.autoStopLottery)
        
        # 抽奖动画计时器
        self.roll_timer.timeout.connect(self.rollOption)
        
        # 开始抽奖
        self.startLottery()
        
    def startLottery(self):
        self.is_rolling = True
        self.roll_timer.start(50)
        self.auto_stop_timer.start(9500)  # 9.5秒后自动停止
        self.idle_timer.start(12000)  # 重置闲置计时器(改为12秒)
        
    def autoStopLottery(self):
        if self.is_rolling:
            self.stopLottery()
        
    def rollOption(self):
        self.current_index = (self.current_index + 1) % len(self.options)
        self.result_label.setText(self.options[self.current_index])
        
    def stopLottery(self):
        if self.is_rolling:
            self.roll_timer.stop()
            self.auto_stop_timer.stop()
            self.is_rolling = False
            selected_option = self.options[self.current_index]
            self.showResult(selected_option)
            
    def showResult(self, result):
        self.result_window = QMainWindow()
        self.result_window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.result_window.setWindowOpacity(0.75)  # 修改为65%透明度
        
        screen = QApplication.desktop().screenGeometry()
        self.result_window.setGeometry(screen)
        
        result_label = QLabel(result, self.result_window)
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setFont(QFont('Honkai Impact3', 72, QFont.Bold))
        result_label.setGeometry(QRect(0, 0, screen.width(), screen.height()))
        
        self.result_window.show()
        QTimer.singleShot(2000, self.result_window.close)
        self.idle_timer.start(12000)  # 重置闲置计时器(改为12秒)
        
    def handleIdleTimeout(self):
        self.showMinimized()
        self.showFloatingWindow()
        
    def showFloatingWindow(self):
        self.floating_window = DraggableWindow()
        self.floating_window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.floating_window.setWindowOpacity(0.75)  # 修改为65%透明度
        
        window_width = 100
        window_height = 100
        self.floating_window.setFixedSize(window_width, window_height)
        
        screen = QApplication.desktop().screenGeometry()
        initial_x = screen.width() - window_width
        initial_y = (screen.height() - window_height) // 2
        self.floating_window.move(initial_x, initial_y)
        
        click_label = QLabel('<a href="#" style="text-decoration:none; color:black; font-size:48px;">转</a>')
        click_label.setAlignment(Qt.AlignCenter)
        click_label.setOpenExternalLinks(False)
        click_label.linkActivated.connect(self.restoreMainWindow)
        
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255, 180))
        self.floating_window.setPalette(palette)
        self.floating_window.setAutoFillBackground(True)
        
        central_widget = QWidget()
        self.floating_window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(click_label)
        
        self.floating_window.show()
        
    def restoreMainWindow(self):
        if hasattr(self, 'floating_window'):
            self.floating_window.close()
            del self.floating_window
            
        self.showNormal()
        self.activateWindow()
        self.startLottery()
        
    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                self.idle_timer.stop()
                QTimer.singleShot(1000, self.showFloatingWindow)
                
    def mouseMoveEvent(self, event):
        self.idle_timer.start(12000)  # 重置闲置计时器(改为12秒)
        
    def keyPressEvent(self, event):
        self.idle_timer.start(12000)  # 重置闲置计时器(改为12秒)
        
    def closeEvent(self, event):
        if hasattr(self, 'result_window'):
            self.result_window.close()
        if hasattr(self, 'floating_window'):
            self.floating_window.close()
        event.accept()

if __name__ == '__main__':
    if sys.platform == 'win32':
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError):
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except (AttributeError, OSError):
                pass
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    lottery = LotteryProgram()
    lottery.show()
    sys.exit(app.exec_())