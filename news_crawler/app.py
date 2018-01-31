#!flask/bin/python
from flask import Flask, jsonify, render_template, request
from dao.mongo import SubmissionsMongoDAO

app = Flask(__name__)

def get_result_set(function_name, param):
    mongo = SubmissionsMongoDAO()
    resultado = getattr(mongo, function_name)(param)
    mongo.close_connection()
    return jsonify(resultado)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submissions_point_any_kind')
def get_10_submissions_point_any_kind():
    return get_result_set('get_top_submissions_point_any_kind', 10)

@app.route('/submissions_point_internal_discussion')
def get_10_submissions_point_internal_discussion():
    return get_result_set('get_top_submissions_point_internal_discussion', 10)

@app.route('/submissions_point_external_link')
def get_10_submissions_point_external_link():
    return get_result_set('get_top_submissions_point_external_link', 10)

@app.route('/submissions_comments_any_kind')
def get_10_submissions_comments_any_kind():
    return get_result_set('get_top_submissions_comments_any_kind', 10)

@app.route('/submissions_comments_internal_discussion')
def get_10_submissions_comments_internal_discussion():
    return get_result_set('get_top_submissions_comments_internal_discussion', 10)

@app.route('/submissions_comments_external_link')
def get_10_submissions_comments_external_link():
    return get_result_set('get_top_submissions_comments_external_link', 10)

@app.route('/top_submitters')
def get_10_top_submitters():
    return get_result_set('get_top_submitters', 10)

@app.route('/top_commenters')
def get_10_top_commenters():
    return get_result_set('get_top_commenters', 10)

@app.route('/top_active_users')
def get_10_top_active_users():
    return get_result_set('get_top_active_users', 10)

@app.route('/posts_from_user', methods=['POST'])
def get_posts_from_user():
    return get_result_set('get_posts_user', request.form['username'])

@app.route('/posts_user_commented', methods=['POST'])
def get_posts_commented_by_user():
    return get_result_set('get_posts_commented_by_user', request.form['username'])

if __name__ == '__main__':
    app.run(debug=True)

