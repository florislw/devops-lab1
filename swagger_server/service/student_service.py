from pymongo import MongoClient
import random
import os

CONNECTION_STRING = os.environ.get('MONGO_URI')

student_db = MongoClient(CONNECTION_STRING).student_db
student_collection = student_db.students


# helper function
def get_student_by_id(student_id):
    student = student_collection.find_one({
        'student_id': student_id,
    })

    return student


def add(student=None):
    # if no student_id is given, generate a random one
    # this is not very efficient, put for the purpose of this
    # exercise it is okay.
    # It would be best to require a student_id for this request,
    # but this way we do not need to modify the tests
    while not student.student_id:
        random_id = random.randint(0, 9999)
        if not get_student_by_id(random_id):
            student.student_id = random_id
            break  # this break ensures we do not do the else check
    else:
        # We do not check for a duplicate names and last name combination,
        # instead we now check for duplicate student_ids
        if get_student_by_id(student.student_id):
            return 'already exists', 409

    student_collection.insert_one(student.to_dict())

    # return the possibly generated student_id, hide the internal _id
    student_id = student.student_id
    return student_id


def get_by_id(student_id=None, subject=None):
    # We rewrite this function to look for the student_id, instead of the
    # primary key. Whether this is actually better depends on the use cases
    # of the API, however for the purpose of this exercise it makes more
    # sense to me.

    student = get_student_by_id(student_id)

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
