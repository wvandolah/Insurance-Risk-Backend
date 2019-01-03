from django.core.management.base import BaseCommand
import csv
from insurance.models import TopDeath
# import os
# path =  "../Top_Ten_Death.csv" # Set path of new directory here
# os.chdir(path) # changes the directory
# from dashboard.models import Country # imports the model
class Command(BaseCommand):
    help = 'A description of your command'

    def handle(self, **options):
        with open('Top_Ten_Death.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = TopDeath(Rank=row['Rank'], under1=row['<1'],
                             one_4=row['1-4'],
                             five_9=row['5-9'],
                             ten_14=row['10-14'],
                             fifteen_24=row['15-24'],
                             twofive_34=row['25-34'],
                             threefive_44=row['35-44'],
                             fourfive_54=row['45-54'],
                             fivefive_64=row['55-64'],
                             over65=row['65+'],
                             Total=row['Total'])
                p.save()
