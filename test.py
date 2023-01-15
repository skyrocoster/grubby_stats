import requests
import json
import time
from app import *
import os
from sqlalchemy import inspect
import pandas as pd


test = Heroes().hero_map()
print(test)
