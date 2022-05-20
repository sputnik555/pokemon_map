from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('Наименование', max_length=200)
    title_en = models.CharField('Наименование (англ.)', max_length=200, blank=True)
    title_jp = models.CharField('Наименование (яп.)', max_length=200, blank=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Картинка', blank=True, null=True)
    next_evolution = models.ForeignKey(
        'self',
        verbose_name='Следующая форма',
        on_delete=models.SET_NULL,
        related_name='previous_evolutions',
        null=True,
        blank=True
    )

    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Покемон',
        on_delete=models.CASCADE,
        related_name='entities'
    )
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Дата появление')
    disappeared_at = models.DateTimeField('Дата исчезновения')
    level = models.IntegerField('Уровень', blank=True, default=0)
    health = models.IntegerField('Здоровье', blank=True, default=0)
    strength = models.IntegerField('Сила', blank=True, default=0)
    defence = models.IntegerField('Защита', blank=True, default=0)
    stamina = models.IntegerField('Выносливость', blank=True, default=0)

    def __str__(self):
        return '{}, {}'.format(self.lat, self.lon)
