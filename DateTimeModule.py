import datetime
import time

def main():
    dir(datetime)
    print(datetime.date.today())
    print(datetime.datetime.now())
    print(datetime.datetime.now().time())
    print(datetime.datetime.now().date())
    print(datetime.datetime.now().year)
    print(datetime.datetime.now().month)
    print(datetime.datetime.now().day)
    print(datetime.datetime.now().hour)
    print(datetime.datetime.now().minute)

    gvr = datetime.date(1956, 1, 31)
    print(gvr)
    millenium = datetime.date(2000, 1, 1)
    dt = datetime.timedelta(days=8888)
    print(millenium + dt)
    print(millenium)

    message = "Today is the 8888th day of the millenium {:%A, %B %d, %Y}".format(millenium + dt)
    print(message)


    launch_date = datetime.date(2017, 3, 30)
    launch_time = datetime.time(22, 27, 0)
    launch_datetime = datetime.datetime(2017, 3, 30, 22, 27, 0)
    print(launch_date)
    print(launch_time)
    print(launch_datetime)

if __name__ == "__main__":
    main()