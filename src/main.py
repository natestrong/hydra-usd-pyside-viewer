import env_setup

# Setup the environment
env_setup.setup_usd_environment()

import os
import sys
from PySide6 import QtWidgets, QtCore
from pxr import Usd, UsdUtils
from pxr.Usdviewq.stageView import StageView
from timeline import TimelineWidget

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
        self.timeline = TimelineWidget()

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.timeline)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        self.timeline.frameChanged.connect(self.on_frame_changed)
        self.timeline.playbackStarted.connect(self.on_playback_started)
        self.timeline.playbackStopped.connect(self.on_playback_stopped)

        if stage:
            self.setStage(stage)

    def setStage(self, stage):
        self.model.stage = stage
        earliest = Usd.TimeCode.EarliestTime()
        self.model.currentFrame = Usd.TimeCode(earliest)

        if stage.HasAuthoredTimeCodeRange():
            self.timeline.setVisible(True)
            self.timeline.setStartFrame(stage.GetStartTimeCode())
            self.timeline.setEndFrame(stage.GetEndTimeCode())
            self.timeline.framesPerSecond = stage.GetFramesPerSecond()
        else:
            self.timeline.setVisible(False)

    def closeEvent(self, event):
        self.timeline.playing = False
        self.view.closeRenderer()

    def on_frame_changed(self, value, playback):
        self.model.currentFrame = Usd.TimeCode(value)
        if playback:
            self.view.updateForPlayback()
        else:
            self.view.updateView()

    def on_playback_stopped(self):
        self.model.playing = False
        self.view.updateView()

    def on_playback_started(self):
        self.model.playing = True
        self.view.updateForPlayback()

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Space:
            self.timeline.toggle_play()
        elif key == QtCore.Qt.Key_F:
            self.view.updateView(resetCam=True, forceComputeBBox=True)


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
