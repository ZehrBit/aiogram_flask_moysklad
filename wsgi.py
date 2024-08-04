from flask import Flask, request

import config
from who_works import form_who_works
import database_processing as dp

app = Flask(__name__)


@app.route('/', methods=['get', 'post'])
def who_works():
    if dict(request.form) == {}:
        return form_who_works()
    else:
        dp.update_db(request.form)
        return form_who_works()


@app.route('/reset', methods=['get', 'post'])
def reset_button():
    dp.reset_db()
    return form_who_works()


if __name__ == '__main__':
    app.run(debug=False, host=config.HOST, port=config.PORT)
