from random import randint

li = [randint(-50, 49) for _ in range(50)]
# %timeit find_max(li)


# using builtin max()
find_max = max
# 672 ns ± 2.45 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

# using for with double check first element
def find_max(some_list):
     max = some_list[0]
     for item in some_list:
         if max < item:
             max = item
     return max
# 1.33 µs ± 6.94 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)


# using for with slice
def find_max(some_list):
     max = some_list[0]
     for item in some_list[1:]:
         if max < item:
             max = item
     return max
# 1.52 µs ± 17.1 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)


# using sorting
def find_max_(some_list):
     local_list = some_list.copy()
     local_list.sort()
     return local_list[-1]
# 1.53 µs ± 11.2 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
