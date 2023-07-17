from django.urls import path, include
from django.views.generic import RedirectView
from . import api
from . import views

# I wrote this code


urlpatterns = [
    path("", views.home, name="index"),
    path("api/", views.home, name="api"),
    path("api/protein/", api.CreateProtein.as_view(), name="create_protein"),
    path(
        "api/protein/<protein_id>", api.ProteinDetail.as_view(), name="protein_detail"
    ),
    path("api/pfam/<domain_id>", api.PfamDetail.as_view(), name="pfam_detail"),
    path(
        "api/proteins/<taxa_id>", api.ProteinsByTaxa.as_view(), name="proteins_by_taxa"
    ),
    path("api/pfams/<taxa_id>", api.PfamsByTaxa.as_view(), name="pfams_by_taxa"),
    path(
        "api/coverage/<protein_id>",
        api.CoverageByProtein.as_view(),
        name="coverage_by_protein",
    ),
]

# end of code I wrote
