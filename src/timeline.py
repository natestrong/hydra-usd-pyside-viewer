from PySide6 import QtWidgets, QtCore
import time


class QJumpSlider(QtWidgets.QSlider):
    """QSlider that jumps to exactly where you click on it."""

    def __init__(self, parent=None):
        super(QJumpSlider, self).__init__(parent)

    def mousePressEvent(self, event):
        self.setValue(QtWidgets.QStyle.sliderValueFromPosition(self.minimum(),
                                                               self.maximum(),
                                                               event.x(),
                                                               self.width()))

    def mouseMoveEvent(self, event):
        self.setValue(QtWidgets.QStyle.sliderValueFromPosition(self.minimum(),
                                                               self.maximum(),
                                                               event.x(),
                                                               self.width()))


class TimelineWidget(QtWidgets.QWidget):
    """Timeline widget with playback controls."""

    frameChanged = QtCore.Signal(int, bool)
    playbackStopped = QtCore.Signal()
    playbackStarted = QtCore.Signal()

    def __init__(self, parent=None):
        super(TimelineWidget, self).__init__(parent=parent)

        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        self.slider = QJumpSlider(QtCore.Qt.Horizontal)
        self.slider.setStyleSheet("""
        QSlider::groove:horizontal {
            border: 1px solid #999999;
            background-color: #BBBBBB;
            margin: 0px 0;
        }
        QSlider::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
            border: 1px solid #5c5c5c;
            width: 15px;
            border-radius: 3px;
        }
        """)

        RANGE = 1e6

        self.start = QtWidgets.QSpinBox()
        self.start.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.start.setMinimum(-RANGE)
        self.start.setMaximum(RANGE)
        self.start.setKeyboardTracking(False)

        self.end = QtWidgets.QSpinBox()
        self.end.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.end.setMinimum(-RANGE)
        self.end.setMaximum(RANGE)
        self.end.setKeyboardTracking(False)

        self.frame = QtWidgets.QSpinBox()
        self.frame.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.frame.setMinimum(-RANGE)
        self.frame.setMaximum(RANGE)
        self.frame.setKeyboardTracking(False)

        self.playButton = QtWidgets.QPushButton("Play")

        self.fps = QtWidgets.QSpinBox()
        self.fps.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.fps.setMinimum(1)
        self.fps.setMaximum(120)
        self.fps.setValue(24)
        self.fps.setKeyboardTracking(False)
        self.fps.valueChanged.connect(self.update_fps)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        layout.addWidget(self.start)
        layout.addWidget(self.slider)
        layout.addWidget(self.end)
        layout.addWidget(self.frame)
        layout.addWidget(self.playButton)
        layout.addWidget(QtWidgets.QLabel("FPS:"))
        layout.addWidget(self.fps)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._advanceFrameForPlayback)

        self.playButton.clicked.connect(self.toggle_play)
        self.slider.valueChanged.connect(self.frame.setValue)
        self.frame.valueChanged.connect(self._frameChanged)
        self.start.valueChanged.connect(self.slider.setMinimum)
        self.end.valueChanged.connect(self.slider.setMaximum)

        self.framesPerSecond = 24.0
        self._lastFrameTime = time.time()

    def setStartFrame(self, start):
        self.start.setValue(start)

    def setEndFrame(self, end):
        self.end.setValue(end)

    @property
    def playing(self):
        return self._timer.isActive()

    @playing.setter
    def playing(self, state):
        if self.playing == state:
            return

        self.playButton.setText("Stop" if state else "Play")

        if state:
            self._lastFrameTime = time.time()
            self._timer.start(int(1000 / self.framesPerSecond))
            self.playbackStarted.emit()
            self.slider.setFocus()
        else:
            self._timer.stop()
            self.playbackStopped.emit()

    def toggle_play(self):
        self.playing = not self.playing

    def _advanceFrameForPlayback(self):
        time.sleep(max(0, 1. / self.framesPerSecond - (time.time() - self._lastFrameTime)))
        self._lastFrameTime = time.time()

        frame = self.frame.value()
        frame += 1
        if frame >= self.slider.maximum():
            frame = self.slider.minimum()
        self.slider.setValue(frame)

    def _frameChanged(self, frame):
        if self.slider.value() != frame:
            self.slider.blockSignals(True)
            self.slider.setValue(True)
            self.slider.blockSignals(False)

        self.frameChanged.emit(frame, self.playing)

    def update_fps(self, value):
        self.framesPerSecond = value
