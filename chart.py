import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import numpy as np
import pylab
import sys
import json


class Chart:
    def __init__(self, store):
        self.store = store

    def showQuality(self):

        trucks_fleet = 0
        trucks_used = 0
        total_distance = 0
        whole_distance = 0

        quality = []

        for algo, solution in self.store.solutions.items():
            trucks_fleet = int(solution['trucks_fleet'])
            total_distance = int(solution['total_distance'])

            for truck in solution["vehicles"]:
                if(len(truck["route"]) > 1):
                    trucks_used += 1
            whole_distance = 0
            indexX = 0
            indexY = 0
            for i in self.store.data["distance_matrix"]:
                for j in i:
                    if indexX > indexY:
                        whole_distance += j
                    indexX += 1
                indexX = 0
                indexY += 1

            quality.append((total_distance / whole_distance)
                           * (trucks_used / trucks_fleet))
            trucks_used = 0

        fig = plt.figure()
        x = [1, 2, 3]
        width = 0.5

        plt.bar(x, quality, width, color=(0.65098041296005249,
                                          0.80784314870834351, 0.89019608497619629, 1.0))

        plt.xlim(0, 4)
        plt.ylim(0, sorted(quality, reverse=True)[
            0] + sorted(quality, reverse=True)[0] * 0.1)

        plt.title('Quality Diagram')

        pylab.xticks(x, self.store.solutions.keys(), rotation=20)

        # plt.savefig('SimpleBar.png')
        plt.show()

    def showComplexity(self):

        color = ['r','b','g']
        i = 0
        
        for algorithm, values in self.store.complexity.items():
            x = []
            y = []
            for point in values:
                x.append(point['cities'])
                y.append(point['duration'])
            curve = plt.plot(x, y, color[i], algorithm)
            x.clear()
            y.clear()
            i += 1

        pylab.legend(loc='upper left')
        plt.show()

