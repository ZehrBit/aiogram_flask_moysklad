import datetime
import requests
import config


def time_interval():
    """Возвращает два значения: начало промежутка "time_start" и конец промежутка "time_end"."""
    date_now = datetime.datetime.now()
    if datetime.time(hour=0, minute=0, second=0) < date_now.time() < datetime.time(hour=10, minute=0, second=0):
        time_start = date_now - datetime.timedelta(hours=24)
        time_start = time_start.replace(hour=10, minute=0, second=0, microsecond=0)
        time_end = date_now.replace(hour=9, minute=59, second=59, microsecond=0)
    else:
        time_start = date_now.replace(hour=10, minute=0, second=0, microsecond=0)
        time_end = date_now + datetime.timedelta(hours=24)
        time_end = time_end.replace(hour=9, minute=59, second=59, microsecond=0)
    return time_start, time_end


def request_to_MoySklad_orders(opr3=None):
    """Возвращает JSON с данными о заказах"""
    if opr3 == 'opr3':
        return requests.get(
            url=f'https://api.moysklad.ru/api/remap/1.2/entity/customerorder?filter=created>={time_interval()[0]};'
                f'created<{time_interval()[1]};'
                f'owner=https://api.moysklad.ru/api/remap/1.2/entity/employee/25599451-4b96-11e7-7a6c-d2a90011c47a',
            headers=config.HEADER, timeout=30).json()
    elif opr3 is None:
        return requests.get(url=f'https://api.moysklad.ru/api/remap/1.2/entity/customerorder?filter=created>={time_interval()[0]};'
                            f'created<{time_interval()[1]}', headers=config.HEADER, timeout=30).json()


def request_to_MoySklad_demands(opr3=None):
    """Возвращает JSON с данными о отгрузках"""
    if opr3 == 'opr3':
        return requests.get(
            url=f'https://api.moysklad.ru/api/remap/1.2/entity/demand?filter=created>={time_interval()[0]};'
                f'created<{time_interval()[1]};'
                f'owner=https://api.moysklad.ru/api/remap/1.2/entity/employee/25599451-4b96-11e7-7a6c-d2a90011c47a',
            headers=config.HEADER, timeout=30).json()
    elif opr3 is None:
        return requests.get(
            url=f'https://api.moysklad.ru/api/remap/1.2/entity/demand?filter=created>={time_interval()[0]};'
                f'created<{time_interval()[1]}', headers=config.HEADER, timeout=30).json()


def request_to_MoySklad_stores():
    """Возвращает JSON с данными о складах"""
    return requests.get('https://api.moysklad.ru/api/remap/1.2/entity/store', headers=config.HEADER,
                        timeout=30).json()

def request_to_MoySklad_cashin():
    """Возвращает JSON с данными о приходных ордерах"""
    return requests.get(url=f'https://api.moysklad.ru/api/remap/1.2/entity/cashin?filter=created>={time_interval()[0]};'
                            f'created<{time_interval()[1]};'
                            f'owner=https://api.moysklad.ru/api/remap/1.2/entity/employee/25599451-4b96-11e7-7a6c-d2a90011c47a',
                        headers=config.HEADER, timeout=30).json()


def user_verification(func):
    pass
