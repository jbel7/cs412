# File: voter_analytics/models.py
# Name: Jed Belsany
# BU email: belsanyj@bu.edu
# Description: Models for voter analytics application with voter model and data loading function 

from django.db import models
from datetime import datetime
# Create your models here.

class Voter(models.Model):
    """
    Model representing a registered voter in Newton, MA.
    
    Fields store voter identification, address, registration details,
    and voting history across recent elections.
    """
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Address Information
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    
    # Registration Information
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)
    
    # Voting History
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField(default=0)
    
    def __str__(self):
        """
        String representation of a Voter object.
        
        Returns:
            str: Full name and street address of the voter
        """
        return f"{self.first_name} {self.last_name} - {self.street_number} {self.street_name}"
    
    class Meta:
        ordering = ['last_name', 'first_name']


def load_data():
    """
    Load voter data from newton_voters.csv file into the database.
    
    This function reads the CSV file, creates Voter objects for each row,
    and saves them to the database. It skips the header row and handles
    data type conversions for dates and boolean values.
    """
    import csv
    from datetime import datetime
    
    # Delete existing records to avoid duplicates
    Voter.objects.all().delete()
    
    filename = 'newton_voters.csv'
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                # Create a new Voter object
                voter = Voter(
                    first_name=row['First Name'].strip(),
                    last_name=row['Last Name'].strip(),
                    street_number=row['Residential Address - Street Number'].strip(),
                    street_name=row['Residential Address - Street Name'].strip(),
                    apartment_number=row['Residential Address - Apartment Number'].strip() if row['Residential Address - Apartment Number'].strip() else None,
                    zip_code=row['Residential Address - Zip Code'].strip(),
                    date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                    date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                    party_affiliation=row['Party Affiliation'],  # Keep as-is (2 chars with potential trailing space)
                    precinct_number=row['Precinct Number'].strip(),
                    v20state=row['v20state'].strip().upper() == 'TRUE',
                    v21town=row['v21town'].strip().upper() == 'TRUE',
                    v21primary=row['v21primary'].strip().upper() == 'TRUE',
                    v22general=row['v22general'].strip().upper() == 'TRUE',
                    v23town=row['v23town'].strip().upper() == 'TRUE',
                    voter_score=int(row['voter_score'])
                )
                voter.save()
                
            except Exception as e:
                print(f"Error processing row: {e}")
                continue
    
    print(f"Successfully loaded {Voter.objects.count()} voters.")