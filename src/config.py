from datetime import datetime

dataPath = "../data/"
pickedDayStr = "20160606"
fileName = dataPath + "{}.csv".format(pickedDayStr)
datetimeFormat = "%Y%m%d%H:%M:%S"


startTime = datetime.strptime(pickedDayStr + "10:00:00", datetimeFormat)
endTime = datetime.strptime(pickedDayStr + "14:00:00", datetimeFormat)

countStartTime = datetime.strptime(pickedDayStr + "11:00:00", datetimeFormat)
countEndTime = datetime.strptime(pickedDayStr + "13:00:00", datetimeFormat)
