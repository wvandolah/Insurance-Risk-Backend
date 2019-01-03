# make sure to get the database set up, makemigrations, etc,
import csv

import os

from insurance.models import InsuranceProductBuild

with open('insurance_build_tables.csv',newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p = InsuranceProductBuild(male=row['Male'],female=row['Female'], height=row['Height'],
            min_age = row['Min Age'], max_age = row['Max Age'], min_weight =row['Min Weight'],
            max_weight = row['Max Weight'], product_type = row['Type'], carrier = row['Product 1'],
            product2 = row['Product 2'], product3= row['Product 3'])
            p.save()
   