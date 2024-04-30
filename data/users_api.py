import flask
from . import db_session
from .users import User
from flask import jsonify
from flask import request
from werkzeug.security import generate_password_hash

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=(
                'id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password_hash'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_users1(user_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(User).get(user_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': jobs.to_dict(only=(
                'id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password_hash', 'city_from'))
        }
    )


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


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['POST'])
def edit_jobs(users_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    s = db_sess.query(User).filter(User.id == users_id).first()
    if s:
        jobs = db_sess.query(User).get(users_id)
        if not jobs:
            return jsonify({'error': 'Not found'})
        db_sess.delete(jobs)
        db_sess.commit()
        users = User(
            id=users_id,
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
    else:
        return jsonify({'error': 'Id not exists'})
