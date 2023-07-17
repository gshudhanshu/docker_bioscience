from django.db import models


# I wrote this code


class Pfam(models.Model):
    domain_id = models.CharField(primary_key=True, max_length=256, blank=False)
    domain_description = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.domain_id


class Domain(models.Model):
    description = models.CharField(max_length=256, blank=True, null=True)
    pfam_id = models.ForeignKey(Pfam, on_delete=models.CASCADE)
    start = models.IntegerField(blank=True, null=True)
    stop = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.protein} {self.pfam.domain_id}"


class Taxonomy(models.Model):
    taxa_id = models.CharField(primary_key=True, max_length=10, blank=False)
    clade = models.CharField(max_length=1, blank=True, null=True)
    genus = models.CharField(max_length=256, blank=True, null=True)
    species = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"{self.taxa_id} {self.clade} {self.genus} {self.species}"


class Protein(models.Model):
    protein_id = models.CharField(primary_key=True, max_length=10, blank=False)
    sequence = models.TextField(blank=True)
    length = models.IntegerField(blank=True, null=True)
    taxonomy = models.ForeignKey(Taxonomy, null=True, on_delete=models.CASCADE)
    domains = models.ManyToManyField(Domain, null=True)

    def __str__(self):
        return self.protein_id


# end of code I wrote
