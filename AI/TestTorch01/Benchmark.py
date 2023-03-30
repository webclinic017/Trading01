# https://pytorch.org/tutorials/recipes/recipes/benchmark.html
import torch
import timeit
import torch.utils.benchmark as benchmark

x = torch.randn(10000, 64)


def batched_dot_mul_sum(a, b):
  '''Computes batched dot by multiplying and summing'''
  return a.mul(b).sum(-1)


def batched_dot_bmm(a, b):
  '''Computes batched dot by reducing to bmm'''
  a = a.reshape(-1, 1, a.shape[-1])
  b = b.reshape(-1, b.shape[-1], 1)
  dd =  torch.bmm(a, b).flatten(-3)
  return dd

def f01():
  # Input for benchmarking

  # Ensure that both functions compute the same output
  assert batched_dot_mul_sum(x, x).allclose(batched_dot_bmm(x, x))

  t0 = timeit.Timer(
    stmt='batched_dot_mul_sum(x, x)',
    setup='from __main__ import batched_dot_mul_sum',
    globals={'x': x})

  t1 = timeit.Timer(
    stmt='batched_dot_bmm(x, x)',
    setup='from __main__ import batched_dot_bmm',
    globals={'x': x})

  print(f'mul_sum(x, x):  {t0.timeit(100) / 100 * 1e6:>5.1f} us')
  print(f'bmm(x, x):      {t1.timeit(100) / 100 * 1e6:>5.1f} us')
  j=1

def f02():
  pass
  t0 = benchmark.Timer(
    stmt='batched_dot_mul_sum(x, x)',
    setup='from __main__ import batched_dot_mul_sum',
    globals={'x': x})

  t1 = benchmark.Timer(
    stmt='batched_dot_bmm(x, x)',
    setup='from __main__ import batched_dot_bmm',
    globals={'x': x})

  print(t0.timeit(100))
  print(t1.timeit(100))


if __name__ == '__main__':
  f01()
  f02()
  j=1

  import torch.utils.benchmark as benchmark

  t0 = benchmark.Timer(
      stmt='batched_dot_mul_sum(x, x)',
      setup='from __main__ import batched_dot_mul_sum',
      globals={'x': x})

  t1 = benchmark.Timer(
      stmt='batched_dot_bmm(x, x)',
      setup='from __main__ import batched_dot_bmm',
      globals={'x': x})

  print(t0.timeit(100))
  print(t1.timeit(100))

  num_threads = torch.get_num_threads()
  print(f'Benchmarking on {num_threads} threads')

  t0 = benchmark.Timer(
      stmt='batched_dot_mul_sum(x, x)',
      setup='from __main__ import batched_dot_mul_sum',
      globals={'x': x},
      num_threads=num_threads,
      label='Multithreaded batch dot',
      sub_label='Implemented using mul and sum')

  t1 = benchmark.Timer(
      stmt='batched_dot_bmm(x, x)',
      setup='from __main__ import batched_dot_bmm',
      globals={'x': x},
      num_threads=num_threads,
      label='Multithreaded batch dot',
      sub_label='Implemented using bmm')

  print(t0.timeit(100))
  print(t1.timeit(100))

  x = torch.randn(10000, 1024, device='cuda')

  t0 = timeit.Timer(
      stmt='batched_dot_mul_sum(x, x)',
      setup='from __main__ import batched_dot_mul_sum',
      globals={'x': x})

  t1 = timeit.Timer(
      stmt='batched_dot_bmm(x, x)',
      setup='from __main__ import batched_dot_bmm',
      globals={'x': x})

  # Ran each twice to show difference before/after warmup
  print(f'mul_sum(x, x):  {t0.timeit(100) / 100 * 1e6:>5.1f} us')
  print(f'mul_sum(x, x):  {t0.timeit(100) / 100 * 1e6:>5.1f} us')
  print(f'bmm(x, x):      {t1.timeit(100) / 100 * 1e6:>5.1f} us')
  print(f'bmm(x, x):      {t1.timeit(100) / 100 * 1e6:>5.1f} us')


  num_threads = torch.get_num_threads()
  print(f'Benchmarking on {num_threads} threads')

  t0 = benchmark.Timer(
      stmt='batched_dot_mul_sum(x, x)',
      setup='from __main__ import batched_dot_mul_sum',
      globals={'x': x},
      num_threads=num_threads,
      label='Multithreaded batch dot',
      sub_label='Implemented using mul and sum')

  t1 = benchmark.Timer(
      stmt='batched_dot_bmm(x, x)',
      setup='from __main__ import batched_dot_bmm',
      globals={'x': x},
      num_threads=num_threads,
      label='Multithreaded batch dot',
      sub_label='Implemented using bmm')

  print(t0.timeit(100))
  print(t1.timeit(100))

  x = torch.randn(10000, 1024, device='cuda')

  t0 = timeit.Timer(
      stmt='batched_dot_mul_sum(x, x)',
      setup='from __main__ import batched_dot_mul_sum',
      globals={'x': x})

  t1 = timeit.Timer(
      stmt='batched_dot_bmm(x, x)',
      setup='from __main__ import batched_dot_bmm',
      globals={'x': x})

  # Ran each twice to show difference before/after warmup
  print(f'mul_sum(x, x):  {t0.timeit(100) / 100 * 1e6:>5.1f} us')
  print(f'mul_sum(x, x):  {t0.timeit(100) / 100 * 1e6:>5.1f} us')
  print(f'bmm(x, x):      {t1.timeit(100) / 100 * 1e6:>5.1f} us')
  print(f'bmm(x, x):      {t1.timeit(100) / 100 * 1e6:>5.1f} us')

  t0 = benchmark.Timer(
      stmt='batched_dot_mul_sum(x, x)',
      setup='from __main__ import batched_dot_mul_sum',
      globals={'x': x})

  t1 = benchmark.Timer(
      stmt='batched_dot_bmm(x, x)',
      setup='from __main__ import batched_dot_bmm',
      globals={'x': x})

  # Run only once since benchmark module does warmup for us
  print(t0.timeit(100))
  print(t1.timeit(100))


  m0 = t0.blocked_autorange()
  m1 = t1.blocked_autorange()

  print(m0)
  print(m1)

  print(f"Mean:   {m0.mean * 1e6:6.2f} us")
  print(f"Median: {m0.median * 1e6:6.2f} us")

  from itertools import product

  # Compare takes a list of measurements which we'll save in results.
  results = []

  sizes = [1, 64, 1024, 10000]
  for b, n in product(sizes, sizes):
      # label and sub_label are the rows
      # description is the column
      label = 'Batched dot'
      sub_label = f'[{b}, {n}]'
      x = torch.ones((b, n))
      for num_threads in [1, 4, 16, 32]:
          results.append(benchmark.Timer(
              stmt='batched_dot_mul_sum(x, x)',
              setup='from __main__ import batched_dot_mul_sum',
              globals={'x': x},
              num_threads=num_threads,
              label=label,
              sub_label=sub_label,
              description='mul/sum',
          ).blocked_autorange(min_run_time=1))
          results.append(benchmark.Timer(
              stmt='batched_dot_bmm(x, x)',
              setup='from __main__ import batched_dot_bmm',
              globals={'x': x},
              num_threads=num_threads,
              label=label,
              sub_label=sub_label,
              description='bmm',
          ).blocked_autorange(min_run_time=1))

  compare = benchmark.Compare(results)
  compare.print()
