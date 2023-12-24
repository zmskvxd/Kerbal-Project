# Анализ логирования данных

Данный код загружает лог-файл с данными о скорости, высоте и времени полета космического аппарата. И представляет данные в виде графика.
```python
import matplotlib.pyplot as plt
import numpy as np
def shorter(a):
    a = str(a)
    i = a.index('.')
    return a[0:i + 5]


a = open('логи ксп.txt')
speed = []
height = []
time_1 = []
for i in a.readlines():
    i = list(map(shorter, i.split()))
    speed.append(float(i[0]))
    height.append(float(i[1]))
    time_1.append(float(i[2]))


new_time = []
new_height = []
start = time_1[0]
for i in range(0, len(time_1)):
    a = time_1[i] - start
    if a <= 162:
        new_time.append(time_1[i] - start)
        new_height.append(height[i])

print(new_time)
plt.plot(new_time, new_height, color='black')
plt.title('График зависимости высоты от времени')
plt.ylabel("Высота")
plt.xlabel("Время")
plt.xticks(np.arange(0, 180, 20))
plt.yticks(np.arange(0, 100000, 10000))
plt.grid()
plt.show()
```
### Ниже приведен график
![image](https://github.com/zmskvxd/Kerbal-Project/assets/154624315/8c019f6d-f8fd-45ed-9557-33ebcf924016)

Исходный код [тут](https://github.com/zmskvxd/Kerbal-Project/blob/main/Programming/Analyzing%20logging.py)
