#!/usr/bin/env python
# coding: utf-8

import random
from timeit import timeit

def construct_tree(seed):
    result = {}
    for _ in seed:
      temp = result
      for item in _:
          temp = temp.setdefault(item, {})
    return result

target_url = '123455'
seed = ['abcdefg' for i in xrange(5)]
tire_seed = construct_tree(seed)

#O(n*l)
def normal_match(seed, target_url):
    for _ in seed:
       for index, item in enumerate(_):
           if index >= len(target_url):
              break
           if item != target_url[index]:
              break
       else:
           return True
    return False

#O(l)
def tire_match(tire_seed, target_url):
    for _ in target_url:
       if _ in tire_seed:
          tire_seed = tire_seed[_]
          if tire_seed == {}:
             return True
       else:
          return False

normal_t = timeit('normal_match(seed, target_url)', 'from __main__ import normal_match, seed, target_url')
print normal_t
tire_t = timeit('tire_match(tire_seed, target_url)', 'from __main__ import tire_match, tire_seed, target_url')
print tire_t
