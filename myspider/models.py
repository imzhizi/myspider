# 需要事先运行 DoubanModel.init() 以初始化 es
from elasticsearch_dsl import connections, Document, Text, analyzer, Completion, Double

connections.create_connection(hosts=['127.0.0.1'])


class DoubanModel(Document):
    title = Text(
        analyzer=analyzer('ik_max_word'),
        fields={
            'suggest': Completion(
                analyzer=analyzer('ik_max_word')
            ),
        }
    )

    douban_link = Text()
    rating = Double()

    class Index:
        name = 'xingren'
        settings = {
            "number_of_shards": 3,
        }
