import numpy as np
import matplotlib.pyplot as plt
import pyuff

def main():
    data = readUFF('../P001F_A_201027-210221.uff')
    # plotSignal(data)
    print(type(data)) # list
    

def readUFF(filename):
    uff_file = pyuff.UFF('../P001F_A_201027-210221.uff') # Tidssignaler_t.o.m._210221/
    # uff_types = uff_file.get_set_types()
    # print(uff_types)
    # uff_set1 = uff_file.read_sets(0)
    # print(uff_set1)
    data = uff_file.read_sets()
    return data

def plotSignal(data):
    plt.semilogy(data[4]['x'], np.abs(data[4]['data']))
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [g]')
    # plt.xlim([0,10])
    plt.show()

def kurtosis():
    pass

if __name__ == '__main__':
    main()