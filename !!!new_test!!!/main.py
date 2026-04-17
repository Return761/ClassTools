import sys
import os
import time
from PySide6.QtCore import QObject, Slot, Signal, QUrl, QThread
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

# 1. 定义桥梁对象：处理业务逻辑
class Bridge(QObject):
    # 定义一个信号，用于主动向 JS 发送数据
    on_status_update = Signal(str)

    # 使用 @Slot 装饰器，允许 JS 调用此方法
    @Slot(str, result=str)
    def heavy_task(self, name):
        print(f"Python 收到请求: 处理 {name}")
        # 模拟异步耗时操作
        time.sleep(2) 
        return f"来自 Python 的结果：{name} 处理完毕！"

# 2. 模拟后台数据推送的线程
class TimeThread(QThread):
    status_signal = Signal(str)
    def run(self):
        while True:
            t = time.strftime('%H:%M:%S')
            self.status_signal.emit(f"系统实时时间: {t}")
            self.msleep(1000)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 + H5 异步通信演示")
        self.resize(800, 600)

        # 创建浏览器组件
        self.browser = QWebEngineView()
        
        # --- 核心通信设置 ---
        self.channel = QWebChannel()
        self.bridge = Bridge()
        # 将 Python 对象注册到 Channel 中，JS 端将通过 "pyObj" 访问
        self.channel.registerObject("pyObj", self.bridge)
        self.browser.page().setWebChannel(self.channel)
        
        # 加载本地 HTML
        curr_path = os.path.dirname(__file__)
        html_path = os.path.join(curr_path, "web", "index.html")
        self.browser.setUrl(QUrl.fromLocalFile(html_path))
        
        self.setCentralWidget(self.browser)

        # 启动后台时间推送
        self.timer_thread = TimeThread()
        self.timer_thread.status_signal.connect(self.bridge.on_status_update.emit)
        self.timer_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())