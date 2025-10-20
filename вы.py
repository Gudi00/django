# import matplotlib.pyplot as plt
#
# # Данные
# nodes = ['а', 'б', 'в', 'г', 'д', 'е', 'а']  # Узлы с возвращением к 'а'
# potentials = [6.70, 9.31, 23.30, -6.97, 0, 10.52, 6.7]  # Потенциалы в В
# resistances = [0, 2, 4, 6, 8, 10, 16]  # Значения R, Ом (примерное соответствие по оси X)
#
# # Создание графика
# plt.figure(figsize=(10, 6))
# plt.plot(resistances, potentials, '-o', label='Потенциал', color='blue')
#
# # Подписи узлов
# for i, node in enumerate(nodes):
#     plt.annotate(node, (resistances[i], potentials[i]), textcoords="offset points", xytext=(0,10), ha='center')
#
# # Настройка осей
# plt.xlabel('R, Ом')
# plt.ylabel('Потенциал, В')
# plt.title('Потенциальная диаграмма')
# plt.grid(True)
# plt.ylim(-15, 25)  # Установим пределы по оси Y, как в образце
#
# # Показать график
# plt.show()


import math


# Ввод данных
e1 = float(input("Введите значение E1 (в В): "))
e3 = float(input("Введите значение E3 (в В): "))

R = []
print("\nВведите значения сопротивлений на резисторах (в кОм):")
for i in range(6):
    R.append(float(input(f"Введите R{i + 1} (в кОм): ")))

print("\nЗначения сопротивлений:")
for i in range(6):
    print(f"R{i + 1} = {R[i]} кОм")

print(f"E1 = {e1} В")
print(f"E3 = {e3} В\n")

# Рассчёт токов для источника E1
print("Токи для источника E1:")

r34 = (R[2] * R[3]) / (R[2] + R[3])
r2346 = R[1] + R[5] + r34
r23456 = (r2346 * R[4]) / (r2346 + R[4])
rvh1 = R[0] + r23456

print(f"R(3,4) = {r34:.4f} кОм")
print(f"R(2,3,4,6) = {r2346:.4f} кОм")
print(f"R(2,3,4,5,6) = {r23456:.4f} кОм")
print(f"R(вх1) = {rvh1:.4f} кОм")

I1_1 = e1 / rvh1
I5_1 = I1_1 * (r2346 / (r2346 + R[4]))
I2_1 = I6_1 = I1_1 - I5_1
I4_1 = I2_1 * (R[2] / (R[2] + R[3]))
I3_1 = I2_1 - I4_1

print(f"I1' = {I1_1:.4f} мА")
print(f"I2' = {I2_1:.4f} мА")
print(f"I3' = {I3_1:.4f} мА")
print(f"I4' = {I4_1:.4f} мА")
print(f"I5' = {I5_1:.4f} мА")
print(f"I6' = {I6_1:.4f} мА")

# Рассчёт токов для источника E3
print("\nТоки для источника E3:")

r15 = (R[0] * R[4]) / (R[0] + R[4])
r1256 = R[1] + R[5] + r15
r12456 = (r1256 * R[3]) / (r1256 + R[3])
rvh2 = R[2] + r12456

print(f"R(1,5) = {r15:.4f} кОм")
print(f"R(1,2,5,6) = {r1256:.4f} кОм")
print(f"R(1,2,4,5,6) = {r12456:.4f} кОм")
print(f"R(вх2) = {rvh2:.4f} кОм")

I3_2 = e3 / rvh2
I4_2 = I3_2 * (r1256 / (r1256 + R[3]))
I2_2 = I6_2 = I3_2 - I4_2
I1_2 = I2_2 * (R[4] / (R[0] + R[4]))
I5_2 = I2_2 - I1_2

print(f"I1'' = {I1_2:.4f} мА")
print(f"I2'' = {I2_2:.4f} мА")
print(f"I3'' = {I3_2:.4f} мА")
print(f"I4'' = {I4_2:.4f} мА")
print(f"I5'' = {I5_2:.4f} мА")
print(f"I6'' = {I6_2:.4f} мА")

# Рассчёт токов по методу наложения
print("\nТоки по методу наложения:")

I1 = I1_1 - I1_2
I2 = I2_1 - I2_2
I3 = -I3_1 + I3_2
I4 = I4_1 + I4_2
I5 = I5_1 + I5_2
I6 = I6_1 - I6_2

print(f"I1 = {I1:.4f} мА")
print(f"I2 = {I2:.4f} мА")
print(f"I3 = {I3:.4f} мА")
print(f"I4 = {I4:.4f} мА")
print(f"I5 = {I5:.4f} мА")
print(f"I6 = {I6:.4f} мА")

# Проверка баланса мощностей
print("\nБаланс мощностей:")

P1 = (I1 ** 2) * R[0] + (I2 ** 2) * R[1] + (I3 ** 2) * R[2] + (I4 ** 2) * R[3] + (I5 ** 2) * R[4] + (I6 ** 2) * R[5]
P2 = e1 * I1 + e3 * I3

print(f"P1 = {P1:.4f} мВт")
print(f"P2 = {P2:.4f} мВт")



