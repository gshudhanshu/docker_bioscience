from django.core.management import BaseCommand, CommandError
from django.utils import timezone
from protein_data.models import *
import csv
import time


# I wrote this code
class Command(BaseCommand):
    help = "Earse previous protein data and populate new data"

    # File paths for data files
    assignment_data_sequences_csv = "./data_files/assignment_data_sequences.csv"
    assignment_data_set_csv = "./data_files/assignment_data_set.csv"
    pfam_descriptions_csv = "./data_files/pfam_descriptions.csv"

    start_time = timezone.now()
    inter_time = start_time

    def handle(self, *args, **options):
        self.stdout.write("Erasing previous protein data")
        self.erase_previous_data()
        test = timezone.now() - self.inter_time
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()
        self.stdout.write("Populating with new data")
        self.populate_with_new_data()

    # Erase previous data from database
    def erase_previous_data(self):
        Protein.objects.all().delete()
        Domain.objects.all().delete()
        Pfam.objects.all().delete()
        Taxonomy.objects.all().delete()

    # Populate database with new data
    def populate_with_new_data(self):
        self.stdout.write("Populating pfam")
        self.populate_pfam()
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()

        self.stdout.write("Populating taxonomy domains")
        self.populate_taxonomy_domains()
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )
        self.inter_time = timezone.now()

        self.stdout.write("Populating protein")
        self.populate_protein()
        self.stdout.write(
            self.style.SUCCESS(
                "Time (sec): " + str((timezone.now() - self.inter_time).total_seconds())
            )
        )

        self.stdout.write("Database populated successfully!")
        self.inter_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                "Total time (sec): "
                + str((timezone.now() - self.start_time).total_seconds())
            )
        )

    # Populate pfam data
    def populate_pfam(self):
        with open(self.pfam_descriptions_csv, "r") as csvfile:
            field_names = ["domain_id", "domain_description"]
            reader = csv.DictReader(csvfile, field_names)
            for row in reader:
                pfam = Pfam(
                    domain_id=row["domain_id"],
                    domain_description=row["domain_description"],
                )
                pfam.save()

    # Populate taxonomy and domain data
    def populate_taxonomy_domains(self):
        with open(self.assignment_data_set_csv, "r") as csvfile:
            field_names = [
                "protein_id",
                "taxonomy_id",
                "clade",
                "genus_species",
                "domain_description",
                "domain_id",
                "domain_start",
                "domain_end",
                "length_sequence",
            ]
            reader = csv.DictReader(csvfile, field_names)
            for row in reader:
                # Handle None value for genus_species
                if row["genus_species"] is None:
                    genus = ""
                    species = ""
                else:
                    genus = row["genus_species"].split(" ")[0]
                    species = row["genus_species"].split(" ")[1]

                taxonomy, _ = Taxonomy.objects.get_or_create(
                    taxa_id=row["taxonomy_id"],
                    clade=row["clade"],
                    genus=genus,
                    species=species,
                )

                pfam_id = row["domain_id"]
                # Handle None value for domain_id
                try:
                    pfam = Pfam.objects.get(domain_id=pfam_id)
                except Pfam.DoesNotExist:
                    pfam, _ = Pfam.objects.get_or_create(
                        domain_id=pfam_id, domain_description=""
                    )

                domain, _ = Domain.objects.get_or_create(
                    description=row["domain_description"],
                    start=row["domain_start"],
                    stop=row["domain_end"],
                    pfam_id=pfam,
                )

                protein = Protein(
                    protein_id=row["protein_id"],
                    taxonomy=taxonomy,
                    length=row["length_sequence"],
                )

                protein.save()
                protein.domains.add(domain),

    # Populate protein sequence data
    def populate_protein(self):
        with open(self.assignment_data_sequences_csv, "r") as csvfile:
            field_names = ["protein_id", "sequence"]
            reader = csv.DictReader(csvfile, field_names)
            for row in reader:
                # Handle None value for sequence
                try:
                    protein, _ = Protein.objects.get_or_create(
                        protein_id=row["protein_id"]
                    )
                    # print(row["protein_id"])
                    protein.sequence = row["sequence"]
                    protein.save()
                except KeyError as e:
                    print(f"Skipping row {row['protein_id']} because of KeyError {e}")


# end of code I wrote
