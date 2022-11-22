#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Task 1

import heapq

def heapsort(iterable):
    h = []
    for value in iterable:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for i in range(len(h))]

def get_kth_element(arr: list, k: int):
    return heapsort(arr)[k]


def solution():
    arr = list(map(int, input().split()))
    k = int(input())
    print(get_kth_element(arr, k))

solution()


# In[ ]:


# Task 2

import heapq

def heapsort(iterable):
    h = []
    for value in iterable:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for i in range(len(h))]

def merge_k_sorted(arrs: list) -> list:
    new = []
    for c in arrs:
        new.extend(c)
        
    return heapsort(new)

def solution():
    arrs = read_multiline_input() # эта функция уже написана
    merged = merge_k_sorted(arrs)
    print(' '.join([str(el) for el in merged]))

solution()

