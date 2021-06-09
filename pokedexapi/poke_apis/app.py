import json
import mysql_connector as mysql
import boto3


def lambda_handler(event, context):
    credentials = get_param(f"/services/pokedexapi/prod/db", True)
    sql_string = "SELECT * FROM pokeapi_urls limit 1"

    try:
        mssql_object = mysql.MySQL(credentials)

        cursor = mssql_object.connect()

        res = mssql_object.run_get_all(cursor, sql_string)

        pokemon_limit = res[0][1]
        poke_sprite_image = res[0][2]
        pokemon_id = res[0][3]
        pokemon_sprite_image = res[0][4]

    except Exception as ex:
        response_message = str(ex)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps({
            "PokemonLimit": pokemon_limit,
            "PokedexSpriteImage": poke_sprite_image,
            "PokemonID": pokemon_id,
            "PokemonSpriteImage": pokemon_sprite_image,
        }),
    }


def get_param(parameter_name, loads=False):
    client = boto3.client('ssm')
    resp = client.get_parameter(Name=parameter_name, WithDecryption=True)
    body = resp['Parameter']['Value']
    if loads:
        return json.loads(body)
    else:
        return body


if __name__ == "__main__":
    print(lambda_handler("", ""))
