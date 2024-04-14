import numpy as np
import re

while (1):
  element = input("Введите элемент(AND, NAND, NOR, OR, XOR, XNOR, BUF, INV): ")
  output_cap = float(input("Введите выходную нагрузку элемента(fF): "))
  input_transition = float(input("Введите время входного фронта(ps): "))
  input_edge = input("Введите тип входного фронта(posedge(p) или negedge(n)): ")

  fl_sit = 0; # string_input_transtion flag
  fl_coc = 0; # column_output_capacitance flag


  fl_element = 0
  current_element = ""
  # fl_and = 0; # AND flag
  # fl_nand = 0; # NAND flag
  # fl_nor = 0; # NOR flag
  # fl_or = 0; # OR flag
  # fl_xor = 0; # XOR flag
  # fl_xnor = 0; # XNOR flag
  # fl_buf = 0; # BUF flag
  # fl_inv = 0; # INV flag


  fl_cap = 0; # camacitance flag

  fl_cell_fall = 0; # cell_fall flag
  fl_cell_rise = 0; # cell_rise flag

  fl_fall_transition = 0; # fall_transition flag
  fl_rise_transition = 0; # rise_transition flag

  sit = ""
  coc = ""

  nand_cap = ""
  cell_fall = list()
  cell_rise = list()
  fall_transition = list()
  rise_transition = list()

  with open('lab1.lib', 'r', encoding='utf-8') as infile:
    for line in infile:
      # print(line)

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
      if (fl_element and current_element == element):
        if (fl_cap):
          nand_cap = line
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
        fl_element = 1
        # print(re.match('AND|NAND', line).group(0))
        current_element = re.match('AND|NAND|NOR|OR|XOR|XNOR|BUF|INV', line).group(0)
      
      
      if (fl_element and re.match('capacitance', line)):
        fl_cap = 1;             
      if (fl_element and re.match('cell_fall', line)):
        fl_cell_fall = 1;             
      if (fl_element and re.match('cell_rise', line)):
        fl_cell_rise = 1;             
      if (fl_element and re.match('fall_transition', line)):
        fl_fall_transition = 1;             
      if (fl_element and re.match('rise_transition', line)):
        fl_rise_transition = 1;             


  sit = sit.replace("\n", "").split(",")
  sit_np = np.array(sit, dtype='float')

  coc = coc.replace("\n", "").split(",")
  coc_np = np.array(coc, dtype='float')


  cell_fall_np = list()
  for i in cell_fall:
    cell_fall_np.append(i.replace("\n", "").split(","))
  cell_fall_np = np.array(cell_fall_np, dtype='float')

  cell_rise_np = list()
  for i in cell_rise:
    cell_rise_np.append(i.replace("\n", "").split(","))
  cell_rise_np = np.array(cell_rise_np, dtype='float')


  fall_transition_np = list()
  for i in fall_transition:
    fall_transition_np.append(i.replace("\n", "").split(","))
  fall_transition_np = np.array(fall_transition_np, dtype='float')

  rise_transition_np = list()
  for i in rise_transition:
    rise_transition_np.append(i.replace("\n", "").split(","))
  rise_transition_np = np.array(rise_transition_np, dtype='float')

  np.set_printoptions(linewidth=200)
  # print("string_input_transtion: " + str(sit_np) + "\n")
  # print("column_output_capacitance: " + str(coc_np) + "\n")
  # print("cell_fall:\n" + str(cell_fall_np) + "\n")
  # print("cell_rise:\n" + str(cell_rise_np) + "\n")
  # print("fall_transition:\n" + str(fall_transition_np) + "\n")
  # print("rise_transition:\n" + str(rise_transition_np) + "\n")

  closest_cap = min(coc_np, key=lambda x:abs(x-output_cap))
  closest_cap_ind, = np.where(coc_np == closest_cap)

  closest_transition = min(sit_np, key=lambda x:abs(x-input_transition))
  closest_transition_ind, = np.where(sit_np == closest_transition)

  if (input_edge == "p" or input_edge == "posedge"):
    output_transition = rise_transition_np[closest_transition_ind, closest_cap_ind]
  else:
    output_transition = fall_transition_np[closest_transition_ind, closest_cap_ind]

  if (input_edge == "p" or input_edge == "posedge"):
    output_edge = cell_rise_np[closest_transition_ind, closest_cap_ind]
  else:
    output_edge = cell_fall_np[closest_transition_ind, closest_cap_ind]
  print("Время выходной задержки: " + " ".join(map(str, output_transition)) + " пс")
  print("Время выходного фронта: " + " ".join(map(str, output_edge)) + " пс\n")
  # output_edge





