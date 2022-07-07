import requests


# Check the situation of our Pokémon API
def resultResponse():
    r = requests.get('https://pokeapi.co/api/v2/pokemon/')
    status = r.status_code
    data = r.json()
    httpCode = requests.options('https://pokeapi.co/api/v2/pokemon/').status_code

    return {
        "Status": status,
        "Data": data,
        "HTTP Codes": httpCode
    }

# oficial site: https://pokeapi.co/
