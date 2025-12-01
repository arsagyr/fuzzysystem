from setups import *

def saveplots():
    # Построение графиков функций принадлежности
    temperature.view()
    plt.title('Функции принадлежности температуры')
    plt.savefig("plots/temperature.png")

    humidity.view()
    plt.title('Функции принадлежности влажности')
    plt.savefig("plots/humidity.png")

    light.view()
    plt.title('Функции принадлежности освещенности')
    plt.savefig("plots/light.png")

    action.view()
    plt.title('Функции принадлежности воздействия на климат')
    plt.savefig("plots/action.png")
