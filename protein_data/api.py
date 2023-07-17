from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response

# I wrote this code


# api/protein
# @POST Add new protein to database
class CreateProtein(generics.CreateAPIView):
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer

    def perform_create(self, serializer):
        instance = serializer.save()


# api/protein/<protein_id>
# @GET Get protein by protein_id
class ProteinDetail(generics.RetrieveAPIView):
    queryset = Protein.objects.all()
    serializer_class = ProteinSerializer
    lookup_field = "protein_id"


# api/pfam/<pfam_id>
# @GET Get pfam by pfam_id
class PfamDetail(generics.RetrieveAPIView):
    queryset = Pfam.objects.all()
    serializer_class = PfamSerializer
    lookup_field = "domain_id"


# api/proteins/<taxa_id>
# @GET Get proteins by taxa_id
class ProteinsByTaxa(generics.ListAPIView):
    serializer_class = ProteinListSerializer

    def get_queryset(self):
        taxa_id = self.kwargs["taxa_id"]
        return Protein.objects.filter(taxonomy_id=taxa_id)


# api/pfams/<taxa_id>
# @GET Get pfams by taxa_id
class PfamsByTaxa(generics.ListAPIView):
    serializer_class = PfamListSerializer

    def get_queryset(self):
        taxa_id = self.kwargs["taxa_id"]
        return Domain.objects.filter(protein__taxonomy_id=taxa_id)


# api/coverage/<protein_id>
# @GET Get coverage by protein_id
class CoverageByProtein(generics.RetrieveAPIView):
    serializer_class = ProteinCoverageSerializer
    lookup_field = "protein_id"

    def get_queryset(self):
        protein_id = self.kwargs["protein_id"]
        return Protein.objects.filter(protein_id=protein_id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        coverage = 0
        for domain in instance.domains.all():
            coverage += (domain.stop - domain.start) / instance.length
            print(coverage)

        serializer = self.get_serializer({"coverage": coverage})
        return Response(serializer.data)


# end of code I wrote
