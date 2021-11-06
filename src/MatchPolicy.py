from utils import haversine_multipoint_to_vector_distance, haversine_point_to_vector_distance
import numpy as np
from scipy import optimize


_MAX_DISTANCE = 10000


def FD(curCusLocation, curVehiLocation, curDriverID, curVehiID, curCusID):
    # first dispatch
    n = len(curDriverID)
    m = len(curVehiID)
    c = len(curCusID)
    if c <= n:
        # we have more drivers, then it reduced to the NN
        return NNwithOrder(curCusLocation, curVehiLocation, curDriverID, curVehiID, curCusID)
    elif m == 1:
        distance_vector = haversine_point_to_vector_distance(curVehiLocation[0, :], curCusLocation)
        return [curCusID[0]], [curVehiID[0]], distance_vector
    else:
        minNum = min(n, m, c)
        return NNwithOrder(curCusLocation[:minNum, :], curVehiLocation, curDriverID, curVehiID, curCusID[:minNum])


def NNwithOrder(curCusLocation, curVehiLocation, curDriverID, curVehiID, curCusID):
    # when we call this function, we are sure there is less customers compared with the number of drivers (vehicles)
    # and we have free drivers (vehicles)
    n = len(curDriverID)
    m = len(curVehiID)
    c = len(curCusID)
    if m == 1: # one vehicle and one customer
        distance_vector = haversine_point_to_vector_distance(curVehiLocation, curCusLocation)
        return [curCusID[0]], [curVehiID[0]], distance_vector
    elif c == 1: # one customer but more than one vehicle
        distance_vector = haversine_point_to_vector_distance(curCusLocation, curVehiLocation)
        min_dis_index = distance_vector.argmin()
        return [curCusID[0]], [curVehiID[min_dis_index]], [distance_vector.min()]
    else:
        distance_matrix = haversine_multipoint_to_vector_distance(curCusLocation, curVehiLocation)
        minNum = min(n, m, c)
        finalVehicleID = np.zeros(minNum)
        distance = np.zeros(minNum)
        for i in range(minNum):
            index = distance_matrix[i, :].argmin()
            finalVehicleID[i] = curVehiID[index]
            distance[i] = distance_matrix[i, index]
            distance_matrix[:, index] = _MAX_DISTANCE
        return curCusID[:minNum], finalVehicleID, distance


def NN(curCusLocation, curVehiLocation, curDriverID, curVehiID, curCusID):
    # nearest neighbor: in this function, we are sure there is at least one idle driver and one idle vehicle

    n = len(curDriverID)
    m = len(curVehiID)
    c = len(curCusID)

    if m == 1:
        distance_vector = haversine_point_to_vector_distance(curVehiLocation, curCusLocation)
        min_dis_index = distance_vector.argmin()
        return [curCusID[min_dis_index]], [curVehiID[0]], [distance_vector.min()]
    elif c == 1:
        distance_vector = haversine_point_to_vector_distance(curCusLocation, curVehiLocation)
        min_dis_index = distance_vector.argmin()
        return [curCusID[0]], [curVehiID[min_dis_index]], [distance_vector.min()]
    else:
        # compute the distance between all customers and all vehicles
        distance_matrix = haversine_multipoint_to_vector_distance(curCusLocation, curVehiLocation)


        # compute the min distance between customers and vehicles
        Cus_ind, Veh_ind = optimize.linear_sum_assignment(distance_matrix)

        all_possible_distance = distance_matrix[Cus_ind, Veh_ind]

        # if the number of drivers is strictly less than the number of vehicles,
        # then we need to choose the min distance of all possible minimum distance as the final matching
        if n < m:
            candidateIndex = np.argpartition(all_possible_distance, n)[:n] # smallest n distance index
            Cus_ind = Cus_ind[candidateIndex]
            Veh_ind = Veh_ind[candidateIndex]
            all_possible_distance = all_possible_distance[candidateIndex]

        Cus_Ids = curCusID[Cus_ind]
        Veh_IDs = curVehiID[Veh_ind]
        return Cus_Ids, Veh_IDs, all_possible_distance

