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

        x = [1, 2, 3]
        width = 0.5

        plt.bar(x, quality, width, color=(0.65098041296005249,
                                          0.80784314870834351, 0.89019608497619629, 1.0))

        plt.xlim(0, 4)
        plt.ylim(0, sorted(quality, reverse=True)[0] * 1.1)

        plt.title('Quality Diagram')

        pylab.xticks(x, self.store.solutions.keys(), rotation=20)

        # plt.savefig('SimpleBar.png')
        plt.show()

    def showComplexity(self):

        for algorithm, values in self.store.complexity.items():
            x = []
            y = []
            for point in values:
                x.append(point['cities'])
                y.append(point['duration'])

            plt.plot(x, y, label=algorithm)

        plt.xlabel("Nodes")
        plt.ylabel("Time")
        plt.legend()

        plt.title('Complexity Diagram')
        plt.show()

    def showUniformity(self, config):
        x = []
        y = []
        i = 0

        for stat in config['stats']:
            i += 1
            x.append(i)
            y.append(stat['execution_time'])

        width = 0.5

        plt.bar(x, y, width, color=(0.65098041296005249,
                                    0.80784314870834351, 0.89019608497619629, 1.0))

        plt.xlim(0, len(x) + 1)
        plt.ylim(0, sorted(y, reverse=True)[0] * 1.1)

        plt.title('Uniformity Diagram')
        plt.ylabel("Time")

        average = np.mean(y)
        standard_deviation = np.std(y)
        variance = np.var(y)
        median = np.median(y)
        first_quartile = round(np.percentile(y, 25))
        third_quartile = round(np.percentile(y, 75))


        plt.legend(title="average: " + str(round(average, 2)) + 
                    "\nstandard_deviation: " + str(round(standard_deviation, 2)) +
                    "\nvariance: " + str(round(variance, 2)) + 
                    "\nmedian: " + str(round(median, 2)) +
                    "\nfirst_quartile: " + str(round(first_quartile, 2)) + 
                    "\nthird_quartile: " + str(round(third_quartile, 2)) )

        plt.show()

    def showScatterPlot(self, stat):
        x = []
        y = []
        averageX = []
        averageY = []
        listY = []

        for bundles in stat:
            for bundle in bundles['stats']:
                x.append(bundles['cities'])
                y.append(bundle['execution_time'])
                listY.append(bundle['execution_time'])
            averageX.append(x[-1])
            averageY.append(np.mean(listY))
            listY.clear()

        plt.scatter(x, y)
        plt.plot(averageX, averageY)


        plt.xlabel('Cities')
        plt.ylabel('Time')
        plt.title('Scatter Plot Diagram')

        plt.show()
