from rest_framework import serializers
from .models import *


# I wrote this code


# Serializer for the Pfam model
class PfamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pfam
        fields = ["domain_id", "domain_description"]


# Serializer for the Taxonomy model
class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ["taxa_id", "clade", "genus", "species"]


# Serializer for the Domain model
class DomainsSerializer(serializers.ModelSerializer):
    pfam_id = PfamSerializer()

    class Meta:
        model = Domain
        fields = ["pfam_id", "description", "start", "stop"]


# Serializer for the POST request for the Pfam model
class PostPfamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pfam
        fields = ["domain_id", "domain_description"]
        extra_kwargs = {"domain_id": {"validators": []}}


# Serializer for the POST request for the Taxonomy model
class PostTaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ["taxa_id", "clade", "genus", "species"]
        extra_kwargs = {"taxa_id": {"validators": []}}


# Serializer for the POST request for the Domain model
class PostDomainsSerializer(serializers.ModelSerializer):
    pfam_id = PostPfamSerializer()

    class Meta:
        model = Domain
        fields = ["pfam_id", "description", "start", "stop"]


# Serializer for the POST request for the Protein model
class ProteinSerializer(serializers.ModelSerializer):
    taxonomy = PostTaxonomySerializer()
    domains = PostDomainsSerializer(many=True)

    class Meta:
        model = Protein
        fields = ["protein_id", "sequence", "taxonomy", "length", "domains"]

    def save(self, **kwargs):
        taxonomy_data = self.validated_data.pop("taxonomy", None)
        domains_data = self.validated_data.pop("domains", [])

        # Update or create the Taxonomy instance
        if taxonomy_data:
            taxa_id = taxonomy_data["taxa_id"]
            try:
                taxonomy = Taxonomy.objects.get(taxa_id=taxa_id)
                for attr, value in taxonomy_data.items():
                    setattr(taxonomy, attr, value)
                taxonomy.save()
            except Taxonomy.DoesNotExist:
                taxonomy = Taxonomy.objects.create(**taxonomy_data)
            self.validated_data["taxonomy"] = taxonomy

        protein = super().save(**kwargs)

        # Update or create the Domain instances
        for domain_data in domains_data:
            pfam_data = domain_data.pop("pfam_id", None)
            if pfam_data:
                pfam_id = pfam_data["domain_id"]
                try:
                    pfam = Pfam.objects.get(domain_id=pfam_id)
                    for attr, value in pfam_data.items():
                        setattr(pfam, attr, value)
                    pfam.save()
                except Pfam.DoesNotExist:
                    pfam = Pfam.objects.create(**pfam_data)
                domain, _ = Domain.objects.update_or_create(
                    pfam_id=pfam, protein=protein, defaults=domain_data
                )
                protein.domains.add(domain)

        return protein


# Serializer for the Domain model
class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ["id"]


# Serializer for the Prtroin list
class ProteinListSerializer(serializers.ModelSerializer):
    domains = DomainSerializer(many=True)

    class Meta:
        model = Protein
        fields = ["domains", "protein_id"]

    def get_domains(self, obj):
        domain_ids = obj.domains.values_list("id", flat=True)
        return list(domain_ids)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        domains = representation.get("domains", [])
        if domains:
            representation["id"] = representation["domains"][0]["id"]
            representation.pop("domains")
        else:
            representation["id"] = None
            representation.pop("domains")
        return {"id": representation["id"], "protein_id": representation["protein_id"]}


# Serializer for the Pfam list
class PfamListSerializer(serializers.ModelSerializer):
    pfam_id = PfamSerializer()

    class Meta:
        model = Domain
        fields = ["id", "pfam_id"]


# Serializer for the Protein coverage
class ProteinCoverageSerializer(serializers.Serializer):
    coverage = serializers.FloatField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {"coverage": representation["coverage"]}


# end of code I wrote
