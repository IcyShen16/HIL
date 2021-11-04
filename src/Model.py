import config as conf



def simuLoss(customers, drivers, fleet, matchPolicy):
    # simulate the loss system with some matching policy (FD, NN)
    for t in range(conf.totalTime):
        pass

    SL = customers.computeMeasure("LS")
    return SL


def simuQueue(customers, drivers, fleet, matchPolicy):
    # simulate the queueing system with some matching policy (FD, NN)
    for t in range(conf.totalTime):
        pass

    EW = customers.computeMeasure("QS")
    return EW


if __name__ == "__main__":
    from DataPreprocessing import fitSystem
    from Roles import CUSTOMERS, FLEET, DRIVERS


    m = 10
    n = 10
    df_cus, vehicleInitData, driverInitData = fitSystem(m, n)
    customers = CUSTOMERS(df_cus)
    fleet = FLEET(vehicleInitData)
    drivers = DRIVERS(driverInitData)
    matchPolicy = "FD"
    SL = simuLoss(customers, drivers, fleet, matchPolicy)
