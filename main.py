import threading
import psutil
from gpuinfo import GPUInfo
from numba import njit
from tqdm import tqdm
import random
import time

available_device = GPUInfo.check_empty()
percent, memory = GPUInfo.gpu_usage()
total_memory = psutil.virtual_memory()[0]
cores = psutil.cpu_count()

print('='*13,'CPU','='*13)
print('CPU usage:', psutil.cpu_percent(0))
print('Cpu cores:', cores)
print()
print('='*13,'RAM','='*13)
print('RAM memory % used:', psutil.virtual_memory()[2])
print('RAM memory size:', round(total_memory/1000000000, 2), 'GB')
print()
print('='*13,'GPU','='*13)
print('GPU usage:', percent[0])
print('GPU memory used:', memory[0], 'bytes')
print()

def mem_test(total):
    start_time = time.time()
    total_ = total
    rand_list = []
    try:
        for t in tqdm (range(int(total_)), desc="Filling..."):
            rand_list.append('a')
    except:
        print('Got to', t)
    print('Completed', abs(round(start_time-time.time(), 2)), 'seconds.')

stress_core_status = 0

def stress_core():
    global stress_core_status
    time.sleep(0.1)
    acc = 0
    for i in range(100000):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    stress_core_status += 1

def cpu_test(cores_):
    global stress_core_status
    start_time = time.time()
    stress_core_status = 0
    for t in tqdm (range (cores_), desc="Threading..."):
        t = threading.Thread(target=stress_core)
        t.start()

    while True:
        if stress_core_status != cores_:
            print('Stressing CPU',stress_core_status,'/',cores_,'.  ', end='\r')
            time.sleep(0.25)
            print('Stressing CPU',stress_core_status,'/',cores_,'.. ', end='\r')
            time.sleep(0.25)
            print('Stressing CPU',stress_core_status,'/',cores_,'...', end='\r')
            time.sleep(0.25)
        else:
            print('Completed in', abs(round(start_time-time.time(), 2))-0.1, 'seconds.')
            break

@njit
def gpu_test(nsamples):
    acc = 0
    for n in range(nsamples):
        x = random.random()
        y = random.random()
        if (x ** 2 + y ** 2) < 1.0:
            acc += 1
    return 4.0 * acc / nsamples

print('='*13,'Mem Stress Test','='*13)
mem_test(1073741824)
print()
print('='*13,'CPU Stress Test','='*13)
cpu_test(cores)
print()

gpu_test(1)
print('='*13,'GPU Stress Test','='*13)
print('Running...')
start_time = time.time()
gpu_test(500000000)
print('Completed in', abs(round(start_time-time.time(), 2)), 'seconds.')
print()
longer_ = input('Would you like to run a longer test? (y/N) : ')
if longer_.lower() == 'y':
    print('This may take a while...')
    print()
    print('='*13,'CPU Stress Test Long','='*13)
    for x in range(12):
        cpu_test(cores*5)
        print(x, '/', 12)
    print()

    gpu_test(1)
    print('='*13,'GPU Stress Test Long','='*13)
    print('Running...')
    start_time = time.time()
    gpu_test(500000000000)
    print('Completed in', abs(round(start_time-time.time(), 2)), 'seconds.')
    print()

print('Stress test completed!')
