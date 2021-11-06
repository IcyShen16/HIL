from Model import simuLoss, simuQueue
import numpy as np
from DataPreprocessing import fitSystem
from Roles import CUSTOMERS, FLEET, DRIVERS
from copy import deepcopy
from utils import localPlot
import config as conf

def tsFleetSize(SysType, DP):
    # SysType: LS or QS, LS means loss system while QS means queueing system
    # DP: FD or NN, FD means first dispatch while NN means Nearest Neighbor
    if SysType == "LS":
        SysSimu = globals()["simuLoss"]
        measurePer = "SL"
        FleetSizeVector = list(range(100, 2000, 100))
        tmp = list(range(2000, 3000, 200))
        FleetSizeVector = np.array([*FleetSizeVector, *tmp])
    elif SysType == "QS":
        SysSimu = globals()["simuQueue"]
        measurePer = "EW"
        FleetSizeVector = list(range(1000, 2000, 300))
        tmp = list(range(2000, 3000, 200))
        FleetSizeVector = [*FleetSizeVector, *tmp]
        tmp = list(range(3000, 4000, 100))
        FleetSizeVector = np.array([*FleetSizeVector, *tmp])
    else:
        raise Exception("\n error @ tsFleetSize: wrong SysType={} \n".format(SysType))

    Results = np.zeros(len(FleetSizeVector))
    df_cus, vehicleInitData, driverInitData = fitSystem(0, 0)
    oriCustomers = CUSTOMERS(df_cus, SysType)
    for index, m in enumerate(FleetSizeVector):
        customers = deepcopy(oriCustomers)
        df_cus, vehicleInitData, driverInitData = fitSystem(m, m)
        fleet = FLEET(vehicleInitData)
        drivers = DRIVERS(driverInitData)
        Results[index] = SysSimu(customers, drivers, fleet, DP)
        print("\n m={}, n={}, {}={}".format(m, m, measurePer, Results[index]))
    xlim = [min(FleetSizeVector) - 10, max(FleetSizeVector) + 10]
    ylim = [max(Results.min() - 0.1, 0), Results.max()+0.1]
    filePath = conf.dataPath + "tsFleetSize_{}_{}.png".format(SysType, DP)
    localPlot(FleetSizeVector.reshape(1, -1), Results.reshape(1, -1), "m", "service level", "{}-fleet size".format(SysType), None, xlim, ylim, True, filePath)


def hilNumDrivers(fleetSize, SysType, DP):

    if SysType == "LS":
        SysSimu = globals()["simuLoss"]
        measurePer = "SL"
    elif SysType == "QS":
        SysSimu = globals()["simuQueue"]
        measurePer = "EW"
    else:
        raise Exception("\n error @ tsFleetSize: wrong SysType={} \n".format(SysType))
    numDriversVector = np.array(range(1, fleetSize+1))
    Results = np.zeros(len(numDriversVector))

    df_cus, vehicleInitData, driverInitData = fitSystem(fleetSize, fleetSize)
    oriCustomers = CUSTOMERS(df_cus, SysType)
    for index, n in enumerate(numDriversVector):
        customers = deepcopy(oriCustomers)
        df_cus, vehicleInitData, driverInitData = fitSystem(fleetSize, n)
        fleet = FLEET(vehicleInitData)
        drivers = DRIVERS(driverInitData)
        Results[index] = SysSimu(customers, drivers, fleet, DP)
        print("\n m={}, n={}, {}={}".format(fleetSize, n, measurePer, Results[index]))
    filePath = conf.dataPath + "hilNumDrivers_{}_{}.png".format(SysType, DP)
    xlim = [min(numDriversVector)-10, max(numDriversVector)+10]
    ylim = [max(Results.min() -0.1, 0), Results.max()+0.1]
    localPlot(numDriversVector.reshape(1, -1), Results.reshape(1, -1), "n", measurePer, "{}-fleet size".format(SysType), None, xlim, ylim, True, filePath)
