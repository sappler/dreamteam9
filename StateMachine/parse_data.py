import time
import datetime
import socket
import matplotlib.pyplot as plt
import numpy as np

class Sleeper:
    def __init__(self, duration, config_file):
        self.duration = int(duration)
        self.time_start = datetime.datetime.now()
        self.config_file = config_file

        f = open(config_file, "r")
        self.name = f.readline()
        self.wakeup_span = int(f.readline())    # float val of num minutes to perform the wakeup cycle
        self.predictive_max = f.readline()      # earliest wakeup where a state transition will be permitted
        self.num_divisions = int(f.readline())  # how many steps to break wakeup into, bounded [1, 100] on Windows and [1, 1000] on Unix due to clock limits (for now)
        self.port = int(f.readline())           # port for local communication to send control signals
        self.use_data = f.readline()            # whether or not to use predictive wakeup feature
        self.data_file = f.readline()           # (optional) dataset for predictive optimal wakeup
        f.close()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', self.port))

        # plt.xlabel("HRV")
        # plt.ylabel("Time (s)")
        # plt.show()

    def graph_baseline(self):
        self.x = []
        y = []
        
        fd = open(self.data_file, "r")
        dataset =  fd.readlines()
        fd.close()
        for line in dataset:
            split_tupple = line.split(',')
            self.x.append(split_tupple[0])
            y.append(float(split_tupple[1]))
            
        # plt.plot(x, y, color = 'blue', linestyle = 'solid', linewidth = 2)
                # marker = 'o', markerfacecolor = 'blue', markersize = 5)
        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.x, y, color = 'blue', linestyle = 'solid', linewidth = 1)
        self.ax.set_xticks(self.ax.get_xticks()[::35])
        plt.gcf().autofmt_xdate()
        plt.xlabel('Time')
        plt.ylabel('HRV')
        plt.title('Dynamic HRV Graph (Debug)')
        plt.ion()
        plt.show()

    def send_com(self, msg):
        n_sent = 0
        n_max = len(msg)
        while n_sent < n_max:
            status = self.sock.send(msg[n_sent:])
            if status == 0:
                print("Socket dropped")
                self.sock.shutdown()
                return None
            n_sent = n_sent + status

    def accept(self, point):                    # add a new HR point to the active / running dataset
        return
    
    def simple(self):                           # simple wakeup with no real-time predictive analysis
        print("Sleep ", str(60*(self.duration - self.wakeup_span)))
        #time.sleep(60*(self.duration - self.wakeup_span))
        print(datetime.datetime.now())

        # n_hrv_per_interval = int(len(self.x) / self.duration)
        # it = int(0)
        
        for zz in range(self.num_divisions):
            self.send_com(str(datetime.datetime.now()).encode())   # send time for debug purposes, normally send a float on [0, 1] representing intensity
            time.sleep(1/self.num_divisions)
        self.send_com("WAKEUP".encode())

        y2 = []
        it = int(0);
        start = len(self.x) - int(float(float(self.wakeup_span) / float(self.duration)) * len(self.x))
        print("Start", start)
        for k in range(len(self.x)):
            if k < start:
                print('set 0')
                y2.append(0)
            else:
                print('set val')
                y2.append(it / self.num_divisions)
                it = it + 1
        self.ax2 = self.ax.twinx()
        self.ax2.plot(self.x, y2, color = 'red', linestyle = 'dashed', linewidth = 1)
        self.ax2.set_ylabel('Light Intensity')
        self.ax2.set_xticks([])
        # self.ax2.ylim(0, 1)
        # plt.figure(figsize = (13.3, 10))
        plt.rcParams['figure.figsize'] = [13.3, 10]
        plt.show()
        
    def manage(self):                           # manage control signals from the ECG feeding to the State Machine while asleep
        while(True):
            print("Hi")
if __name__ == '__main__':
    S1 = Sleeper(100, "sleep_config.txt")
    S1.graph_baseline()
    S1.simple()
    # S1.manage()