"""MoshiWindow — 可拓展的原生桌面壳窗口。

QMainWindow 骨架 + QWebEngineView 主区域。
未来加 toolbar/sidebar/statusbar 往 layout 里插即可。
"""

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


class MoshiWindow(QMainWindow):
    """可拓展的桌面壳窗口，内嵌 Chromium webview。"""

    def __init__(
        self,
        url: str = "http://localhost:3000",
        title: str = "MOSHI",
        width: int = 1280,
        height: int = 800,
    ):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(width, height)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl(url))
        layout.addWidget(self.webview)

    def load_url(self, url: str) -> None:
        """切换 webview 到指定 URL。"""
        self.webview.setUrl(QUrl(url))

    def eval_js(self, code: str) -> None:
        """在 webview 中执行 JavaScript。"""
        self.webview.page().runJavaScript(code)
