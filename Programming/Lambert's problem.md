# Решение задачи Ламберта

Данный код реализует решение задачи Ламберта для миссии межпланетного перелета с Земли на Венеру.
Импортируются необходимые модули и классы из библиотек astropy, poliastro и matplotlib.
Задаются временные параметры отправления и прибытия для миссии.
Генерируются промежутки времени от даты отправления до даты прибытия с помощью функции time_range.
Определяются орбиты Земли и Венеры на заданные моменты времени с использованием класса Ephem.
Создаются орбиты для момента отправления с Земли и прибытия к Венере с помощью класса Orbit.
Реализуется функция lambert_solution_orbits, которая вычисляет все возможные орбиты решения задачи Ламберта.
Создается график с помощью класса StaticOrbitPlotter и отображаются орбиты Земли и Венеры.
Отображаются решения задачи Ламберта для каждого сценария с помощью функции plot_maneuver.
В результате получается график с различными траекториями для миссии межпланетного перелета с Земли на Венеру.


```python
from astropy import units as u  # Импортируем модуль units из библиотеки astropy для работы с физическими единицами
from astropy.time import Time
from poliastro.bodies import Sun, Earth, Venus  # Импортируем планеты Sun, Earth, Venus из библиотеки poliastro.bodies
from poliastro.ephem import Ephem  # Импортируем класс Ephem из библиотеки poliastro.ephem для работы с орбитами
from poliastro.twobody import Orbit  # Импортируем класс Orbit из библиотеки poliastro.twobody для работы с двухтелесными орбитами
from poliastro.util import time_range  # Импортируем функцию time_range из библиотеки poliastro.util для генерации промежутков времени
from itertools import product
from poliastro.maneuver import Maneuver  # Импортируем класс Maneuver из библиотеки poliastro.maneuver для работы с маневрами
from matplotlib import pyplot as plt
from poliastro.plotting import StaticOrbitPlotter  # Импортируем класс StaticOrbitPlotter из библиотеки poliastro.plotting для визуализации орбит

# Задаем временные параметры отправления и прибытия для миссии
EPOCH_DPT = Time("2031-05-22", scale="tdb")  # Задаем дату отправления в формате строки и указываем шкалу времени "tdb"
EPOCH_ARR = EPOCH_DPT + 2 * u.year  # Задаем дату прибытия

epochs = time_range(EPOCH_DPT, end=EPOCH_ARR)  # Генерируем промежутки времени от даты отправления до даты прибытия

# Определяем орбиты Земли и Венеры на заданные моменты времени
earth = Ephem.from_body(Earth, epochs=epochs)  # Создаем эфемериды для орбиты Земли
venus = Ephem.from_body(Venus, epochs=epochs)  # Создаем эфемериды для орбиты Венеры

# Создаем орбиты для момента отправления с Земли и прибытия к Венере
earth_departure = Orbit.from_ephem(Sun, earth, EPOCH_DPT)  # Создаем орбиту для момента отправления с Земли
venus_arrival = Orbit.from_ephem(Sun, venus, EPOCH_ARR)  # Создаем орбиту для момента прибытия к Венере

# Генерируем все возможные комбинации типа движения и пути
type_of_motion_and_path = list(product([True, False], repeat=2))

# Проградные орбиты отображаются синим цветом, а ретроградные орбиты - красным
colors_and_styles = [
    color + style for color in ["r", "b"] for style in ["-", "--"]
]

def lambert_solution_orbits(ss_departure, ss_arrival, M):
    """Вычисляет все возможные орбиты решения задачи Ламберта."""
    for (is_prograde, is_lowpath) in type_of_motion_and_path:
        if (is_prograde != is_lowpath):
            continue
        ss_sol = Maneuver.lambert(
            ss_departure,
            ss_arrival,
            M=M,
            prograde=is_prograde,
            lowpath=is_lowpath,
        )
        yield ss_sol

# Создаем сетку 1x1 для графиков
fig, axs = plt.subplots(1, 1, figsize=(8, 8))
a = [1]
for i in a:
    ith_case = 2
    M = 2
    # Отображаем орбиты Земли и Венеры
    op = StaticOrbitPlotter(ax=axs)
    axs.set_title("Mission Trajectory")

    op.plot_body_orbit(Earth, EPOCH_DPT - 0.193 * u.year)
    op.plot_body_orbit(Venus, EPOCH_ARR)

    # Отображаем решения задачи Ламберта для данного сценария
    for ss, colorstyle in zip(
            lambert_solution_orbits(earth_departure, venus_arrival, M=M),
            colors_and_styles,
    ):
        ss_plot_traj = op.plot_maneuver(
            earth_departure, ss, color=colorstyle[0]
        )
plt.show()
```
### Ниже приведена траектория полета
![](https://github.com/zmskvxd/Pictures/blob/main/trajectory.jpg)

Исходный код [тут](https://github.com/zmskvxd/Kerbal-Project/blob/main/Programming/Lambert's%20problem.py)
