import datetime
from flask import current_app as app

# __id__, name, price, category, store, last_update
class ProductModel:
    def __init__(self, id, name, price, category, store, last_update):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.store = store
        self.last_update = last_update

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, category, store, last_update
FROM Products
WHERE id = :id
''',
                                id=id)
        return ProductModel(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_by_feature(name, minprice, maxprice,category,store):
        rows = app.db.execute('''
SELECT id, name, price, category, store, last_update
FROM Products
WHERE name LIKE :name and price >= :minprice and price <= :maxprice and category =:category and store = :store

''',
                                name='%'+name+'%',
                                minprice=minprice,
                                maxprice=maxprice,
                                category=category,
                                store=store)
        return [ProductModel(*row) for row in rows]
    @staticmethod 
    def get_all_categories(since=datetime.datetime(2022, 10, 1, 0, 0, 0)):
        rows = app.db.execute('''
SELECT DISTINCT category
FROM Products
WHERE last_update >= :since
''',
                                since=since)
        return [ProductModel(*row) for row in rows]
    def search_by_name(name):
        rows = app.db.execute('''
SELECT id, name, price, category, store, last_update
FROM Products
WHERE name LIKE :name
''',
                                name='%'+name+'%')
        return [ProductModel(*row) for row in rows] if rows is not None else None

    @staticmethod
    def get_all(since=datetime.datetime(2022, 10, 1, 0, 0, 0)):
        rows = app.db.execute('''
SELECT id, name, price, category, store, last_update
FROM Products
WHERE last_update >= :since
''',
                                since=since)
        return [ProductModel(*row) for row in rows]

    @staticmethod
    def getKMostExpensive(k):
        rows = app.db.execute('''
SELECT id, name, price, category, store, last_update
FROM Products
ORDER BY price DESC
''')    
        i = 0
        productList = []
        while i < int(k):
            productList.append(ProductModel(*(rows[i])))
            i += 1
        return productList

