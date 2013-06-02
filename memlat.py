#!/usr/bin/env python

import mmap
import random
import ctypes
import timeit
import optparse

# global constants
KB = 1024

def alloc_buf(size):
   return mmap.mmap(-1, size)

def permute_buf(begin, size, linesize=64):
   addr = ctypes.addressof(begin)
   cache_lines = range(addr, addr + size, linesize)
   random.shuffle(cache_lines)
   # setup pointers according to random shuffle
   for off in range(0, size, linesize):
       index = off/linesize
       pindex = off/ctypes.sizeof(ctypes.c_void_p)
       void_p = ctypes.pointer(begin)
       void_p[pindex] =  cache_lines[index]

def measure():
    simple.run(begin, options.num)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-s', '--size', help='size of the buffer in KB',
                      type=int, default=64*1024)
    parser.add_option('-n', '--num', help='number of iterations',
                      type=int, default=int(1e7))
    (options, args) = parser.parse_args()

    buf = alloc_buf(options.size * KB)
    begin = ctypes.c_void_p.from_buffer(buf)
    permute_buf(begin, options.size * KB)
    simple = ctypes.CDLL("./simple.so")
    best = min(timeit.repeat("from __main__ import measure; measure();",
                            repeat=3,
                            number=1))
    print "Memory latency: ",  best * 1e9/options.num, " ns"
