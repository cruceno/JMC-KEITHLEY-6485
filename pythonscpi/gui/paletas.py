from PySide2.QtGui import QPalette, QBrush, QColor
from PySide2.QtCore import Qt


colors = [(QPalette.Active, QPalette.WindowText, Qt.white),
    # (QPalette.Active, QPalette.Button, QColor(0, 0, 0, 255)),
    # (QPalette.Light, QColor(0, 0, 0, 255)),
    # (QPalette.Active, QPalette.Midlight, QColor(0, 0, 0, 255)),
    # (QPalette.Active, QPalette.Dark, QColor(0, 0, 0, 255)),
    # (QPalette.Active, QPalette.Mid, QColor(0, 0, 0, 255)),
    (QPalette.Active, QPalette.Text, Qt.white),
    # (QPalette.Active, QPalette.BrightText, QColor(0, 0, 0, 255)),
    # (QPalette.Active, QPalette.ButtonText, QColor(0, 0, 0, 255)),
    # (QPalette.Active, QPalette.Base, QColor(0, 0, 0, 255)),
    (QPalette.Active, QPalette.Window, Qt.black),
    # (QPalette.Active, QPalette.Shadow, QColor(0, 0, 0, 255)),
    # (QPalette.Active, QPalette.ToolTipBase, QColor(0, 0, 0, 255)),
    # (QPalette.Active, QPalette.ToolTipText QColor(0, 0, 0, 255)),

    (QPalette.Inactive, QPalette.WindowText, Qt.white),
    # (QPalette.Inactive, QPalette.Button, QColor(0, 0, 0, 255)),
    # (QPalette.Light, QColor(0, 0, 0, 255)),
    # (QPalette.Inactive, QPalette.Midlight, QColor(0, 0, 0, 255)),
    # (QPalette.Inactive, QPalette.Dark, QColor(0, 0, 0, 255)),
    # (QPalette.Inactive, QPalette.Mid, QColor(0, 0, 0, 255)),
    (QPalette.Inactive, QPalette.Text, Qt.white),
    # (QPalette.Inactive, QPalette.BrightText, QColor(0, 0, 0, 255)),
    # (QPalette.Inactive, QPalette.ButtonText, QColor(0, 0, 0, 255)),
    # (QPalette.Inactive, QPalette.Base, QColor(0, 0, 0, 255)),
    (QPalette.Inactive, QPalette.Window, Qt.black),
    # (QPalette.Inactive, QPalette.Shadow, QColor(0, 0, 0, 255)),
    # (QPalette.Inactive, QPalette.ToolTipBase, QColor(0, 0, 0, 255)),
    # (QPalette.Inactive, QPalette.ToolTipText QColor(0, 0, 0, 255)),

    (QPalette.Disabled, QPalette.WindowText, Qt.white),
    # (QPalette.Disabled, QPalette.Button, QColor(0, 0, 0, 255)),
    # (QPalette.Light, QColor(0, 0, 0, 255)),
    # (QPalette.Disabled, QPalette.Midlight, QColor(0, 0, 0, 255)),
    # (QPalette.Disabled, QPalette.Dark, QColor(0, 0, 0, 255)),
    # (QPalette.Disabled, QPalette.Mid, QColor(0, 0, 0, 255)),
    (QPalette.Disabled, QPalette.Text, Qt.white),
    # (QPalette.Disabled, QPalette.BrightText, QColor(0, 0, 0, 255)),
    # (QPalette.Disabled, QPalette.ButtonText, QColor(0, 0, 0, 255)),
    # (QPalette.Disabled, QPalette.Base, QColor(0, 0, 0, 255)),
    (QPalette.Disabled, QPalette.Window, Qt.black),
    # (QPalette.Disabled, QPalette.Shadow, QColor(0, 0, 0, 255)),
    # (QPalette.Disabled, QPalette.ToolTipBase, QColor(0, 0, 0, 255)),
    # (QPalette.Disabled, QPalette.ToolTipText QColor(0, 0, 0, 255)),
]

groups = [QPalette.Active, QPalette.Disabled, QPalette.Inactive]

def get_colored_pallete(colors, palette=QPalette()):
    for group, role, color in colors:
        brush = QBrush(color)
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(group, role, brush)
    return palette

