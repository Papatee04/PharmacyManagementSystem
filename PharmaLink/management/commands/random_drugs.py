import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from PharmaLink.models import Drug

class Command(BaseCommand):
    help = 'Populate the Drug model with 20 different drugs'

    def handle(self, *args, **kwargs):
        drug_names = [
            'Aspirin', 'Ibuprofen', 'Paracetamol', 'Lipitor', 'Nexium',
            'Advil', 'Amoxicillin', 'Atorvastatin', 'Metformin', 'Prednisone',
            'Omeprazole', 'Losartan', 'Amlodipine', 'Hydrochlorothiazide', 'Simvastatin',
            'Azithromycin', 'Gabapentin', 'Levothyroxine', 'Albuterol', 'Celebrex'
        ]

        drug_types = ['Opioids', 'Antibiotics', 'Statins', 'Pain Relievers', 'Antacids']

        for _ in range(20):
            drug = Drug(
                name=random.choice(drug_names),
                description=f"Description for {random.choice(drug_names)}",
                manufacturer=f"Manufacturer for {random.choice(drug_names)}",
                strength=f"Strength for {random.choice(drug_names)}",
                dosage=f"{random.randint(1, 100)} mg",
                photo=None,  # You can add the path to a drug photo if available
            )
            drug.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully created drug: {drug.name}'))

