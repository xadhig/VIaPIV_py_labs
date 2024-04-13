import numpy as np
import re

flag_sit = 0; 

with open('./../lab1.lib', 'r', encoding='utf-8') as infile:
  for line in infile:
    # print(line)

    # обработка флагов
    if (flag_sit):
      # строка обрабатывается
      sit = line; 
      # флаг сбрасывается
      flag_sit = 0; 
    
    # выставление флагов
    if (re.match('string_input_transtion', line)):
    # if (line == 'string_input_transtion \n'):
      flag_sit = 1;             


# исходная строка
print("Исходная строка: " + sit + "\n")

# строка, сразу разбитая по элементам
print("Сразу разбитая по элементам строка: " + str(sit.split(",")) + "\n")

# replace & split
print("Разбитая по элементам строка с предварительной заменой: " + str(sit.replace("\n", "").split(",")) + "\n")
sit = sit.replace("\n", "").split(",")

sit_np = np.array(sit, dtype='float')

sit_lc = [float(x) for x in sit]

for i in range(0, len(sit)):
  sit[i] = float(sit[i])


print("Данные во float через цикл: " + str(sit) + "\n")
print("Данные во float через numpy: " + str(sit_np) + "\n")
print("Данные во float через list comprehension: " + str(sit_lc) + "\n")

# Проверим эквивалентность этих результатов

print(sit == sit_lc)
print(sit == sit_np)