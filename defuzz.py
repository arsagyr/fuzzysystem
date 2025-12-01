from setups import *
# Функции для различных методов дефаззификации
def centroid_defuzzification(output_mf, action_range):
    """Дефаззификация методом центра тяжести"""
    return skfuzzy.defuzz(action_range, output_mf, 'centroid')

def bisector_defuzzification(output_mf, action_range):
    """Дефаззификация методом центра площади"""
    return skfuzzy.defuzz(action_range, output_mf, 'bisector')

def mom_defuzzification(output_mf, action_range):
    """Дефаззификация методом среднего максимума"""
    return skfuzzy.defuzz(action_range, output_mf, 'mom')

def som_defuzzification(output_mf, action_range):
    """Дефаззификация методом наименьшего максимума"""
    return skfuzzy.defuzz(action_range, output_mf, 'som')

def lom_defuzzification(output_mf, action_range):
    """Дефаззификация методом наибольшего максимума"""
    return skfuzzy.defuzz(action_range, output_mf, 'lom')

def agregiration():
    # Получаем агрегированную функцию принадлежности для выходной переменной
    output_mf = np.zeros_like(action_range)

    # Агрегируем все правила
    for rule in rules:
        # Вычисляем степень активации для каждого правила
        activation = min(
            skfuzzy.interp_membership(temp_range, temperature['temperature_PB'].mf, 28),
            skfuzzy.interp_membership(humid_range, humidity['humidity_PB'].mf, 75),
            skfuzzy.interp_membership(light_range, light['light_PM'].mf, 3000)
        )
        
        # Применяем импликацию (min)
        rule_mf = np.fmin(activation, action['cool_hard'].mf)
        output_mf = np.fmax(output_mf, rule_mf)

    # Выполняем дефаззификацию различными методами
    centroid_result = centroid_defuzzification(output_mf, action_range)
    bisector_result = bisector_defuzzification(output_mf, action_range)
    mom_result = mom_defuzzification(output_mf, action_range)
    som_result = som_defuzzification(output_mf, action_range)
    lom_result = lom_defuzzification(output_mf, action_range)

    print("\nРезультаты различных методов дефаззификации:")
    print(f"Метод центра тяжести (centroid): {centroid_result:.2f}")
    print(f"Метод центра площади (bisector): {bisector_result:.2f}")
    print(f"Метод среднего максимума (mom): {mom_result:.2f}")
    print(f"Метод наименьшего максимума (som): {som_result:.2f}")
    print(f"Метод наибольшего максимума (lom): {lom_result:.2f}")

    # Визуализация результатов
    plt.figure(figsize=(12, 8))

    # График агрегированной функции принадлежности
    plt.subplot(2, 1, 1)
    plt.plot(action_range, output_mf, 'b', linewidth=1.5, label='Агрегированная функция принадлежности')

    # Отмечаем точки дефаззификации
    plt.axvline(x=centroid_result, color='r', linestyle='--', label=f'Центр тяжести: {centroid_result:.2f}')
    plt.axvline(x=bisector_result, color='g', linestyle='--', label=f'Центр площади: {bisector_result:.2f}')
    plt.axvline(x=mom_result, color='orange', linestyle='--', label=f'Средний максимум: {mom_result:.2f}')
    plt.axvline(x=som_result, color='purple', linestyle='--', label=f'Наименьший максимум: {som_result:.2f}')
    plt.axvline(x=lom_result, color='brown', linestyle='--', label=f'Наибольший максимум: {lom_result:.2f}')

    plt.title('Методы дефаззификации выходной переменной "action"')
    plt.ylabel('Степень принадлежности')
    plt.xlabel('Значение воздействия')
    plt.legend()
    plt.grid(True)

    # График отдельных функций принадлежности для действия
    plt.subplot(2, 1, 2)
    plt.plot(action_range, action['heat_NB'].mf, 'r', linewidth=1.5, label='Сильно охладить')
    plt.plot(action_range, action['heat_NM'].mf, 'orange', linewidth=1.5, label='Охладить')
    plt.plot(action_range, action['heat_Z'].mf, 'g', linewidth=1.5, label='Не менять')
    plt.plot(action_range, action['heat_РМ'].mf, 'blue', linewidth=1.5, label='Обогреть')
    plt.plot(action_range, action['heat_РВ'].mf, 'purple', linewidth=1.5, label='Сильно обогреть')

    plt.title('Функции принадлежности для выходной переменной')
    plt.ylabel('Степень принадлежности')
    plt.xlabel('Значение воздействия')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("plots/agr.png")

