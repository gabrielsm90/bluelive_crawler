
from dao.mongo import SubmissionsMongoDAO

if __name__ == '__main__':
    mongo = SubmissionsMongoDAO()
    mongo.collection.drop()