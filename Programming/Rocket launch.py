import math
import numpy as np
import matplotlib.pyplot as plt

# Тяга (в Н)
thrust = 730000 * 9

# Диаметр ракеты (в метрах)
midel_diameter = 3.7

# Площадь сечени яракеты
midel_area = math.pi * (midel_diameter / 2) ** 2

# Начальная масса летательного аппарата (полезная нагрузка + конструкция аппарата + топливо) в кг
start_rocket_mass = 433090
G = 6.6743 * 10 ** (-11)
M_E = 5.9726 * (10 ** 24)
R_E = 6378100


def g(height):
    result = ((G * M_E) / ((R_E + height) ** 2))
    return result

def calculate_density(height):
    # Изменение плотности воздуха по мере взлета
    # Используем стандартную атмосферную модель до высоты 11 км

    # Коэффициенты для плотности воздуха
    h0 = 0.0
    rho0 = 1.2  # плотность воздуха на уровне моря в кг/м^3
    dh = 11000.0  # высота, на которой плотность уменьшается на e раз
    e = np.exp(1.0)

    # Расчет плотности воздуха на данной высоте
    if height <= 11000.0:
        rho = rho0 * np.exp(-height / dh)
    else:
        rho = rho0 * np.exp(-h0 / dh) * np.exp(-(height - h0) / dh)
    if height < 11000:
        return rho
    else:
        return 0


def calculate_drag_force(atmosphere_density: float, speed: float, midel_area: float):
    c_x_coef = 0.5 * (
            3.7 / 7.2)  # коэффициент сопротивления для консу с диаметро мракеты Falcon 9 И высотой примерно как головная часть ракеты
    return c_x_coef * (atmosphere_density * (speed ** 2)) / 2 * midel_area


# Начальная скорость полета ракеты
speed = 0

# Начальная высота ракеты
height = 0

# Текущая масса ракеты
current_rocket_mass = start_rocket_mass

# Расход топлива ракеты
fuel_consumption = 140 * 9

# Время полета ракеты
dt = 1
theoretical_time = list(range(0, 162, 1))

# Список высот полет ракеты
theoretical_height = [height]

for time in theoretical_time:
    # Расчет плотности и давления атмосферы
    atmosphere_density = calculate_density(height)

    # Расчет текущей массы ракеты
    current_rocket_mass = start_rocket_mass - fuel_consumption * time

    # Расчет текущей силы лобового сопротивления
    current_drag_force = calculate_drag_force(atmosphere_density, speed, midel_area)
    # Расчет изменения скорости
    dv = (thrust - current_drag_force - current_rocket_mass * g(height)) / current_rocket_mass * dt

    # Расчет новой скорости
    previous_speed = speed
    speed = previous_speed + dv
    # Расчет высоты полета
    height = height + previous_speed * dt
    theoretical_height.append(height)

plt.plot(range(len(theoretical_height)), [height for height in theoretical_height], color="red", label="Math model")
plt.xticks(np.arange(0, 180, 20))
plt.yticks(np.arange(0, 120000, 10000))
plt.grid(True)

plt.legend()
plt.show()
