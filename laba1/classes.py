import numpy as np
import re

class Gate:

  def __init__(self, gate_name, lib_name) -> None:
    self.gate_name = gate_name
    self.open_lib(lib_name)

  def open_lib(self, lib_name):
    fl_sit = 0; # string_input_transtion flag
    fl_coc = 0; # column_output_capacitance flag

    fl_gate = 0

    fl_cap = 0; # camacitance flag

    fl_cell_fall = 0; # cell_fall flag
    fl_cell_rise = 0; # cell_rise flag

    fl_fall_transition = 0; # fall_transition flag
    fl_rise_transition = 0; # rise_transition flag


    sit = ""
    coc = ""

    current_gate = ""

    gate_cap = ""
    cell_fall = list()
    cell_rise = list()
    fall_transition = list()
    rise_transition = list()


    with open(lib_name, 'r', encoding='utf-8') as infile:
      for line in infile:
        # обработка флагов
        if (fl_sit):
          # строка обрабатывается
          sit = line; 
          # флаг сбрасывается
          fl_sit = 0; 
        
        if (fl_coc):
          # строка обрабатывается
          coc = line; 
          # флаг сбрасывается
          fl_coc = 0; 
        
        # Обработка таблиц элемента
        if (fl_gate and current_gate == self.gate_name):
          if (fl_cap):
            gate_cap = line
            fl_cap = 0
          if (fl_cell_fall):
            if (re.match(r'\w+', line)):
              cell_fall.append(line)
            else:
              fl_cell_fall = 0
          if (fl_cell_rise):
            if (re.match(r'\w+', line)):
              cell_rise.append(line)
            else:
              fl_cell_rise = 0

          if (fl_fall_transition):
            if (re.match(r'\w+', line)):
              fall_transition.append(line)
            else:
              fl_fall_transition = 0
          if (fl_rise_transition):
            if (re.match(r'\w+', line)):
              rise_transition.append(line)
            else:
              fl_rise_transition = 0
        
        # выставление флагов
        if (re.match('string_input_transtion', line)):
          fl_sit = 1;             
        if (re.match('column_output_capacitance', line)):
          fl_coc = 1;             
        
        if (re.match('AND|NAND|NOR|OR|XOR|XNOR|BUF|INV', line)):
          fl_gate = 1
          # print(re.match('AND|NAND', line).group(0))
          current_gate = re.match('AND|NAND|NOR|OR|XOR|XNOR|BUF|INV', line).group(0)
        
        
        if (fl_gate and re.match('capacitance', line)):
          fl_cap = 1;             
        if (fl_gate and re.match('cell_fall', line)):
          fl_cell_fall = 1;             
        if (fl_gate and re.match('cell_rise', line)):
          fl_cell_rise = 1;             
        if (fl_gate and re.match('fall_transition', line)):
          fl_fall_transition = 1;             
        if (fl_gate and re.match('rise_transition', line)):
          fl_rise_transition = 1;        
    
    sit = sit.replace("\n", "").split(",")
    self.input_transition = np.array(sit, dtype='float')
    
    coc = coc.replace("\n", "").split(",")
    self.output_capacitance = np.array(coc, dtype='float')

    self.cell_fall = list()
    for i in cell_fall:
      self.cell_fall.append(i.replace("\n", "").split(","))
    self.cell_fall = np.array(self.cell_fall, dtype='float')

    self.cell_rise = list()
    for i in cell_rise:
      self.cell_rise.append(i.replace("\n", "").split(","))
    self.cell_rise = np.array(self.cell_rise, dtype='float')


    self.fall_transition = list()
    for i in fall_transition:
      self.fall_transition.append(i.replace("\n", "").split(","))
    self.fall_transition = np.array(self.fall_transition, dtype='float')

    self.rise_transition = list()
    for i in rise_transition:
      self.rise_transition.append(i.replace("\n", "").split(","))
    self.rise_transition = np.array(self.rise_transition, dtype='float')

    self.capacitance = float(gate_cap)

  def get_closest(self, tr_in, c_out):
    max_cap = min(filter(lambda x: x > c_out, self.output_capacitance), default=None)
    min_cap = max(filter(lambda x: x < c_out, self.output_capacitance), default=None)

    max_transition = min(filter(lambda x: x > tr_in, self.input_transition), default=None)
    min_transition = max(filter(lambda x: x < tr_in, self.input_transition), default=None)

    min_cap_ind, = np.where(self.output_capacitance == min_cap)
    max_cap_ind, = np.where(self.output_capacitance == max_cap)

    min_transition_ind, = np.where(self.input_transition == min_transition)
    max_transition_ind, = np.where(self.input_transition == max_transition)
    
    min_cap_ind = int(min_cap_ind)
    max_cap_ind = int(max_cap_ind)
    min_transition_ind = int(min_transition_ind)
    max_transition_ind = int(max_transition_ind)

    return min_cap, min_cap_ind, max_cap, max_cap_ind, min_transition, min_transition_ind, max_transition, max_transition_ind


  def get_delay(self, edge, tr_in, c_out):
    min_cap, min_cap_ind, max_cap, max_cap_ind, min_transition, min_transition_ind, max_transition, max_transition_ind = self.get_closest(tr_in, c_out)
    if (edge == "p" or edge == "posedge"):
      ((q11, q21), (q12, q22)) = tuple(map(tuple, self.cell_rise[min_transition_ind:max_transition_ind+1, min_cap_ind:max_cap_ind+1]))
    else:
      ((q11, q21), (q12, q22)) = tuple(map(tuple, self.cell_fall[min_transition_ind:max_transition_ind+1, min_cap_ind:max_cap_ind+1]))

    del_lin1 = (max_cap - c_out)/(max_cap - min_cap)*q11 + (c_out - min_cap)/(max_cap - min_cap)*q21
    del_lin2 = (max_cap - c_out)/(max_cap - min_cap)*q12 + (c_out - min_cap)/(max_cap - min_cap)*q22
    del_bilin = (max_transition - tr_in)/(max_transition - min_transition)*del_lin1 + (tr_in - min_transition)/(max_transition - min_transition)*del_lin2
    return del_bilin, del_lin1

  def get_transition(self, edge, tr_in, c_out):
    min_cap, min_cap_ind, max_cap, max_cap_ind, min_transition, min_transition_ind, max_transition, max_transition_ind = self.get_closest(tr_in, c_out)
    if (edge == "p" or edge == "posedge"):
      ((q11, q21), (q12, q22)) = tuple(map(tuple, self.rise_transition[min_transition_ind:max_transition_ind+1, min_cap_ind:max_cap_ind+1]))
    else:
      ((q11, q21), (q12, q22)) = tuple(map(tuple, self.fall_transition[min_transition_ind:max_transition_ind+1, min_cap_ind:max_cap_ind+1]))

    del_lin1 = (max_cap - c_out)/(max_cap - min_cap)*q11 + (c_out - min_cap)/(max_cap - min_cap)*q21
    del_lin2 = (max_cap - c_out)/(max_cap - min_cap)*q12 + (c_out - min_cap)/(max_cap - min_cap)*q22
    del_bilin = (max_transition - tr_in)/(max_transition - min_transition)*del_lin1 + (tr_in - min_transition)/(max_transition - min_transition)*del_lin2
    return del_bilin, del_lin1
 
  def get_propagate(self, edge, tr_in, c_out):
    del_bilin, del_lin = self.get_delay(edge, tr_in, c_out)
    tran_bilin, tran_lin = self.get_transition(edge, tr_in, c_out)
    return del_bilin, del_lin, tran_bilin, tran_lin