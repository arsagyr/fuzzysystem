import numpy as np
import skfuzzy  
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. Определение лингвистических переменных 
# Диапазоны (универсум дискурса)
temp_range = np.arange(0, 51, 1)
humid_range = np.arange(0, 101, 1)
light_range = np.arange(0, 10001, 1)
action_range = np.arange(-100, 101, 1)

# Входные переменные
temperature = ctrl.Antecedent(temp_range, 'temperature')
humidity = ctrl.Antecedent(humid_range, 'humidity')
light = ctrl.Antecedent(light_range, 'light')

# Выходная переменная
action = ctrl.Consequent(action_range, 'action')

# Определение функций принадлежности (трапециевидные и треугольные)

# Температура: Низкая (0-15), Оптимальная (10-30), Высокая (25-50)
temperature['temperature_PS'] = skfuzzy.trimf(temp_range, [0, 0, 15])
temperature['temperature_PM'] = skfuzzy.trimf(temp_range, [10, 20, 30])
temperature['temperature_PB'] = skfuzzy.trimf(temp_range, [25, 50, 50])

# Влажность: Сухая (0-40), Нормальная (30-70), Влажная (60-100)
humidity['humidity_PS'] = skfuzzy.trimf(humid_range, [0, 0, 40])
humidity['humidity_PM'] = skfuzzy.trimf(humid_range, [30, 50, 70])
humidity['humidity_PB'] = skfuzzy.trimf(humid_range, [60, 100, 100])

# Освещенность: Темно (0-1000), Светло (500-5000), Очень_светло (4000-10000)
light['light_PS'] = skfuzzy.trimf(light_range, [0, 0, 1000])
light['light_PM'] = skfuzzy.trimf(light_range, [500, 3000, 5000])
light['light_PB'] = skfuzzy.trimf(light_range, [4000, 10000, 10000])

# Воздействие: Сильно_охладить (-100...-50), Охладить (-60...-10), Не_менять (-20...20), Обогреть (10...60), Сильно_обогреть (50...100)
action['heat_NB'] = skfuzzy.trimf(action_range, [-100, -100, -50])
action['heat_NM'] = skfuzzy.trimf(action_range, [-60, -35, -10])
action['heat_Z'] = skfuzzy.trimf(action_range, [-20, 0, 20])
action['heat_PM'] = skfuzzy.trimf(action_range, [10, 35, 60])
action['heat_PB'] = skfuzzy.trimf(action_range, [50, 100, 100])

from setups import *

# 2. Определение базы знаний 

rule1 = ctrl.Rule(temperature['temperature_PS'] & humidity['humidity_PS'] & light['light_PS'], action['heat_PB'])
rule2 = ctrl.Rule(temperature['temperature_PS'] & humidity['humidity_PS'] & light['light_PM'], action['heat_PM'])
rule3 = ctrl.Rule(temperature['temperature_PS'] & humidity['humidity_PM'] & light['light_PS'], action['heat_PM'])
rule4 = ctrl.Rule(temperature['temperature_PS'] & humidity['humidity_PM'] & light['light_PM'], action['heat_Z'])
rule5 = ctrl.Rule(temperature['temperature_PS'] & humidity['humidity_PB'] & light['light_PS'], action['heat_PM'])
rule6 = ctrl.Rule(temperature['temperature_PS'] & humidity['humidity_PB'] & light['light_PM'], action['heat_Z'])
rule7 = ctrl.Rule(temperature['temperature_PM'] & humidity['humidity_PS'] & light['light_PS'], action['heat_Z'])
rule8 = ctrl.Rule(temperature['temperature_PM'] & humidity['humidity_PS'] & light['light_PM'], action['heat_NM'])
rule9 = ctrl.Rule(temperature['temperature_PM'] & humidity['humidity_PM'] & light['light_PS'], action['heat_Z'])
rule10 = ctrl.Rule(temperature['temperature_PM'] & humidity['humidity_PM'] & light['light_PM'], action['heat_Z'])
rule11 = ctrl.Rule(temperature['temperature_PM'] & humidity['humidity_PB'] & light['light_PS'], action['heat_Z'])
rule12 = ctrl.Rule(temperature['temperature_PM'] & humidity['humidity_PB'] & light['light_PM'], action['heat_NM'])
rule13 = ctrl.Rule(temperature['temperature_PB'] & humidity['humidity_PS'] & light['light_PS'], action['heat_NM'])
rule14 = ctrl.Rule(temperature['temperature_PB'] & humidity['humidity_PS'] & light['light_PM'], action['heat_NB'])
rule15 = ctrl.Rule(temperature['temperature_PB'] & humidity['humidity_PM'] & light['light_PS'], action['heat_NM'])
rule16 = ctrl.Rule(temperature['temperature_PB'] & humidity['humidity_PM'] & light['light_PM'], action['heat_NB'])
rule17 = ctrl.Rule(temperature['temperature_PB'] & humidity['humidity_PB'] & light['light_PS'], action['heat_NB'])
rule18 = ctrl.Rule(temperature['temperature_PB'] & humidity['humidity_PB'] & light['light_PM'], action['heat_NB'])
rule19 = ctrl.Rule(temperature['temperature_PB'] & humidity['humidity_PS'] & light['light_PB'], action['heat_NB'])
rule20 = ctrl.Rule(temperature['temperature_PB'] & humidity['humidity_PM'] & light['light_PB'], action['heat_NB'])
rule21 = ctrl.Rule(temperature['temperature_PB'] & humidity['humidity_PB'] & light['light_PB'], action['heat_NB'])

rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21]
# Система управления
greenhouse_ctrl = ctrl.ControlSystem(rules)


