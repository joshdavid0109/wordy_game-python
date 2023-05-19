import sched, time as t
from timer import timer
import threading

import Connector

Font = ("Comic Sans MS", 15, "bold")
FontLetters = ("Courier", 13, "bold")
FontLetterz = ("Helvetica", 12, "bold")

# connector = daConnector("192.168.219.133", 9999)  # should be read sa config
connector = Connector.daConnector("localhost", 9999)  # should be read sa config
connector.connect()

eo = Connector.eo


# s = sched.scheduler(eo.getTimer(24, "r"), time.sleep)


class thread(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID

        # helper function to execute the threads

    def run(self):
        a = False
        while not a:
            time = eo.getTimer(25, "r")
            print(time)
            t.sleep(1)
            time -= 1
            if time < 0:
                a = True


thread1 = thread("timer", 1000)

thread1.run()


print("Exit")

# def print_time():
#     print("From print_time", eo.getTimer(24, "r"))
#
#
# def print_some_times():
#     print(time.time())
#     s.enter(5, 1, print_time, ())
#     s.enter(10, 1, print_time, ())
#     s.run()
#     print(time.time())
#
#
# print_some_times()
