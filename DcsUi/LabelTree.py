import json
import sys
import os

from pyecharts import options as opts
from pyecharts.charts import Page, Tree
from pyecharts.globals import CurrentConfig
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QFrame
from PyQt5.QtWebEngineWidgets import QWebEngineView


data = [
        {
            "children": [
                {"name": "B"},
                {
                    "children": [
                        {"children": [{"name": "I"}], "name": "E"},
                        {"name": "F"},
                    ],
                    "name": "C",
                },
                {
                    "children": [
                        {"children": [{"name": "J"}, {"name": "K"}], "name": "G"},
                        {"name": "H"},
                    ],
                    "name": "D",
                },
            ],
            "name": "A",
        }
    ]




class LabelTree(QWidget):
    def __init__(self, projectpath):
        super(LabelTree, self).__init__()
        self.path = os.path.join(projectpath, '.userdata', 'Tree.html').replace('\\', '/')
        self.mainLayout()

    def mainLayout(self):
        self.mainhboxLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.mainhboxLayout.addWidget(self.frame)
        self.hboxLayout = QHBoxLayout(self.frame)
        self.myHtml = QWebEngineView()
        self.getTree()
        self.myHtml.load(QUrl("file:///" + self.path))
        
        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)

    def getTree(self):
        tree=(
         Tree().add("", data).set_global_opts(title_opts=opts.TitleOpts(title="Tree-基本示例"))
            )
        tree.js_host = os.path.join(os.path.abspath(''), 'static\\')
        print(tree.js_host)

        tree.render(self.path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LabelTree()
    ex.show()
    sys.exit(app.exec_())
