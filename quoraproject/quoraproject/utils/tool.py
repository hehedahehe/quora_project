# -*- coding: utf-8 -*-
import os, json, scrapy

def get_files(dir, condition_file):
    for each in os.walk(dir):
        files =[_each for _each in each[2] if condition_file(_each)]
        return files

def file_condition(file_name):
    if file_name.startswith("urls"):
        return True
    else:
        return False




