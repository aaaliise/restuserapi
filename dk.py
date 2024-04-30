import flask
from requests import get
from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from data import db_session
from data.jobs import Jobs
from data.users import User
from werkzeug.security import generate_password_hash
import flask
from data import db_session
from data.users import User
from flask import jsonify
from flask import request
from werkzeug.security import generate_password_hash
from data import db_session, jobs_api, users_api

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@blueprint.route('/api/users', methods=['POST'])
def get_users2():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    elif 'id' in request.json:
        s = db_sess.query(User).filter(User.id == request.json['id']).first()
        if s:
            return jsonify({'error': 'Id already exists'})
    users = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email']
    )
    users.password_hash = generate_password_hash(request.json['password'])
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_users1(user_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(User).get(user_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': jobs.to_dict()
        }
    )


@app.route('/users_show/<int:user_id>')
def user_show(user_id):
    info = get(f'http://127.0.0.1:8080/api/users/{user_id}').json().get('users')
    print(info)
    if info is not None:
        res = get(f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={info["city_from"]}&format=json')
        pos = ",".join(res.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split())
        map_params = {
            "ll": pos,
            "l": 'sat',
            "z": '14'
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = get(map_api_server, params=map_params)
        map_file = f"static/img/map.png"
        with open(map_file, mode="wb") as file:
            file.write(response.content)
    f = info is None
    return render_template('nostalgy.html', data=info, flag=f)


if __name__ == '__main__':
    db_session.global_init('db/blogs2.db')
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080, host='127.0.0.1')

