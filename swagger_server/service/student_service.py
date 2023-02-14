from pymongo import MongoClient

# Get the container IP using docker inspect
CONNECTION_STRING = "mongodb://host.docker.internal:27017"

student_db = MongoClient(CONNECTION_STRING).student_db
student_collection = student_db.students

def add(student=None):
    # todo: make student_id a primary key
    # We do not check for a duplicate names and last name combination,
    # instead we now check for duplicate student_ids
    res = student_collection.find_one({
        'student_id': student.student_id,
    })
    if res:
        return 'already exists', 409

    doc = student_collection.insert_one(student.to_dict())
    doc_id = doc.inserted_id
    return str(doc_id)

def get_by_id(student_id=None, subject=None):
    # We rewrite this function to look for the student_id, instead of the
    # primary key. Whether this is actually better depends on the use cases
    # of the API, however for the purpose of this exercise it makes more
    # sense to me.

    student = student_collection.find_one({
        'student_id': student_id
    })

    if not student:
        return 'not found', 404

    student.pop('_id')
    return student

def delete(student_id=None):
    res = student_collection.delete_one({
        'student_id': student_id
    })

    if not res.deleted_count:
        return 'not found', 404

    return student_id