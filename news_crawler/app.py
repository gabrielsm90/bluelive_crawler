#!flask/bin/python
from flask import Flask, jsonify
from dao.mongo import SubmissionsMongoDAO
import os

app = Flask(__name__)

def get_result_set(function_name):
    mongo = SubmissionsMongoDAO()
    resultado = getattr(mongo, function_name)()
    mongo.close_connection()
    return jsonify(resultado)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/submissions_point_any_kind', methods=['GET'])
def get_10_submissions_point_any_kind():
    return get_result_set('get_10_submissions_point_any_kind')

@app.route('/get_10_submissions_point_internal_discussion', methods=['GET'])
def get_10_submissions_point_internal_discussion():
    return get_result_set('get_10_submissions_point_internal_discussion')

@app.route('/get_10_submissions_point_external_link', methods=['GET'])
def get_10_submissions_point_external_link():
    return get_result_set('get_10_submissions_point_external_link')

@app.route('/get_10_submissions_comments_any_kind', methods=['GET'])
def get_10_submissions_comments_any_kind():
    return get_result_set('get_10_submissions_comments_any_kind')

@app.route('/get_10_submissions_comments_internal_discussion', methods=['GET'])
def get_10_submissions_comments_internal_discussion():
    return get_result_set('get_10_submissions_comments_internal_discussion')

@app.route('/get_10_submissions_comments_external_link', methods=['GET'])
def get_10_submissions_comments_external_link():
    return get_result_set('get_10_submissions_comments_external_link')

if __name__ == '__main__':
    print(os.getcwd())
    app.run(debug=True)

