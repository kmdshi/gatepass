import hashlib
import json


def generate_hash(**args):
    args_string = json.dumps(args, sort_keys=True)
    return hashlib.sha256(args_string.encode()).hexdigest()


