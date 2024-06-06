import utils
from database_processing import execute_car_status




def create_orders_answer():
    """
    Формирует строку-ответ на основе двух JSON и статуса машины из БД
    status == 1: ночь
    status == 2: день
    status == 3: выходной
    """
    car_list = execute_car_status()
    orders_json = utils.request_to_MoySklad_orders()
    stores_json = utils.request_to_MoySklad_stores()
    time_start, time_end = utils.time_interval()
    dict_ID_order_ID_car = {}  # Словарь {ID заказа: ID машины(склада)}
    dict_ID_car_Name = {}  # Словарь {ID машины(склада): Имя}
    car_status = {}  # Словарь {Номер машины: статус}
    for car in car_list:
        car_status[car[0][-2:]] = car[1]
    error_list = ''
    for data in orders_json['rows']:
        try:
            dict_ID_order_ID_car[data['id']] = data['store']['meta']['uuidHref'][-36:]
        except KeyError:
            error_list += f'{data["name"]}\n'
    for i in stores_json['rows']:
        dict_ID_car_Name[i['id']] = i['name']

    dict_output = {}
    for id_store1, name in dict_ID_car_Name.items():
        count = 0
        for id_store2 in dict_ID_order_ID_car.values():
            if id_store1 == id_store2:
                count += 1
        dict_output[name] = count
    night_car = ''
    day_car = ''
    night_count_car = 0
    day_count_car = 0
    for num, status in car_status.items():
        if status == 1:
            counted = dict_output[num]
            if counted < 6:
                night_count_car += 1
                night_car += f'<strong>Машина {num}: {counted} ⬅</strong>\n'
            elif counted >= 6:
                night_count_car += 1
                night_car += f'Машина {num}: {counted}\n'
        elif status == 2:
            counted = dict_output[num]
            if counted < 6:
                day_count_car += 1
                day_car += f'<strong>Машина {num}: {counted} ⬅</strong>\n'
            elif counted >= 6:
                day_count_car += 1
                day_car += f'Машина {num}: {counted}\n'

    answer = (f'Заказы созданные\n'
              f'с    {time_start}\n'
              f'до {time_end}\n\n'
              f'Количество <b>НОЧНЫХ {night_count_car}</b>:\n'
              f'{night_car}\n\n'
              f'Количество <b>ДНЕВНЫХ {day_count_car}</b>:\n'
              f'{day_car}\n\n')

    if error_list != '':
        answer = answer + f'🔴 Что-то не так с заказами:\n{error_list}'
    return answer


if __name__ == '__main__':
    print(create_orders_answer())
