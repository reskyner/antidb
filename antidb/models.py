from django.db import models


class Sequence(models.Model):
    sequence = models.TextField(blank=False, null=False, unique=True)

    class Meta:
        db_table = 'sequence'


class Structure(models.Model):
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    structure_file = models.FileField(upload_to='structure_files/%Y%M%d')

    class Meta:
        db_table = 'structure'


class Pdb(models.Model):
    pdb_code = models.CharField(max_length=255, blank=False, null=False, unique=True)
    pdb_file = models.FileField(upload_to='pdb_files/%Y%M%d')

    XRD = 'XRD'
    EM = 'EMP'
    SNMR = 'SNM'
    SSHM = 'SSH'
    EMHM = 'EMH'
    SS = 'SSC'
    SSNMR = 'SSN'
    SSNMRHM = 'SSM'
    NA = 'N/A'

    EM_CHOICES = (
        (XRD, 'X-ray diffraction'),
        (EM, 'Electron microscopy'),
        (SNMR, 'Solution NMR'),
        (SSHM, 'Solution scattering/Homology modelling'),
        (EMHM, 'Electron microscopy/Homology modelling'),
        (SS, 'Solution scattering'),
        (SSNMR, 'Solution-state NMR'),
        (SSNMRHM, 'Solution-state NMR/Homology modelling'),
        (NA, 'N/A')

    )

    exp_method = models.CharField(choices=EM_CHOICES, max_length=3, default=NA)
    organism = models.CharField(max_length=225, blank=True, null=True)
    resolution = models.FloatField(blank=True, null=True)
    r_factor = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'pdb'


class Methodology(models.Model):
    pass

class Antigen(models.Model):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)

    class Meta:
        db_table = 'antigen'

class Antibody(models.Model):
    pdb_code = models.ForeignKey(Pdb, on_delete=models.CASCADE)
    antigen = models.ForeignKey(Antigen, blank=True, null=True, on_delete=models.CASCADE)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)

    class Meta:
        db_table = 'antibody'

class HeavyChain(models.Model):
    antibody = models.ForeignKey(Antibody, on_delete=models.CASCADE)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)

    class Meta:
        db_table = 'heavy_chain'


class LightChain(models.Model):
    antibody = models.ForeignKey(Antibody, on_delete=models.CASCADE)

    N = 'N'
    K = 'K'
    L = 'L'

    LC_CHOICES = (
        (N, 'N/A'),
        (K, 'kappa'),
        (L, 'lambda'),
    )

    type = models.CharField(choices=LC_CHOICES, max_length=1, default=N)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)

    class Meta:
        db_table = 'light_chain'


class HeavyVariable(models.Model):
    heavy_chain = models.ForeignKey(HeavyChain, on_delete=models.CASCADE)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)

    class Meta:
        db_table = 'heavy_variable'


class HeavyConserved(models.Model):
    heavy_chain = models.ForeignKey(HeavyChain, on_delete=models.CASCADE)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)

    class Meta:
        db_table = 'heavy_conserved'


class LightVariable(models.Model):
    light_chain = models.ForeignKey(LightChain, on_delete=models.CASCADE)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)

    class Meta:
        db_table = 'light_variable'


class LightConserved(models.Model):
    light_chain = models.ForeignKey(LightChain, on_delete=models.CASCADE)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)

    class Meta:
        db_table = 'light_conserved'


class CDRH(models.Model):
    heavy_variable = models.ForeignKey(HeavyVariable, on_delete=models.CASCADE)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cdr_heavy'


class CDRL(models.Model):
    light_variable = models.ForeignKey(LightVariable, on_delete=models.CASCADE)
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cdr_light'


class CDRPair(models.Model):
    heavy_cdr = models.ForeignKey(CDRH, on_delete=models.CASCADE)
    light_cdr = models.ForeignKey(CDRL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cdr_pair'


class CDRClust(models.Model):

    COHTHIA = 'CH'
    KABAT = 'KB'
    CONTACT = 'CN'
    NA = 'NA'

    M_CHOICES = (
        (COHTHIA, 'Cohthia'),
        (KABAT, 'Kabat'),
        (CONTACT, 'Contact'),
        (NA, 'N/A'),
    )

    method = models.CharField(choices=M_CHOICES, max_length=2, default=NA)

    H1 = 'H1'
    H2 = 'H2'
    H3 = 'H3'
    L1 = 'L1'
    L2 = 'L2'
    L3 = 'L3'
    # NA = 'NA'

    T_CHOICES = (
        (H1, 'H1'),
        (H2, 'H2'),
        (H3, 'H3'),
        (L1, 'L1'),
        (L2, 'L2'),
        (L3, 'L3'),
        (NA, 'N/A'),
    )

    type = models.CharField(choices=T_CHOICES, max_length=2, default=NA)

    pair = models.ForeignKey(CDRPair, on_delete=models.CASCADE)


    class Meta:
        db_table = 'cdr_cluster'


class BindingAffinity(models.Model):
    antibody = models.ForeignKey(Antibody, on_delete=models.CASCADE)
    antigen = models.ForeignKey(Antigen, on_delete=models.CASCADE)
    affinity = models.FloatField(blank=False, null=False)

    class Meta:
        unique_together = ('antibody', 'antigen')
        db_table = 'binding_affinity'





