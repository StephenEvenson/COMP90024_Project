from fastapi import FastAPI
import os

from database.couch_api import DatabaseService

app = FastAPI()

read_db_host = os.environ.get('READ_DB_HOST')
read_db_port = os.environ.get('READ_DB_PORT')
write_db_port = os.environ.get('WRITE_DB_PORT')
write_db_host = os.environ.get('WRITE_DB_HOST')

read_db_service = DatabaseService(server_url=f'http://{read_db_host}:{read_db_port}/', username='admin',
                                  password='admin')
write_db_service = DatabaseService(server_url=f'http://{write_db_host}:{write_db_port}/', username='admin',
                                   password='admin')


# common
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api/views/create/{db_name}")
async def create_views(db_name: str):
    write_db_service.create_views(db_name)
    return {"message": "views created"}


# mastodon
@app.get("/api/mastodon/init")
async def init_mastodon():
    write_db_service.init_mastodon()
    return {"message": "mastodon initialized"}


@app.get("/api/mastodon/new/{source}/{seconds}")
async def get_new_mastodon(source: str, seconds: int):
    docs = read_db_service.get_mastodon_new('mastodon', source, seconds)
    return {"message": "new mastodon data", "docs": docs}


@app.get("/api/mastodon/sentiment/{seconds}")
async def get_mastodon_sentiment(seconds: int):
    docs = read_db_service.get_mastodon_sentiment('mastodon', seconds)
    return {"message": "mastodon sentiment", "docs": docs}


@app.get("/api/mastodon/lang/{seconds}")
async def get_mastodon_lang(seconds: int):
    docs = read_db_service.get_mastodon_lang_count('mastodon', seconds)
    return {"message": "mastodon lang", "docs": docs}


@app.get("/api/mastodon/count/{scenario}")
async def get_mastodon_scenario_count(scenario: str):
    # scenario = 'all' | 'homeless' | 'abuse'
    docs = read_db_service.get_mastodon_scenario_count('mastodon', scenario)
    return {"message": "mastodon scenario count", "docs": docs}


# sudo
@app.get("/api/sudo/init")
async def init_sudo():
    write_db_service.init_sudo()
    return {"message": "sudo initialized"}


@app.get("/api/sudo/regional_language")
async def get_sudo_regional_language():
    docs = read_db_service.get_sudo_regional_language('sudo_regional_language')
    return {"message": "sudo regional language", "docs": docs}


@app.get("/api/sudo/regional_population")
async def get_sudo_regional_population():
    docs = read_db_service.get_sudo_regional_population('sudo_regional_population')
    return {"message": "sudo regional population", "docs": docs}


@app.get("/api/sudo/gcc_homeless")
async def get_sudo_gcc_homeless():
    docs = read_db_service.get_sudo_gcc_homeless('sudo_gcc_homeless')
    return {"message": "sudo gcc homeless", "docs": docs}


@app.get("/api/sudo/sudo_sa4_homeless")
async def get_sudo_sa4_homeless():
    docs = read_db_service.get_sudo_sa4_homeless('sudo_sa4_homeless')
    return {"message": "sudo sa4 homeless", "docs": docs}


@app.get("/api/sudo/sudo_sa4_income")
async def get_sudo_sa4_income():
    docs = read_db_service.get_sudo_sa4_income('sudo_sa4_income')
    return {"message": "sudo sa4 income", "docs": docs}


# twitter
@app.get("/api/twitter/init")
async def init_twitter():
    return {"message": "twitter initialized"}


@app.get("/api/twitter/count/{scenario}")
async def get_twitter_scenario_count(scenario: str):
    # scenario = 'all' | 'homeless' | 'language' | 'abuse'
    if scenario == 'all':
        return {
            "message": "tweets scenario count",
            "count": {
                "all": 378927,
                "homeless": 5682,
                "language": 8551,
                "abuse": 23694
            }
        }
    if scenario == 'homeless':
        return {"message": "tweets scenario count", "count": 5682}
    if scenario == 'language':
        return {"message": "tweets scenario count", "count": 8551}
    if scenario == 'abuse':
        return {"message": "tweets scenario count", "count": 23694}


@app.get("/api/twitter/test")
async def get_twitter_test():
    docs = read_db_service.get_twitter_test('target_tweets')
    return {"message": "twitter test", "docs": docs}

# run with `uvicorn main:app --reload`
