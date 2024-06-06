import sqlite3
import utils


def update_db(data_from_form=None):
    car_list_from_MoySklad = []
    cars = utils.request_to_MoySklad_stores()
    for car in cars['rows']:
        car_list_from_MoySklad.append(f"car_{car['name']}")
        car_list_from_MoySklad.sort()  # [01, 02, 03...]
    conn = sqlite3.connect('car_status.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS car_status'
                   '(car_num TEXT NOT NULL PRIMARY KEY,'
                   'status INTEGER)'
                   )
    cursor.execute('SELECT car_num FROM car_status')
    cars_from_DB = cursor.fetchall()
    car_list_from_DB = []
    for car_num in cars_from_DB:
        car_list_from_DB.append(car_num[0])
    for car_num in car_list_from_MoySklad:
        try:
            status = dict(data_from_form)[car_num]
        except:
            status = 1
        if car_num in car_list_from_DB:
            cursor.execute('UPDATE car_status SET status = ? WHERE car_num = ?', (status, car_num))
            conn.commit()
        else:
            cursor.execute('INSERT INTO car_status (car_num, status) VALUES (?, ?)', (car_num, status))
            conn.commit()
    conn.close()


def execute_car_status():
    conn = sqlite3.connect('car_status.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS car_status'
                   '(car_num TEXT NOT NULL,'
                   'status INTEGER)'
                   )
    cursor.execute('SELECT * FROM car_status')
    car_status = cursor.fetchall()
    conn.close()
    return car_status
