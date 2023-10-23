from bucket import bucket

# TODO: Needs to be implemented asyncly by JavaScript.
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result