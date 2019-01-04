from django.core.management.base import BaseCommand
import csv
from insurance.models import InsuranceProductBuild
# import os
# path =  "../Top_Ten_Death.csv" # Set path of new directory here
# os.chdir(path) # changes the directory
# from dashboard.models import Country # imports the model
class Command(BaseCommand):
    help = 'A description of your command'

    def handle(self, **options):
      with open('insurance_build_tables.csv',newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
          p = InsuranceProductBuild(male=row['Male'],female=row['Female'], height=row['Height'],
          min_age=row['Min Age'], max_age=row['Max Age'], min_weight =row['Min Weight'],
          max_weight=row['Max Weight'], product_type=row['Type'], carrier=row['Product 1'],
          product2=row['Product 2'], product3=row['Product 3'])
          p.save()
