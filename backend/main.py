from fastapi import FastAPI
import os

from database.couch_api import DatabaseService

app = FastAPI()

read_db_host = os.environ.get('READ_DB_HOST')
read_db_port = os.environ.get('READ_DB_PORT')
write_db_port = os.environ.get('WRITE_DB_PORT')
write_db_host = os.environ.get('WRITE_DB_HOST')

# read_db_host = '192.168.0.80'
# read_db_port = '5984'
# write_db_port = '5984'
# write_db_host = '192.168.0.80'

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
    write_db_service.init_twitter()
    return {"message": "twitter initialized"}


@app.get("/api/twitter/count/{scenario}")
async def get_twitter_scenario_count(scenario: str):
    # scenario = 'all' | 'homeless' | 'abuse'
    docs = read_db_service.get_twitter_scenario_count('twitter', scenario)
    return {"message": "twitter scenario count", "docs": docs}


@app.get("/api/twitter/homeless/distribution/{gcc}")
async def get_twitter_homeless_related_distribution(gcc: str):
    docs = read_db_service.get_twitter_homeless_related_distribution('twitter', gcc)
    return {"message": "twitter homeless related distribution", "docs": docs}


@app.get("/api/twitter/homeless/heat")
async def get_twitter_homeless_related_heat():
    docs = read_db_service.get_twitter_homeless_related_heat('twitter')
    return {"message": "twitter homeless related heat", "docs": docs}


@app.get("/api/twitter/sentiment/gcc")
async def get_twitter_sentiment_gcc():
    docs = read_db_service.get_twitter_sentiment_gcc('twitter')
    return {"message": "twitter sentiment gcc", "docs": docs}


@app.get("/api/twitter/sentiment/weighted")
async def get_twitter_sentiment_weighted():
    docs = read_db_service.get_sudo_abs_regional_population_sentiment_weighted('sudo_abs_regional_population')
    return {"message": "twitter sentiment weighted", "docs": docs}


@app.get("/api/twitter/sentiment/period/{kind}")
async def get_twitter_sentiment_period(kind: str):
    docs = read_db_service.get_twitter_sentiment_period('twitter', kind)
    return {"message": "twitter sentiment period", "docs": docs}

# run with `uvicorn main:app --reload`
