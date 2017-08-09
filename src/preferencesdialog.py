from functools import partial

from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets

from ui import resources_rc

class PreferencesDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(PreferencesDialog, self).__init__(parent)
        self.selector = QtWidgets.QListWidget()
        self.selector.setViewMode(QtWidgets.QListView.IconMode)
        self.selector.setIconSize(QtCore.QSize(96, 84))
        self.selector.setMovement(QtWidgets.QListView.Static)
        self.selector.setMaximumWidth(128)
        self.selector.setSpacing(12)

        self.pages = QtWidgets.QStackedWidget()
        self.pages.addWidget(CommonMarkPage())

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.rejected.connect(self.accept)

        self.addSelectorIcon(':/img/img/markdown-208x128-solid.png', 'CommonMark')
        self.selector.setCurrentRow(0)
        self.selector.currentItemChanged.connect(self.changePage)

        #connect(closeButton, &QAbstractButton::clicked, this, &QWidget::close);

        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.addWidget(self.selector)
        horizontalLayout.addWidget(self.pages, 1)

        buttonsLayout = QtWidgets.QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(self.buttonBox)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(buttonsLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr('Preferences'))


    def addSelectorIcon(self, img, text):
        icon = QtWidgets.QListWidgetItem(self.selector)
        icon.setIcon(QtGui.QIcon(img))
        icon.setText(self.tr(text))
        icon.setTextAlignment(Qt.AlignHCenter)
        icon.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def changePage(self, current, previous):
        if not current:
            current = previous
        self.pages.setCurrentIndex(self.selector.row(current))


class CommonMarkPage(QtWidgets.QWidget):
    def __init__(self, parent = None, settings = QtCore.QSettings('CMarkEd', 'CMarkEd')):
        super(CommonMarkPage, self).__init__(parent)
        self.settings = settings
        dialectGroupBox = QtWidgets.QGroupBox(self.tr('CommonMark Dialect'))
        def saveDialect(settings, radio, name):
            if radio.isChecked():
                settings.setValue('CommonMarkDialect', name)
        defaultRadio = QtWidgets.QRadioButton(self.tr('&Standard CommonMark'))
        githubRadio  = QtWidgets.QRadioButton(self.tr('&GitHub Flavored Markdown'))

        self.dialects = (
            (defaultRadio, 'standard'),
            (githubRadio, 'gfm'),
        )
        for radio, name in self.dialects:
            radio.clicked.connect(partial(saveDialect, self.settings, radio, name))

        dialect = settings.value('CommonMarkDialect')
        if dialect:
            for radio, name in self.dialects:
                if name == dialect:
                    radio.setChecked(True)
                    break
        else:
            self.settings.setValue('CommonMarkDialect', 'standard')

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(defaultRadio)
        vbox.addWidget(githubRadio)
        vbox.addStretch(1)
        dialectGroupBox.setLayout(vbox)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(dialectGroupBox)
        layout.addStretch(1)
        self.setLayout(layout)

    def save(self):
        for radio, name in self.dialects:
            if radio.isChecked():
                self.settings.setValue('CommonMarkDialect', name)
                break
