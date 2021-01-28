import random
import networkx as nx
import sys
import time
import multiprocessing
import threading

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
matplotlib.use('Qt5Agg')
plt.style.use('ggplot')

from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon


class CyberAgent():
    def __init__(self):
        self.score = 0
    
    def act(self, gameState):
        pass

    def viewGame(self, gameState):
        pass

class CyberAttacker(CyberAgent):
    def __init__(self):
        super().__init__()

class CyberDefender(CyberAgent):
    def __init__(self):
        super().__init__()

class HumanDefender(CyberDefender):
    class Canvas(FigureCanvas):
        def __init__(self, parent=None, width=5, height=4, dpi=300):
            fig = Figure(figsize=(width, height), dpi=dpi, facecolor="#f0f0f0")
            self.fig = fig
            self.axes = fig.add_subplot(111)
            FigureCanvas.__init__(self, fig)
            self.setParent(parent)

            FigureCanvas.setSizePolicy(self,
                                    QtWidgets.QSizePolicy.Expanding,
                                    QtWidgets.QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)

    class DefWindow(QtWidgets.QMainWindow):
        def __init__(self, parent, recvQueue, sendQueue):
            super().__init__()
            self.recvQueue = recvQueue
            self.sendQueue = sendQueue

            QtWidgets.QMainWindow.__init__(self)
            self.parent = parent
            self.setAttribute(Qt.WA_DeleteOnClose)
            self.setWindowTitle("HumanCyberDefender")
            self.main_widget = QtWidgets.QWidget(self)
            self.main_widget.setFocus()
            self.setCentralWidget(self.main_widget)
            self.grid = QtWidgets.QGridLayout(self.main_widget)
            
            # Top : graph
            self.graphWidget = HumanDefender.Canvas(self.main_widget)
            self.grid.addWidget(self.graphWidget, 0, 0, 1, 2)


            # Bottom left : state and node information
            self.infoWidget = QtWidgets.QGridLayout(self.main_widget)
            self.grid.addLayout(self.infoWidget, 1, 0)
            self.scoreLabel = QtWidgets.QLabel()
            self.scoreLabel.setText("Score : [loading]")
            self.infoWidget.addWidget(self.scoreLabel, 1, 0)
            self.nodeLabel = QtWidgets.QLabel()
            self.nodeLabel.setText("Selected node : [loading]")
            self.infoWidget.addWidget(self.nodeLabel, 2, 0)

            # Bottom right : choices
            self.choiceWidget = QtWidgets.QGridLayout(self.main_widget)
            self.grid.addLayout(self.choiceWidget, 1, 1)
            self.testButton = QtWidgets.QPushButton('test')
            self.choiceWidget.addWidget(self.testButton, 1, 0)

            self.thread = threading.Thread(target=self.eventLoop)
            self.thread.start()

        def eventLoop(self):
            while True:
                ax = self.recvQueue.get() # blocks
                self.graphWidget.axes.clear()
                #self.graphWidget.axes = ax
                self.graphWidget.axes.plot([1, 2, 3, 4])
                self.graphWidget.draw()
                self.graphWidget.flush_events()

    
    def __init__(self):
        super().__init__()
        self.sendQueue = multiprocessing.Queue()
        self.recvQueue = multiprocessing.Queue()
        self.process = multiprocessing.Process(target=self.showWindow, args=(self.sendQueue,self.recvQueue, ))
        self.process.start()

    def __del__(self):
        self.process.join()

        
    def showWindow(self, sendQueue, recvQueue):
        qApp = QtWidgets.QApplication(sys.argv)
        self.aw = HumanDefender.DefWindow(self, sendQueue, recvQueue)
        self.aw.setWindowTitle("CyberDefender")
        #aw.setWindowIcon(QIcon(scriptDir + os.path.sep + '..' + os.path.sep + 'img' + os.path.sep + 'LOGO6.png'))
        self.aw.show()
        sys.exit(qApp.exec_())

        


    def act(self, gameState):
        self.showState(gameState)

    
    def showState(self, state):
        graph = nx.Graph()
        for node in state.nodes:
            graph.add_node(node)
        for link in state.links:
            graph.add_edge(link[0], link[1])

        fig = plt.figure()
        ax = fig.add_subplot()
        nx.draw(graph, font_weight='bold', ax=ax)
        self.sendQueue.put(ax)
        action = self.recvQueue.get()
        return action

class HumanAttacker(CyberAttacker):
    def act(self, gameState):
        print("The current game state is :")
        print(gameState)
        print("Choose a node to attack :")
        print("Choose an attack vector :")

    def showState(self, state):
        print(vars(state))
        
class RandomAttacker(CyberAttacker):
    def act(self, gameState):
        target = random.randint(0, len(gameState.nodes)-1)
        if len(gameState.nodes[target].atqVectors)-1 < 0 :
            raise RuntimeError("This should never happen. The bug was fixed... !")
        vector = random.randint(0, len(gameState.nodes[target].atqVectors)-1)
        return gameState.attack(gameState.nodes[target], vector)

class RandomDefender(CyberDefender):
    def act(self, gameState):
        calls = {0: self.changeDefense, 1: self.changeDetection, 2: self.insertNode, 3: self.removeNode, 4: self.insertLink, 5: self.removeLink, 6: self.endTurn}
        action = random.randint(0, len(calls.keys())-1)
        return calls[action](gameState)

    def changeDefense(self, gameState):
        target = random.randint(0, len(gameState.nodes)-1)
        vector = random.randint(0, len(gameState.nodes[target].defense)-1)
        value = random.random() * 100
        return gameState.changeDefense(gameState.nodes[target], vector, value)

    def changeDetection(self, gameState):
        target = random.randint(0, len(gameState.nodes)-1)
        value = random.random() * 100
        return gameState.changeDetection(gameState.nodes[target], value)

    def insertNode(self, gameState):
        while True:
            left = random.randint(0, len(gameState.nodes)-1)
            right = random.randint(0, len(gameState.nodes)-1)
            if left != right:
                break
        return gameState.insertNode(gameState.nodes[left], gameState.nodes[right])

    def removeNode(self, gameState):
        target = random.randint(0, len(gameState.nodes)-1)
        return gameState.removeNode(gameState.nodes[target])

    def insertLink(self, gameState):
        while True:
            left = random.randint(0, len(gameState.nodes)-1)
            right = random.randint(0, len(gameState.nodes)-1)
            if left != right:
                break
        return gameState.insertLink(gameState.nodes[left], gameState.nodes[right])

    def removeLink(self, gameState):
        while True:
            left = random.randint(0, len(gameState.nodes)-1)
            right = random.randint(0, len(gameState.nodes)-1)
            if left != right:
                break
        return gameState.removeLink(gameState.nodes[left], gameState.nodes[right])

    def endTurn(self, gameState):
        return gameState.endTurn()