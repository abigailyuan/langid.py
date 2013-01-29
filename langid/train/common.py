"""
Common functions

Marco Lui, January 2013
"""

from itertools import islice
import marshal

class Enumerator(object):
  """
  Enumerator object. Returns a larger number each call. 
  Can be used with defaultdict to enumerate a sequence of items.
  """
  def __init__(self, start=0):
    self.n = start

  def __call__(self):
    retval = self.n
    self.n += 1
    return retval

def chunk(seq, chunksize):
  """
  Break a sequence into chunks not exceeeding a predetermined size
  """
  seq_iter = iter(seq)
  while True:
    chunk = tuple(islice(seq_iter, chunksize))
    if not chunk: break
    yield chunk

def unmarshal_iter(path):
  """
  Open a given path and yield an iterator over items unmarshalled from it.
  """
  with open(path, 'rb') as f:
    while True:
      try:
        yield marshal.load(f)
      except EOFError:
        break

import os, errno
def makedir(path):
  try:
    os.makedirs(path)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise

import csv
def write_weights(path, weights):
  w = dict(weights)
  with open(path, 'w') as f:
    writer = csv.writer(f)
    try:
      key_order = sorted(w, key=w.get, reverse=True)
    except ValueError:
      # Could not order keys by value, value is probably a vector.
      # Order keys alphabetically in this case.
      key_order = sorted(w)

    for k in key_order:
      row = [repr(k)]
      try:
        row.extend(w[k])
      except TypeError:
        row.append(w[k])
      writer.writerow(row)

import numpy
def read_weights(path):
  with open(path) as f:
    reader = csv.reader(f)
    retval = dict()
    for row in reader:
      key = eval(row[0])
      #val = numpy.array( map(float,row[1:]) )
      val = numpy.array( [float(v) if v != 'nan' else 0. for v in row[1:]] )
      retval[key] = val
  return retval
      

from itertools import imap
from contextlib import contextmanager, closing
import multiprocessing as mp

@contextmanager
def MapPool(processes=None, initializer=None, initargs=None, maxtasksperchild=None):
  """
  Contextmanager to express the common pattern of not using multiprocessing if
  only 1 job is allocated (for example for debugging reasons)
  """
  if processes is None:
    processes = mp.cpu_count() + 4

  if processes > 1:
    with closing( mp.Pool(processes, initializer, initargs, maxtasksperchild)) as pool:
      f = lambda fn, chunks: pool.imap_unordered(fn, chunks, chunksize=1)
      yield f
  else:
    if initializer is not None:
      initializer(*initargs)
    f = imap
    yield f

  if processes > 1:
    pool.join()