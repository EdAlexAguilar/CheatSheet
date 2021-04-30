'''
Helper Script to benchmark multiprocessing in python.

Does some slow function (sum of primes), then checks how
multiprocessing.Process compares in timing.

This is just to get an idea of how the scaling behaves.
No averaging over multiple runs is performed.

Author: Edgar Aguilar
Date: 30.04.2021
'''
import time
import math
import multiprocessing as mp

NUM_CORES = mp.cpu_count()
INPUT = int(8e5)


def primality_test(n):
    """Naive Primality test.
     Remember, this should be slow!
    returns True if prime"""
    if not isinstance(n, int):
        raise TypeError("Argument must be Integer!")
    if n<2:
        return False
    if n==2:
        return True
    sqrt = int(math.sqrt(n)+2)
    for k in range(2,sqrt):
        if n%k==0:
            return False
    return True

def prime_sum(n):
    """ Sums primes below integer n
    Sum_{k=0}^{n} primality_test(k)"""
    if not isinstance(n, int):
        raise TypeError("Argument must be Integer!")
    return sum([k for k in range(n) if primality_test(k)])

def main():
    print(f'Starting the benchmark!')

    print(f'\n---NORMAL PROCESSING---')
    start_time = time.time()
    prime_sum(INPUT)
    serial_time = time.time() - start_time
    print(f'Time elapsed: {serial_time:.4f}s')
    print(f'This time will now be used for normalization of parallel processing.')

    print(f'\n---PARALLEL PROCESSING---')
    for n_cores in range(1,NUM_CORES+1):
        processes = []
        start_time = time.time()
        for ii in range(n_cores):
            proc = mp.Process(target=prime_sum, args=(INPUT, ))
            proc.start()
            processes.append(proc)
        for proc in processes:
            proc.join()
        n_core_time = time.time()-start_time
        print(f'Cores: {n_cores}   Time elapsed: {n_core_time:.4f}s'
              f'   Normalized: {n_core_time/serial_time:.3f}')

if __name__ == '__main__':
    main()
