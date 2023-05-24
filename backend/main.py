from fastapi import FastAPI

from database.couch_api import DatabaseService

app = FastAPI()

db_service = DatabaseService(server_url='http://192.168.0.80:5984/', username='admin', password='admin')


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api/views/create/{db_name}")
async def create_views(db_name: str):
    db_service.create_views(db_name)
    return {"message": "views created"}


@app.get("/api/mastodon/new/{source}/{seconds}")
async def get_new_mastodon_data(source: str, seconds: int):
    docs = db_service.get_mastodon_new_data('mastodon', source, seconds)
    return {"message": "new mastodon data", "docs": docs}


@app.get("/api/mastodon/sentiment/{seconds}")
async def get_mastodon_sentiment_data(seconds: int):
    docs = db_service.get_mastodon_sentiment_data('mastodon', seconds)
    return {"message": "mastodon sentiment", "docs": docs}


@app.get("/api/sudo/regional_language")
async def get_sudo_regional_language():
    docs = db_service.get_sudo_regional_language('sudo_regional_language')
    return {"message": "sudo regional language", "docs": docs}


@app.get("/api/sudo/regional_population")
async def get_sudo_regional_population():
    docs = db_service.get_sudo_regional_population('sudo_regional_population')
    return {"message": "sudo regional population", "docs": docs}


@app.get("/api/sudo/gcc_homeless")
async def get_sudo_gcc_homeless():
    docs = db_service.get_sudo_gcc_homeless('sudo_gcc_homeless')
    return {"message": "sudo gcc homeless", "docs": docs}


@app.get("/api/sudo/sudo_sa4_homeless")
async def get_sudo_sa4_homeless():
    docs = db_service.get_sudo_sa4_homeless('sudo_sa4_homeless')
    return {"message": "sudo sa4 homeless", "docs": docs}


@app.get("/api/sudo/sudo_sa4_income")
async def get_sudo_sa4_income():
    docs = db_service.get_sudo_sa4_income('sudo_sa4_income')
    return {"message": "sudo sa4 income", "docs": docs}


@app.get("/api/sudo/init")
async def init_sudo():
    db_service.init_sudo()
    return {"message": "sudo initialized"}


@app.get("/api/twitter/count/{scenario}")
async def init_huge(scenario: str):
    # scenario = 'all' | 'homeless' | 'language' | 'abuse'
    if scenario == 'all':
        return {
            "message": "tweets number counted",
            "count": {
                "all": 378927,
                "homeless": 5682,
                "language": 8551,
                "abuse": 23694
            }
        }
    if scenario == 'homeless':
        return {"message": "tweets number counted", "count": 5682}
    if scenario == 'language':
        return {"message": "tweets number counted", "count": 8551}
    if scenario == 'abuse':
        return {"message": "tweets number counted", "count": 23694}

# run with `uvicorn main:app --reload`
