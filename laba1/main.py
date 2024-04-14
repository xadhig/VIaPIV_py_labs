import numpy as np
import re
from classes import Gate

while (1):
# for i in range(1):
  # gate = "AND"
  # output_cap = 12.7
  # input_transition = 15.1
  # input_edge = "n"

  gate = input("Введите элемент(AND, NAND, NOR, OR, XOR, XNOR, BUF, INV): ")
  output_cap = float(input("Введите выходную нагрузку элемента(fF): "))
  input_transition = float(input("Введите время входного фронта(ps): "))
  input_edge = input("Введите тип входного фронта(posedge(p) или negedge(n)): ")

  gate = Gate(gate, "lab1.lib")

  # gate.get_delay(input_edge, input_transition, output_cap)
  
  del_bilin, del_lin, tran_bilin, tran_lin = gate.get_propagate(input_edge, input_transition, output_cap)

  np.set_printoptions(linewidth=200)

  print("Линейная")
  print("Время выходной задержки: " + str(tran_lin) + " пс")
  print("Время выходного фронта: " + str(del_lin) + " пс")

  print("\nБилинейная")
  print("Время выходной задержки: " + str(tran_bilin) + " пс")
  print("Время выходного фронта: " + str(del_bilin) + " пс")
  # print("Время выходной задержки: " + " ".join(map(str, f_p_tr)) + " пс")
  # print("Время выходного фронта: " + " ".join(map(str, f_p_edge)) + " пс\n")