# Анализ различных сценариев
def analyze_scenario(temp, humid, light_val, scenario_name):
    greenhouse_sim = ctrl.ControlSystemSimulation(greenhouse_ctrl)
    greenhouse_sim.input['temperature'] = temp
    greenhouse_sim.input['humidity'] = humid
    greenhouse_sim.input['light'] = light_val
    greenhouse_sim.compute()
    
    greenhouse = ctrl.ControlSystemSimulation(greenhouse_ctrl)


    # Получаем агрегированную функцию принадлежности
    output_mf = np.zeros_like(action_range)
    
    # Вычисляем степени принадлежности для входных переменных
    temp_mf_low = skfuzzy.interp_membership(temp_range, temperature['temperature_PS'].mf, temp)
    temp_mf_optimal = skfuzzy.interp_membership(temp_range, temperature['temperature_PM'].mf, temp)
    temp_mf_high = skfuzzy.interp_membership(temp_range, temperature['temperature_PB'].mf, temp)
    
    humid_mf_dry = skfuzzy.interp_membership(humid_range, humidity['humidity_PS'].mf, humid)
    humid_mf_normal = skfuzzy.interp_membership(humid_range, humidity['humidity_PM'].mf, humid)
    humid_mf_wet = skfuzzy.interp_membership(humid_range, humidity['humidity_PB'].mf, humid)
    
    light_mf_dark = skfuzzy.interp_membership(light_range, light['light_PS'].mf, light_val)
    light_mf_bright = skfuzzy.interp_membership(light_range, light['light_PM'].mf, light_val)
    light_mf_very_bright = skfuzzy.interp_membership(light_range, light['light_PB'].mf, light_val)
    
    # Агрегируем правила
    rules_activation = []
    
    # Правила для низкой температуры
    rules_activation.append(min(temp_mf_low, humid_mf_dry, light_mf_dark))
    rules_activation.append(min(temp_mf_low, humid_mf_dry, light_mf_bright))
    rules_activation.append(min(temp_mf_low, humid_mf_normal, light_mf_dark))
    # ... и так для всех правил
    
    # Для простоты используем готовый результат
    simulation = ctrl.ControlSystemSimulation(greenhouse_ctrl)

# Задание конкретных входных значений
    simulation.input['temperature'] = temp
    simulation.input['humidity'] = humid
    simulation.input['light'] = light_val

# Выполнение нечеткого вывода
    simulation.compute()
    result = simulation.output['action'] 
    
    print(f"\n{scenario_name}:")
    print(f"Температура: {temp}°C, Влажность: {humid}%, Освещенность: {light_val} люкс")
    print(f"Результат: {result}")
    
    # Определяем лингвистическое значение
    if result < -50:
        action_desc = "Сильное охлаждение"
    elif result < -10:
        action_desc = "Охлаждение"
    elif result < 20:
        action_desc = "Без изменений"
    elif result < 60:
        action_desc = "Обогрев"
    else:
        action_desc = "Сильный обогрев"
    
    print(f"Действие: {action_desc}")


def examples():
    print("Разбор случаев")
    #x1: Жарко, влажно, светло
    analyze_scenario(40, 85, 7000, "1: Жарко, влажно, светло")

    #2: Холодно, сухо, темно
    analyze_scenario(8, 20, 500, "2: Холодно, сухо, темно")

    #3: Оптимальные условия
    analyze_scenario(22, 55, 3000, "3: Оптимальные условия")

    #4: Жарко, сухо, очень светло
    analyze_scenario(38, 30, 9000, "4: Жарко, сухо, очень светло")