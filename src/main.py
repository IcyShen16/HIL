from Comparison import  tsFleetSize, hilNumDrivers, computePerformance
from utils import savenpy, loadnpy
import argparse

def lsCompute(m):
    nVector, ResultVector = computePerformance(m, "LS", "FD")
    print("m={}".format(m))
    print(nVector, ResultVector)
    savenpy([nVector, ResultVector], "LS_FD_m{}.npy".format(m))

def parsepara():
    parser = argparse.ArgumentParser()
    parser.add_argument('--Stype', help='[LS]: Loss System;\n [QS]: Queueing System;\n')
    parser.add_argument('--Dtype', help='[FD]: First Dispatch;\n [NN]: Nesrest Neighbor;\n')
    parser.add_argument('--FleetSize', help='positive integer number\n')
    args = parser.parse_args()
    print(args, type(args))
    if (args.Stype is not None) and (args.Dtype is not None) and (args.FleetSize.isdecimal()):
        FleetSize = int(args.FleetSize)
        SysType = args.Stype
        DP = args.Dtype
        print("System type:{}, Dispatching Policy:{}, number of vehicles:{}".format(SysType, DP, FleetSize))
        return SysType, DP, FleetSize
    else:
        raise Exception("\n error: wrong parameters \n")


def main():
    SysType, DP, FleetSize = parsepara()
    # SysType, DP, FleetSize = "LS", "FD", 2000
    if SysType == "LS":
        if DP == "FD":
            lsCompute(FleetSize)
    # tsFleetSize("LS", "FD")
    # tsFleetSize("QS", "FD")
    # hilNumDrivers(100, "QS", "FD")


if __name__ == "__main__":
    main()