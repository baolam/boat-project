from typing import List
from .MatrixPoint import MatrixPoint, check_point_ctd

def bfs(trace, visited, matrix, i_, j_, f, rows, cols):
  t = []
  for i in MatrixPoint.I:
    for j in MatrixPoint.J:
      ti = i + i_
      tj = j + j_
      if check_point_ctd(ti, tj, rows, cols) and not visited[ti][tj] \
        and matrix[ti][tj] != MatrixPoint.WARNING_VC:
        visited[ti][tj] = True
        t.append([ti, tj])
        if f(ti, tj):
          trace.append([ti, tj])
          return True
  while len(t) > 0:
    z = t.pop(0)
    if bfs(trace, visited, matrix, z[0], z[1], f, rows, cols):
      return True
  return False
  
def bfs_get_x_nearest(matrix : List[List[int]], x : int, i : int, j : int):
  rows, cols = len(matrix), len(matrix[0])
  
  visited = []
  trace = []
  
  for __ in range(rows):
    visited.append([False] * cols)
  
  visited[i][j] = True
  trace.append([i, j])

  def f(ti, tj):
    #global x
    return matrix[ti][tj] == x
  
  if f(i, j):
    return True, trace
    
  st = bfs(trace, visited, matrix, i, j, f, rows, cols)
  return st, trace

def goes_to_home(matrix : List[List[int]], i : int, j : int):
  rows, cols = len(matrix), len(matrix[0])
  
  visited = []
  trace = []
  
  for __ in range(rows):
    visited.append([False] * cols)
  
  visited[i][j] = True
  trace.append([i, j])
  
  def f(ti, tj):
    return ti == 0 and tj == 0
  
  if f(i, j):
    return True, trace
  
  st = bfs(trace, visited, matrix, i, j, f, rows, cols)
  return st, trace