from django.core.management.base import BaseCommand
from PharmaLink.models import Specialization

class Command(BaseCommand):
    help = 'Populate specializations in the database'

    def handle(self, *args, **options):
        specializations = [
    'Cardiology',
    'Dermatology',
    'Ophthalmology',
    'Gastroenterology',
    'Neurology',
    'Orthopedics',
    'Endocrinology',
    'Pediatrics',
    'Oncology',
    'Rheumatology',
    'Nephrology',
    'Pulmonology',
    'Infectious Disease',
    'Hematology',
    'Geriatrics',
    'Urology',
    'Psychiatry',
    'Radiology',
    'Anesthesiology',
    'Family Medicine',
    'Internal Medicine',
    'General Surgery',
    'Obstetrics and Gynecology',
    'Emergency Medicine',
    'Physical Medicine and Rehabilitation',
    'Dentistry',
    'Allergy and Immunology',
    'Pathology',
    'Nuclear Medicine',
    'None',  # A placeholder for cases where no specialization is selected
]

        for specialization_name in specializations:
            specialization, created = Specialization.objects.get_or_create(name=specialization_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created specialization: {specialization_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Specialization already exists: {specialization_name}'))
