from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    Lat = models.FloatField()
    Lon = models.FloatField()

    def __str__(self):
        return '{}, {}'.format(self.Lat, self.Lon)
