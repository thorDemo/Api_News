# -*- coding:utf-8 -*-
from peewee import *

db = MySQLDatabase("station", host='127.0.0.1', port=3306, user='root', passwd='123456', charset='utf8')


class Person(Model):
    id = IntegerField()
    name = CharField()

    class Meta:
        table_name = 'JSModel_test'
        database = db # This model uses the "people.db" database.


if __name__ == '__main__':
    db.connect()
    db.create_tables([Person])

    Person.insert({'id': 1, 'name': 'Nicholas'})