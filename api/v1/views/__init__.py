#!/usr/bin/python3
"""Creates base Blueprint"""
from flask import Blueprint

app_views = Blueprint('/api/v1', __name__)
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.users import *
