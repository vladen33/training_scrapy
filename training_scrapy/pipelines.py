from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()

class Quote(Base):
    __tablename__ = 'quote'
    id = Column(Integer, primary_key=True)
    text = Column(Text())
    author = Column(String(200))
    tags = Column(String(400))

class TrainingScrapyPipeline:
    def process_item(self, item, spider):
        return item

class QuotesToDBPipeline:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db', echo=True)
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        quote = Quote(
            text=item['text'],
            author=item['author'],
            tags=', '.join(item['tags'])
        )
        # print('========================================', quote)
        self.session.add(quote)
        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
