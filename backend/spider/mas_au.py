from mastodon import Mastodon, StreamListener
import json

# import db

MASTODON_ACCESS_TOKEN = "hufM3Vs_Gock6w0RsiICkwX4VquIm17tMzeRFiwRMVI"
# mastodon = Mastodon(api_base_url='https://mastodon.online', access_token = os.environ['MASTODON_ACCESS_TOKEN'])
# mastodon = Mastodon(api_base_url='https://mastodon.online', access_token=MASTODON_ACCESS_TOKEN)
# mastodon.retrieve_mastodon_version()
# mastodon.status("109666136628267939")["content"]

m = Mastodon(
    api_base_url=f'https://mastodon.au',
    client_id="RdWuJXarXVqmT2lyNxvSLxCxqUUbxsb6ZvdSULtPT4s",
    client_secret="ZiubtS7EMH0YLK0RF4LJ6SGqE9B2oReUS9TvQ_o4Nd0",
    # access_token=os.environ['MASTODON_ACCESS_TOKEN']
    access_token=MASTODON_ACCESS_TOKEN
)


class Listener(StreamListener):
    def on_update(self, status):
        # data = json.dumps(status, indent=2, sort_keys=True, default=str, ensure_ascii=False)
        print(status)
        print(status.keys())
        # db.save_data(status)
        # print("save success")
        # with open("example-mastodon.json", "a") as outfile:
        #     outfile.write(data)
        #     outfile.write("\n")


print("start crawling")
m.stream_public(Listener())
