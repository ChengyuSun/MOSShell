"""MoshiWindow — 可拓展的原生桌面壳窗口。

QMainWindow 骨架 + QWebEngineView 主区域，带启动加载态：
Reflex 等本地服务启动慢于窗口，启动期间展示 loading 画面，
后台轮询检测目标 URL 可用后自动切到页面。
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QProgressBar, QStackedWidget,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QTimer, Qt
from PySide6.QtGui import QColor
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class _LoadingOverlay(QWidget):
    """深色加载画面：居中文字 + 不确定进度条。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#0f0f1a"))
        self.setPalette(p)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

        self._label = QLabel("MOSHI 正在启动...")
        self._label.setStyleSheet(
            "color: #a0a0c0; font-size: 18px; font-family: sans-serif;"
        )
        layout.addWidget(self._label, alignment=Qt.AlignmentFlag.AlignCenter)

        self._bar = QProgressBar()
        self._bar.setRange(0, 0)
        self._bar.setFixedWidth(300)
        self._bar.setFixedHeight(4)
        self._bar.setTextVisible(False)
        self._bar.setStyleSheet(
            "QProgressBar { background: #1a1a2e; border: none; border-radius: 2px; }"
            "QProgressBar::chunk { background: #6c6cff; border-radius: 2px; }"
        )
        layout.addWidget(self._bar, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

    def set_message(self, text: str) -> None:
        self._label.setText(text)


class MoshiWindow(QMainWindow):
    """可拓展的桌面壳窗口，内嵌 Chromium webview，带启动加载检测。"""

    def __init__(
        self,
        url: str = "http://localhost:3000",
        title: str = "MOSHI",
        width: int = 1280,
        height: int = 800,
        check_interval_ms: int = 1000,
    ):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(width, height)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._loading = _LoadingOverlay()
        self.webview = QWebEngineView()
        self.webview.page().setBackgroundColor(QColor("#0f0f1a"))

        self._stack = QStackedWidget()
        self._stack.addWidget(self._loading)
        self._stack.addWidget(self.webview)
        layout.addWidget(self._stack)

        self._target_url = url
        self._checking = False
        self._network = QNetworkAccessManager()
        self._network.finished.connect(self._on_check_response)

        self._check_timer = QTimer()
        self._check_timer.setInterval(check_interval_ms)
        self._check_timer.timeout.connect(self._check_server)

        self._stack.setCurrentIndex(0)
        self._check_timer.start()

    # ---- 健康检查 ----

    def _check_server(self) -> None:
        if self._checking:
            return
        self._checking = True
        req = QNetworkRequest(QUrl(self._target_url))
        self._network.head(req)

    def _on_check_response(self, reply: QNetworkReply) -> None:
        self._checking = False
        if reply.error() == QNetworkReply.NetworkError.NoError:
            self._check_timer.stop()
            self.webview.setUrl(QUrl(self._target_url))
            self._stack.setCurrentIndex(1)
        reply.deleteLater()

    # ---- public ----

    def load_url(self, url: str) -> None:
        self._target_url = url
        self._checking = False
        self._stack.setCurrentIndex(0)
        self._loading.set_message(f"正在连接 {url}...")
        self._check_timer.start()

    def eval_js(self, code: str) -> None:
        self.webview.page().runJavaScript(code)
