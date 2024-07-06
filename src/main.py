import env_setup

# Setup the environment
env_setup.setup_usd_environment(verbose=True)

import os
import sys
from PySide6 import QtWidgets, QtCore
from pxr import Usd, UsdGeom, UsdUtils
from pxr.Usdviewq.stageView import StageView

# Constants
USD_FILE = "robot_walk_idle.usdz"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USD_FILE_PATH = os.path.join(SCRIPT_DIR, '..', USD_FILE)


# Define the main widget and application
class Widget(QtWidgets.QWidget):
    def __init__(self, stage=None):
        super(Widget, self).__init__()
        self.model = StageView.DefaultDataModel()

        self.view = StageView(dataModel=self.model)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)

        if stage:
            self.setStage(stage)

    def setStage(self, stage):
        self.model.stage = stage

    def closeEvent(self, event):
        # Ensure to close the renderer to avoid GlfPostPendingGLErrors
        self.view.closeRenderer()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Load USD file
    with Usd.StageCacheContext(UsdUtils.StageCache.Get()):
        stage = Usd.Stage.Open(USD_FILE_PATH)

    window = Widget(stage)
    window.setWindowTitle("USD Viewer")
    window.resize(QtCore.QSize(750, 750))
    window.show()

    # Make camera fit the loaded geometry
    window.view.updateView(resetCam=True, forceComputeBBox=True)

    sys.exit(app.exec())
