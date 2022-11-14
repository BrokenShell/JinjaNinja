from os import getenv
from typing import Dict, Iterator

from bleach import clean
from pandas import DataFrame
from pymongo import MongoClient
from dotenv import load_dotenv
from certifi import where

from app.generator import RandomInput


class MongoDB:
    load_dotenv()
    collection = MongoClient(
        getenv("MONGO_URL"), tlsCAFile=where(),
    )["JinjaNina"]["Data"]

    def create(self, record: Dict):
        self.collection.insert_one(
            {k: clean(v, strip=True) for k, v in record.items()}
        )

    def read(self, query: Dict) -> Iterator[Dict]:
        return self.collection.find(query, {"_id": False})

    def dataframe(self) -> DataFrame:
        return DataFrame(self.read({}))

    def html_table(self) -> str:
        return self.dataframe().to_html()

    def reset(self):
        self.collection.delete_many({})

    def count(self) -> int:
        return self.collection.count_documents({})

    def seed(self, amount: int):
        self.collection.insert_many(vars(RandomInput()) for _ in range(amount))


if __name__ == '__main__':
    MongoDB().reset()
