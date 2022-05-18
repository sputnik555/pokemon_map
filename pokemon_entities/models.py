from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField(blank=True, default=0)
    health = models.IntegerField(blank=True, default=0)
    strength = models.IntegerField(blank=True, default=0)
    defence = models.IntegerField(blank=True, default=0)
    stamina = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return '{}, {}'.format(self.lat, self.lon)
