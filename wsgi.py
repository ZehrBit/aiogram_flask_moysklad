from flask import Flask, render_template, url_for, request

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


if __name__ == '__main__':
    app.run(debug=True, host=config.HOST, port=config.PORT)
