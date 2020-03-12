# -*- coding: utf-8 -*-
import datetime, time


class TimeUtil:
    @staticmethod
    def string2time_stamp(str_value):

        try:
            d = datetime.datetime.strptime(str_value, "%Y-%m-%d %H:%M:%S.%f")
            t = d.timetuple()
            time_stamp = int(time.mktime(t))
            time_stamp = float(str(time_stamp) + str("%06d" % d.microsecond)) / 1000000
            return time_stamp
        except ValueError as e:
            print(e)
            d = datetime.datetime.strptime(str_value, "%Y-%m-%d %H:%M:%S")
            t = d.timetuple()
            time_stamp = int(time.mktime(t))
            time_stamp = float(str(time_stamp) + str("%06d" % d.microsecond)) / 1000000
            return time_stamp
