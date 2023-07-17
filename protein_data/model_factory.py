import factory
from factory.django import DjangoModelFactory
from factory import SubFactory, post_generation
from factory.fuzzy import FuzzyText, FuzzyInteger
from .models import *

# I wrote this code

# Model factory classes


class PfamFactory(DjangoModelFactory):
    class Meta:
        model = Pfam

    domain_id = FuzzyText(length=10)
    domain_description = FuzzyText(length=10)


class DomainFactory(DjangoModelFactory):
    class Meta:
        model = Domain

    description = FuzzyText(length=10)
    pfam_id = SubFactory(PfamFactory)
    start = FuzzyInteger(0, 10)
    stop = FuzzyInteger(0, 10)


class TaxonomyFactory(DjangoModelFactory):
    class Meta:
        model = Taxonomy

    taxa_id = FuzzyText(length=10)
    clade = FuzzyText(length=10)
    genus = FuzzyText(length=10)
    species = FuzzyText(length=10)


class ProteinFactory(DjangoModelFactory):
    class Meta:
        model = Protein

    protein_id = FuzzyText(length=10)
    sequence = FuzzyText(length=10)
    length = FuzzyInteger(0, 10)
    taxonomy = SubFactory(TaxonomyFactory)

    @post_generation
    def domains(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for domain in extracted:
                self.domains.add(domain)


# end of code I wrote
