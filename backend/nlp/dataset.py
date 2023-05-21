import json
import mmap

from torch.utils.data import Dataset
from tqdm import tqdm


class TweetsDataSet(Dataset):
    def __init__(self, jsonl_path: str, is_test=False):
        super().__init__()
        self.jsonl_path = jsonl_path
        self.is_test = is_test
        jsonl_file = open(jsonl_path, 'r', encoding='utf-8')
        self.raw_data = mmap.mmap(jsonl_file.fileno(), length=0, access=mmap.ACCESS_READ)
        self.ids = []
        self.texts = []
        self.tokens = []
        self.build()

    def build(self):
        pbar = tqdm(total=100., desc='Reading data', unit='%')
        self.raw_data.seek(0)
        total_size = self.raw_data.size()
        while True:
            line = self.raw_data.readline()
            if not line:
                break
            sample = json.loads(line)
            self.ids.append(sample['_id'])
            self.texts.append(self.process_text(sample['text']))
            self.tokens.append(self.process_token(sample['tokens']))
            pbar.update(round(self.raw_data.tell() / total_size * 100, 2) - pbar.n)

        tqdm.write(f'Read from {self.jsonl_path}, total {len(self.ids)} samples.')

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, index: int):
        return self.ids[index], self.texts[index], self.tokens[index]

    def get_texts(self, index: int | list[int] | None = None):
        if index is None:
            return self.texts
        elif isinstance(index, int):
            return self.texts[index]
        else:
            return [self.texts[i] for i in index]

    def get_tokens(self, index: int | list[int] | None = None):
        if index is None:
            return self.tokens
        elif isinstance(index, int):
            return self.tokens[index]
        else:
            return [self.tokens[i] for i in index]

    def get_ids(self, index: int | list[int] | None = None):
        if index is None:
            return self.ids
        elif isinstance(index, int):
            return self.ids[index]
        else:
            return [self.ids[i] for i in index]

    @staticmethod
    def process_text(text: str):
        return text.lower().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()

    @staticmethod
    def process_token(tokens: str):
        return tokens.replace('|', ' ').replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()


if __name__ == '__main__':
    dataset = TweetsDataSet('data/tweets_geo_merged.jsonl')
