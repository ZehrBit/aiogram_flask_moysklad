import config
import utils
import datetime


def create_audit_answer():
    orders_json = utils.request_to_MoySklad_orders(opr3='opr3')
    demands_json = utils.request_to_MoySklad_demands(opr3='opr3')
    cashin_json = utils.request_to_MoySklad_cashin()

    def create_and_moment():
        """Проверка даты создания и присвоенной вручную даты"""
        answer = ''
        count = 0
        for order in orders_json['rows']:
            try:
                count += 1
                date_created = datetime.datetime.strptime(order['created'], '%Y-%m-%d %H:%M:%S.%f')
                if datetime.time(hour=10, minute=0, second=0) <= date_created.time() <= datetime.time(hour=23,
                                                                                                      minute=59,
                                                                                                      second=59):
                    date_created = date_created.date() + datetime.timedelta(days=1)
                else:
                    date_created = date_created.date()
                date_moment = datetime.datetime.strptime(order['moment'], '%Y-%m-%d %H:%M:%S.%f').date()
                if date_moment != date_created:
                    answer += f'{order["name"]}\n'
            except Exception as e:
                answer += f'Ошибка:{e} у заказа: {order["name"]}\n'

        if answer == '':
            answer += '🟢 Ошибок в <strong>ДАТАХ ЗАКАЗОВ</strong>\nне найдено'
        else:
            answer = '🔴 Ошибки в <strong>ДАТАХ СОЗДАНИЯ</strong>:\n' + answer
        counted_orders = f'Количество заказов у Оператора-3:  <strong>{count}</strong>'
        return answer, counted_orders

    def audit_delivery_sum():
        """Проверка суммы доставки у курьеров"""
        answer = ''
        for order in orders_json['rows']:
            if order['owner']['meta']['href'][-36:] == config.ID_OPERATOR:
                try:
                    for attribute in order['attributes']:
                        if attribute['name'] == 'Сумма доставки':
                            if 590 <= attribute['value'] <= 1190:
                                pass
                            else:
                                answer += f'{order["name"]}\n'
                except Exception as e:
                    answer += f'Ошибка:{e} у {order["name"]}\n'
        if answer == '':
            answer += '🟢 Ошибок в <strong>СУММАХ ДОСТАВОК</strong> от 490р до 1090р у курьеров\nне найдено'
        else:
            answer = '🔴 Ошибки в <strong>ДОСТАВКАХ</strong> от 490р до 1090р у курьеров:\n' + answer
        return answer

    def audit_car_number_in_order_and_demand():
        """Проверяет совпадают ли номера машин(складов) в Заказах и Отгрузках.
        Если не совпадают, то формирует строку с именами(номерами) этих Заказов и Отгрузок"""
        answer = ''
        idcar_ordername = {}
        for order in orders_json['rows']:
            try:
                id_order = order['id']
                id_car = order['store']['meta']['href'][-36:]
                name_order = order['name']
                idcar_ordername[id_order] = {id_car: name_order}
            except KeyError:
                answer += f'Ошибка ключа в заказе: {order["name"]}\n'

        idcar_demandname = {}
        for demand in demands_json['rows']:
            try:
                id_order = demand['customerOrder']['meta']['href'][-36:]
                id_car = demand['store']['meta']['href'][-36:]
                name_demand = demand['name']
                idcar_demandname[id_order] = {id_car: name_demand}
            except KeyError:
                answer += f'Ошибка ключа в заказе: {demand["name"]}\n'

        for id_order1, idcar_nameorder in idcar_ordername.items():
            for id_order2, idcar_namedemand in idcar_demandname.items():
                if id_order1 == id_order2:
                    idcar_nameorder = tuple(idcar_nameorder.items())[0]
                    idcar_namedemand = tuple(idcar_namedemand.items())[0]
                    if idcar_nameorder[0] != idcar_namedemand[0]:
                        answer += f'в заказе: {idcar_nameorder[1]} и отгрузке: {idcar_namedemand[1]}\n'
        if answer == '':
            answer += '🟢 Во всех <strong>ЗАКАЗАХ и ОТГРУЗКАХ</strong> номера машин совпадают'
        else:
            answer = '🔴 Номера машин <strong>НЕ СОВПАДАЮТ</strong>:\n' + answer
        return answer

    def audit_only_one_demand():
        """Проверяет заказы на связь с Отгрузками.
        Формирует строку с именами(номерами) заказов, где больше одной отгрузки или где нет отгрузок вообще"""
        answer = ''
        for order in orders_json['rows']:
            try:
                if len(order['demands']) == 1:
                    pass
                elif len(order['demands']) > 1:
                    answer += f'заказ: {order["name"]} - <strong>БОЛЬШЕ ОДНОЙ ОТГРУЗКИ</strong>\n'
            except KeyError:
                answer += f'заказ: {order["name"]} - <strong>НЕТ ОТГРУЗКИ</strong>\n'
        if answer == '':
            answer += '🟢 Во всех <strong>ЗАКАЗАХ</strong> по одной отгрузке'
        else:
            answer = '🔴 В <strong>ЗАКАЗАХ ЕСТЬ ОШИБКИ</strong> с количеством <strong>ОТГРУЗОК</strong>:\n' + answer
        return answer

    def audit_sum_in_order_and_demand():
        """Проверяет совпадают ли суммы в Заказах и Отгрузках.
        Если не совпадают, то формирует строку с именами(номерами) этих Заказов и Отгрузок"""
        answer = ''
        full_sum = 0.0
        id_sum_ordername = []
        for order in orders_json['rows']:
            try:
                id_order = order['id']
                sum_order = order['sum']
                name_order = order['name']
                id_sum_ordername.append([id_order, sum_order, name_order])
                full_sum += sum_order
            except KeyError:
                answer += f'Ошибка ключа в заказе: {order["name"]}\n'
        full_sum = int(full_sum / 100)
        zp = int(full_sum / 100 * 6)
        id_sum_demandname = []
        for demand in demands_json['rows']:
            try:
                id_order = demand['customerOrder']['meta']['href'][-36:]
                sum_order = demand['sum']
                name_demand = demand['name']
                id_sum_demandname.append([id_order, sum_order, name_demand])
            except KeyError:
                answer += f'Отгрузка {demand["name"]} не связана с заказом\n'

        for id_order1, sum1, ordername in id_sum_ordername:
            for id_order2, sum2, demandname in id_sum_demandname:
                if id_order1 == id_order2:
                    if sum1 != sum2:
                        answer += f'в заказе: {ordername} и отгрузке: {demandname}\n'
        if answer == '':
            answer += '🟢 Во всех <strong>ЗАКАЗАХ и ОТГРУЗКАХ</strong> суммы совпадают'
        else:
            answer = '🔴 Суммы не совпадают:\n' + answer
        return answer, f'Общая сумма заказов:  <strong>{str(full_sum)}</strong> ₽', f'6% от общей суммы:  <strong>{str(zp)}</strong> ₽'

    def audit_date_in_order_demand_cashin():
        """Проверяет совпадает ли даты в Заказах, Отгрузках и Приходных ордерах.
        Если не совпадают, то формирует строку с именами(номерами) этих Заказов и Отгрузок"""
        answer = ''
        id_date_ordername = []
        id_date_demandname = []
        id_date_cashin = []
        for order in orders_json['rows']:
            try:
                id_order = order['id']
                date_moment_order = datetime.datetime.strptime(order['moment'], '%Y-%m-%d %H:%M:%S.%f').date()
                name_order = order['name']
                id_date_ordername.append([id_order, date_moment_order, name_order])
            except KeyError:
                answer += f'Заказ {order["name"]} не связан с отгрузкой\n'

        for demand in demands_json['rows']:
            try:
                id_order = demand['customerOrder']['meta']['href'][-36:]
                id_demand = demand['id']
                date_moment_demand = datetime.datetime.strptime(demand['moment'], '%Y-%m-%d %H:%M:%S.%f').date()
                name_demand = demand['name']
                id_date_demandname.append([id_order, id_demand, date_moment_demand, name_demand])
            except KeyError:
                answer += f'Отгрузка {demand["name"]} не связана с заказом\n'

        for cashin in cashin_json['rows']:
            try:
                id_demand = cashin['operations'][0]['meta']['href'][-36:]
                date_moment_cashin = datetime.datetime.strptime(cashin['moment'], '%Y-%m-%d %H:%M:%S.%f').date()
                name_cashin = cashin['name']
                id_date_cashin.append([id_demand, date_moment_cashin, name_cashin])
            except KeyError:
                answer += f'Приходный ордер {cashin["name"]} не связан с отгрузкой\n'

        for id_order1, date_moment_order, ordername in id_date_ordername:
            for id_order2, id_demand, date_moment_demand, demandname in id_date_demandname:
                if id_order1 == id_order2:
                    if date_moment_order != date_moment_demand:
                        answer += f'в заказе: {ordername} и отгрузке: {demandname}\n'

        for id_demand1, date_moment_cashin, cashinname in id_date_cashin:
            for id_order, id_demand2, date_moment_demand, demandname in id_date_demandname:
                if id_demand1 == id_demand2:
                    if date_moment_cashin != date_moment_demand:
                        answer += f'в отгрузке: {demandname} и приходном ордере: {cashinname}\n'

        if answer == '':
            answer += '🟢 Во всех <strong>ЗАКАЗАХ, ОТГРУЗКАХ и ПРИХОДНЫХ ОРДЕРАХ</strong> даты совпадают'
        else:
            answer = '🔴 Даты <strong>НЕ СОВПАДАЮТ</strong>:\n' + answer
        return answer

    answer_sum, full_sum, zp = audit_sum_in_order_and_demand()
    listname_with_date_errors, counted_orders = create_and_moment()
    return (f'Заказы созданные\nс    {utils.time_interval()[0]}\nдо {utils.time_interval()[1]}\n\n'
            f'● {counted_orders}\n\n'
            f'● {full_sum}\n\n'
            f'● {zp}\n\n'
            f'{audit_delivery_sum()}\n\n'
            f'{listname_with_date_errors}\n\n'
            f'{audit_date_in_order_demand_cashin()}\n\n'
            f'{audit_car_number_in_order_and_demand()}\n\n'
            f'{audit_only_one_demand()}\n\n'
            f'{answer_sum}\n\n')
