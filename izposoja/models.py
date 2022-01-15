from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager
import string

OZNAKE = [(crka,crka) for crka in string.ascii_uppercase ]
class Omara(models.Model):
    naziv = models.CharField(max_length=100)
    oznaka = models.CharField(choices=OZNAKE, max_length=10)
    polica = models.PositiveIntegerField()


class Lokacija(models.Model):
    ime = models.CharField(max_length=100)
    naslov = models.CharField(max_length=1000)
    omara = models.ForeignKey(Omara, on_delete=models.PROTECT)


class Oprema(models.Model):
    naziv = models.CharField(max_length=200)
    lokacija = models.ForeignKey(Lokacija, on_delete=models.PROTECT)
    kolicina = models.PositiveIntegerField()
    poskodbe = models.TextField()
    opombe = models.TextField()


class Funkcija(models.Model):
    naziv = models.CharField(max_length=100)
    pomocnik = models.BooleanField()

class Oseba(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    telefonska_stevilka = PhoneNumberField(default='+41524204242')
    ime = models.CharField(max_length=100)
    priimek = models.CharField(max_length=100)


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['telefonska_stevilka','ime','priimek']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Rezervacija(models.Model):
    oseba = models.ForeignKey(Oseba, on_delete=models.CASCADE)
    oprema = models.ForeignKey(Oprema,on_delete=models.CASCADE)
    cas = models.DateTimeField()
    trajanje_izposoje = models.PositiveIntegerField()
    odobreno = models.BooleanField()
    opombe = models.TextField()


class Izposoja(models.Model):
    rezervacija = models.ForeignKey(Rezervacija, on_delete=models.CASCADE)
    cas_izposoje = models.DateTimeField()
    cas_vracila = models.DateTimeField()
    opmbe = models.TextField()


class Odklepanje(models.Model):
    rezervacija = models.ForeignKey(Rezervacija,on_delete=models.PROTECT)
    cas_odklepanja = models.DateTimeField()


