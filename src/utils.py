import numpy as np
import matplotlib.pyplot as plt

_AVG_EARTH_RADIUS_KM = 6371.0088


def haversine_point_to_vector_distance(point, vector):
    point = point.flatten()
    point = np.radians(point)
    vector = np.radians(vector)
    Difference = point - vector
    latpoint = np.cos(point[1])
    latVector = np.cos(vector[:, 1])
    DistanceMatrix = np.square( np.sin(Difference[:, 1]/2) ) + latpoint * latVector * np.square( np.sin( Difference[:, 0]/2 ) )
    DistanceMatrix = 2 * _AVG_EARTH_RADIUS_KM * np.arcsin(np.sqrt(DistanceMatrix))
    return DistanceMatrix

def haversine_multipoint_to_vector_distance(points, vector):
    points = np.radians(points)
    vector = np.radians(vector)

    Difference = [vector - x for x in points] # Nbs * Nvs * 2
    latVector = np.cos(vector[:, 1])
    latPoints = np.cos(points[:, 1])
    DistanceMatrix = [ np.square( np.sin(X[:, 1]/2) ) + latVector*latPoints[i] * np.square( np.sin(X[:, 0]/2) ) for i, X in enumerate(Difference)]
    DistanceMatrix = 2 * _AVG_EARTH_RADIUS_KM * np.arcsin(np.sqrt(DistanceMatrix))# KM
    return DistanceMatrix

def localPlot(x, y, xlabel, ylabel, title, legends, xlim, ylim, SaveorNot=False, filePath=None):
    n = y.shape[0]
    if n > 1:
        for i in range(n):
            plt.plot(x, y[i, :], label=legends[i])
        plt.legend()
    else:
        plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xlim(left=xlim[0], right=xlim[1])
    plt.ylim(bottom=ylim[0], top=ylim[1])
    if SaveorNot:
        plt.savefig(filePath)
    else:
        plt.show()
    plt.close()

