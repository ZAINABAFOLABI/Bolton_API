from flask import Blueprint
import json
from src.config import database

modules = Blueprint("lessons", __name__,
                    url_prefix="/mybolton/v1/modules")

@modules.get('/')
def get_all_lessons():
    return  {"Course": "SWE7101"}

# @modules.post('/new-module')
# def add_new_module():
#     json_data = request.get_json()
#     print(json_data)

# new_module = Module (

# )