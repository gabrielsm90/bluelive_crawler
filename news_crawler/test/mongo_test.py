# -*- coding: utf-8 -*-

from dao.mongo import SubmissionsMongoDAO

if __name__ == '__main__':
    mongo = SubmissionsMongoDAO()
    resultado = mongo.get_10_submissions_point_any_kind()
    for data in resultado:
        print(data)