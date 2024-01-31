from itemadapter import ItemAdapter
import mysql.connector
import os

class ScrapingPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip all whitespaces
        for field_name in adapter.field_names():
            if field_name != 'strategy':
                value = adapter.get(field_name)
                if value and value[0] is not None:
                    adapter[field_name] = value[0].strip()
                else:
                    adapter[field_name] = None

        # Converting tags to normal case (first symbol is upper and others are lower)
        field_name = 'tags'
        value = adapter.get(field_name)
        if value is not None:
            if ',' in value:
                values = value.split(',')
                values = [value.strip() for value in values]
                adapter[field_name] = ', '.join([f'{word[0].upper()}{word[1:].lower()}' for word in values])
            else:
                adapter[field_name] = value[0].upper() + value[1:].lower()

        # Dealing with numbers
        field_name = 'invest'
        value = adapter.get(field_name)
        if value is not None:
            value = value.replace('$', '')
            if 'M' not in value:
                result = f'{float(float(value) / 10 ** 6):.2f}'
                result = result.rstrip("0") if result[-1] == '0' else result
                result = result.replace(".", "") if result[-1] == '.' else result
                adapter[field_name] = f'{result}M'
            else:
                adapter[field_name] = value

        return item

class SaveToMySQLPipeline:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv("MySQLPass"),
            database='dropshub'
        )

        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alphadrops(
                id int NOT NULL auto_increment,
                title TEXT,
                tags VARCHAR(255),
                invest TEXT,
                network VARCHAR(255),
                status TEXT,
                description VARCHAR(255),
                strategy VARCHAR(255),
                website VARCHAR(255),
                discord VARCHAR(255),
                logo VARCHAR(255),
                PRIMARY KEY (id)
                ) 
        """)

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO alphadrops(
                title,
                tags,
                invest,
                network,
                status,
                description,
                strategy,
                website,
                discord,
                logo
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )""", (
            item['title'],
            item['tags'],
            item['invest'],
            item['network'],
            item['status'],
            item['description'],
            item['strategy'],
            item['website'],
            item['discord'],
            item['logo'],
        ))

        self.connection.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
