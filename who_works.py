from database_processing import execute_car_status, update_db


def form_who_works():
    form = ''
    car_list = execute_car_status()
    if not car_list:
        update_db()
        car_list = execute_car_status()
    for car_num, status in car_list:
        checked1 = ''
        checked2 = ''
        checked3 = ''
        if status == 1:
            checked1 = 'checked'
        elif status == 2:
            checked2 = 'checked'
        elif status == 3:
            checked3 = 'checked'
        form += (f'<div>'
                 f'<b>{car_num[-2:]}</b> '
                 f'<span class="radio">'
                 f'<input label="Ночь" type="radio" id="{"car_" + car_num + "1"}" name="{car_num}" value="1" {checked1} />'
                 f'<input label="День" type="radio" id="{"car_" + car_num + "2"}" name="{car_num}" value="2" {checked2} />'
                 f'<input label="Вых." type="radio" id="{"car_" + car_num + "3"}" name="{car_num}" value="3" {checked3} />'
                 f'</span><br>'
                 f'</div>')

    skeleton = (f"<!doctype html>"
                f"<html lang='ru'>"
                f'<head>'
                f'<meta charset="UTF-8">'
                f'<meta name="viewport"'
                f'content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, '
                f'minimum-scale=1.0">'
                f'<meta http-equiv="X-UA-Compatible" content="ie=edge">'
                f'<link rel="stylesheet" href="static/css/main.css">'
                f'<title>Кто в работе</title>'
                f'</head>'
                f'<body>'
                f'<form method="post">'
                f'<div align = "center">'
                f'<h3>Кто в работе</h3>'
                f'{form}'
                f'<input class="btn-new" type="submit" value="Сохранить">'
                f'</form>'
                f'</div>'
                f'</body>'
                f'</html>')

    return skeleton
