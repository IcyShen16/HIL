from Model import simuLoss
import numpy as np
from DataPreprocessing import fitSystem
from Roles import CUSTOMERS, FLEET, DRIVERS
from copy import deepcopy
from utils import localPlot
# (x, y, xlabel, ylabel, title, legends, xlim, ylim, SaveorNot=False, filePath=None):

def tsFleetSize(SysType):
    FleetSizeList = list(range(100, 2000, 100))
    tmp = list(range(2000, 5000, 300))
    FleetSizeList = [*FleetSizeList, *tmp]
    tmp = list(range(5000, 8000, 500))
    FleetSizeList = [*FleetSizeList, *tmp]

    Results = np.zeros(len(FleetSizeList))
    if SysType == "LS":
        SysSimu = globals()["simuLoss"]

    elif SysType == "QS":
        SysSimu = globals()["simuQueue"]
    else:
        raise Exception("\n error @ tsFleetSize: wrong SysType={} \n".format(SysType))
    df_cus, vehicleInitData, driverInitData = fitSystem(0, 0)
    oriCustomers = CUSTOMERS(df_cus, SysType)
    for index, m in enumerate(FleetSizeList):
        customers = deepcopy(oriCustomers)
        df_cus, vehicleInitData, driverInitData = fitSystem(m, m)
        fleet = FLEET(vehicleInitData)
        drivers = DRIVERS(driverInitData)
        Results[index] = simuLoss(customers, drivers, fleet)
        print("\n m={}, n={}, SL={}".format(m, m, Results[index]))
    localPlot(FleetSizeList.reshape(1, -1), Results.reshape(1, -1), "m", "service level", "{}-fleet size".format(SysType), None, [LB, UB], [0, 1])

