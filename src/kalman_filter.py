# Phỏng theo thuật toán của anh denyssene
# link : https://github.com/denyssene/SimpleKalmanFilter/blob/master/src/SimpleKalmanFilter.h
import math

class KalmanFilter:
  def __init__(self, mea_e, est_e, q):
    self._err_measure = mea_e
    self._err_estimate = est_e
    self._q = q
    self._current_estimate = 0
    self._last_estimate = 0
    self._kalman_gain = 0
  
  def update_estimate(self, mea):
    self._kalman_gain = self._err_estimate / (self._err_estimate + self._err_measure)
    self._current_estimate = self._last_estimate + \
      self._kalman_gain * (mea - self._last_estimate)
    self._err_estimate = (1.0 - self._kalman_gain) * self._err_estimate \
      + math.fabs(self._last_estimate - self._current_estimate) * self._q
    self._last_estimate = self._current_estimate
    
    return self._current_estimate
  
  def set_measurement_error(self, mea_e):
    self._err_measure = mea_e
  
  def set_estimate_error(self, est_e):
    self._err_estimate = est_e
  
  def set_process_noise(self, q):
    self._q = q
  
  def get_kalman_gain(self):
    return self._kalman_gain
  
  def get_estimate_error(self):
    return self._err_estimate