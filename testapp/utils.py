""" File for all auxiliary functions"""
import re
import csv
import os
from bs4 import BeautifulSoup
from pathlib import Path
import datetime
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = os.path.join(BASE_DIR, 'files', 'test_task.csv')
XML_PATH = os.path.join(BASE_DIR, 'files', 'test_task.xml')
MEDIA_PATH = os.path.join(BASE_DIR, "files")


def get_csv_data(csv_file):
    """function for reading CSV and write it in list of dicts"""
    csv_data = []
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if all(row) and len(row) == 3:
                csv_data.append({'username': row[0], 'password': row[1], 'date_joined': row[2]})
        csv_data.pop(0)  # remove header row
    return csv_data


def get_xml_data(xml_file):
    """function that parse xml file and write data to list with dicts"""
    xml_data = []
    with open(xml_file, 'r') as f:
        file = f.read()
        soup = BeautifulSoup(file, 'xml')
        for user in soup.select('users user'):
            first_name = user.first_name.text
            last_name = user.last_name.text
            photo_url = user.avatar.text
            if all([first_name, last_name, photo_url]):
                xml_data.append({'first_name': user.first_name.text, 'last_name': user.last_name.text,
                                 'photo_url': user.avatar.text})
    return xml_data


def clear_data(data):
    """function that ignore text in round and square brackets """
    for i in range(2):
        for item in data:
            for key in item.keys():
                item[key] = re.sub("\(.*?\)|\[.*?\]", "", item[key])
                if item[key] == '':  # if after removing item becomes empty
                    data.remove(item)
    return data


def collect_valid_data(csv_data, xml_data):
    """ function for ignoring users without some kind of information"""
    validated_data = []
    for csv_item in csv_data:
        for xml_item in xml_data:
            if xml_item['last_name'].lower() in csv_item['username'].lower():
                xml_item.update(csv_item)
                validated_data.append(xml_item)
                xml_data.remove(xml_item)
    return validated_data


def collect_from_stored_files():
    """ Complicated function that takes data from test files, clean it and return in list of dicts"""
    csv_data = clear_data(get_csv_data(CSV_PATH))
    xml_data = clear_data(get_xml_data(XML_PATH))
    return collect_valid_data(csv_data, xml_data)


def collect_from_uploaded_files(csv_file, xml_file):
    """Complicated function that takes data from uploaded files, clean it and return in list of dicts"""
    csv_data = clear_data(get_csv_data(os.path.join(MEDIA_PATH, os.path.basename(csv_file))))
    xml_data = clear_data(get_xml_data(os.path.join(MEDIA_PATH, os.path.basename(xml_file))))
    return collect_valid_data(csv_data, xml_data)


def add_users(user_model, data):
    """ function that create a new users and add it into database"""
    for user_data in data:
        if not user_model.objects.filter(username=user_data['username']):
            user_model.objects.create(
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                date_joined=datetime.datetime.fromtimestamp(int(user_data['date_joined'])),
                photo_url=user_data['photo_url']
            )
        valid_user = user_model.objects.get(username=user_data["username"])
        valid_user.set_password(user_data["password"])
        valid_user.save()
