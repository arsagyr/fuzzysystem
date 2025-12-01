from setups import *
from plots import *

def simulation (temp = 25 , hum = 75, lig = 3000):
    # Создание симуляции
    simulation = ctrl.ControlSystemSimulation(greenhouse_ctrl)

    # Задание конкретных входных значений
    simulation.input['temperature'] = temp
    simulation.input['humidity'] = hum
    simulation.input['light'] = lig

    # Выполнение нечеткого вывода
    simulation.compute()

    # Визуализация агрегированного выходного нечеткого множества
    print(f"Агрегированное выходное нечеткое множество для T={temp}, H={hum}, L={lig}\n")
    action.view(sim=simulation)
    plt.title('Агрегированное нечеткое множество воздействия')
    plt.show()
