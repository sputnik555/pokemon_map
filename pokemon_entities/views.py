import folium

from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_entities = PokemonEntity.objects.filter(
            pokemon=pokemon,
            appeared_at__lte=localtime(),
            disappeared_at__gte=localtime()
        )
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                pokemon.image.path if pokemon.image else DEFAULT_IMAGE_URL
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append(get_pokemon_data_basic(pokemon))

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=requested_pokemon,
        appeared_at__lte=localtime(),
        disappeared_at__gte=localtime()
    )
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            requested_pokemon.image.path if requested_pokemon.image else ''
        )
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': get_pokemon_data_full(requested_pokemon)
    })


def get_pokemon_data_full(pokemon):

    pokemon_data = {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
    }
    if pokemon.next_evolution:
        pokemon_data['next_evolution'] = get_pokemon_data_basic(pokemon.next_evolution)
    previous_evolution = pokemon.previous_evolutions.all().first()
    if previous_evolution:
        pokemon_data['previous_evolution'] = get_pokemon_data_basic(previous_evolution)
    return pokemon_data


def get_pokemon_data_basic(pokemon):
    pokemon_data = {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
        'title_ru': pokemon.title,
    }
    return pokemon_data
