import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from pxr import Usd, UsdImagingGL


class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.stage = None
        self.renderer = UsdImagingGL.Engine()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        self.stage = Usd.Stage.Open('/path/to/your.usda')  # Update with the path to your USD file

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.stage:
            self.renderer.Render(self.stage)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("USD Hydra Viewer")
        self.glWidget = GLWidget(self)
        self.setCentralWidget(self.glWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
