from collections import OrderedDict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *
from .model_factory import *
from .serializers import *
from .api import *


# I wrote this code
# Serializer test
class ProteinSerializerTest(APITestCase):
    def setUp(self):
        self.protein = ProteinFactory()
        self.proteinserializer = ProteinSerializer(instance=self.protein)

    def tearDown(self):
        Pfam.objects.all().delete()
        Domain.objects.all().delete()
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()

    # Ensure the serializer contains all the expected fields
    def test_contains_expected_fields(self):
        data = self.proteinserializer.data
        self.assertEqual(
            set(data.keys()),
            set(["protein_id", "sequence", "taxonomy", "length", "domains"]),
        )

    # Ensure the protein_id field is correct
    def test_protein_id_field_content(self):
        data = self.proteinserializer.data
        self.assertEqual(data["protein_id"], self.protein.protein_id)


# api/protein
# @POST Add new protein to database
class ProteinCreateTest(APITestCase):
    def setUp(self):
        self.url = reverse("create_protein")
        self.valid_payload = {
            "protein_id": "ABC123",
            "sequence": "AGTACGTACG",
            "length": 10,
            "taxonomy": {
                "taxa_id": "10005",
                "clade": "A",
                "genus": "Genus",
                "species": "Species",
            },
            "domains": [
                {
                    "description": "Domain 1",
                    "start": 1,
                    "stop": 10,
                    "pfam_id": {
                        "domain_id": "PF001",
                        "domain_description": "Domain Description",
                    },
                }
            ],
        }

    def tearDown(self):
        Pfam.objects.all().delete()
        Domain.objects.all().delete()
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()

    # Test creating a new protein
    def test_create_protein(self):
        response = self.client.post(self.url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        protein = Protein.objects.first()
        self.assertEqual(protein.protein_id, "ABC123")

        expected_data = ProteinSerializer(protein).data
        self.assertEqual(response.data, expected_data)


# api/protein/<protein_id>
# @GET Get protein by protein_id
class ProteinDetailTest(APITestCase):
    def setUp(self):
        self.protein = ProteinFactory()
        self.url = reverse(
            "protein_detail", kwargs={"protein_id": self.protein.protein_id}
        )

    def tearDown(self):
        Pfam.objects.all().delete()
        Domain.objects.all().delete()
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()

    # Test getting a protein by protein_id
    def test_get_protein(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = ProteinSerializer(self.protein).data
        self.assertEqual(response.data, expected_data)


# api/pfam/<pfam_id>
# @GET Get pfam by pfam_id
class PfamDetailTest(APITestCase):
    def setUp(self):
        self.pfam = PfamFactory()
        self.url = reverse("pfam_detail", kwargs={"domain_id": self.pfam.domain_id})

    def tearDown(self):
        Pfam.objects.all().delete()
        Domain.objects.all().delete()
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()

    # Test getting a pfam by pfam_id
    def test_get_pfam(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = PfamSerializer(self.pfam).data
        self.assertEqual(response.data, expected_data)


# api/proteins/<taxa_id>
# @GET Get proteins by taxa_id
class ProteinsByTaxaTest(APITestCase):
    def setUp(self):
        self.taxa = TaxonomyFactory()
        self.protein = ProteinFactory(taxonomy=self.taxa)
        self.url = reverse("proteins_by_taxa", kwargs={"taxa_id": self.taxa.taxa_id})

    def tearDown(self):
        Pfam.objects.all().delete()
        Domain.objects.all().delete()
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()

    # Test getting proteins by taxa_id
    def test_get_proteins(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = ProteinListSerializer([self.protein], many=True).data
        self.assertEqual(response.data, expected_data)


# api/pfams/<taxa_id>
# @GET Get pfams by taxa_id
class PfamsByTaxaTest(APITestCase):
    def setUp(self):
        self.taxa = TaxonomyFactory()
        self.pfam = PfamFactory()
        self.protein = ProteinFactory(taxonomy=self.taxa)
        self.domain = DomainFactory(protein=self.protein, pfam_id=self.pfam)
        self.url = reverse("pfams_by_taxa", kwargs={"taxa_id": self.taxa.taxa_id})

    def tearDown(self):
        Pfam.objects.all().delete()
        Domain.objects.all().delete()
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()

    # Test getting pfams by taxa_id
    def test_get_pfams(self):
        response = self.client.get(self.url)
        if response.data:
            expected_data = PfamListSerializer([self.domain], many=True).data
            self.assertEqual(response.data, expected_data)
        else:
            expected_data = []
            self.assertEqual(response.data, expected_data)


# api/coverage/<protein_id>
# @GET Get coverage by protein_id
class CoverageByProteinTest(APITestCase):
    def setUp(self):
        self.protein = ProteinFactory()
        self.domain = DomainFactory(protein=self.protein)
        self.url = reverse(
            "coverage_by_protein", kwargs={"protein_id": self.protein.protein_id}
        )

    def tearDown(self):
        Pfam.objects.all().delete()
        Domain.objects.all().delete()
        Taxonomy.objects.all().delete()
        Protein.objects.all().delete()

    # Test getting coverage by protein_id
    def test_get_coverage(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {"coverage": 0.0}
        self.assertEqual(response.data, expected_data)


# End of code I wrote
