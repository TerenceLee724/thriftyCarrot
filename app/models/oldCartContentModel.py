from flask import current_app as app

# model
# __cid__, __pid__, product_name, price, category, store, quantity
class OldCartContentModel:
    def __init__(self, cid, pid, product_name, price, category, store, quantity=1):
        self.cid = cid
        self.pid = pid
        self.product_name = product_name
        self.price = price
        self.category = category
        self.store = store
        self.quantity = quantity

    @staticmethod
    def get(cid):
        rows = app.db.execute('''
SELECT cid, pid, product_name, price, category, store, quantity
FROM OldCartContents
WHERE cid = :cid
''',
                              cid=cid)
        return OldCartContentModel(*(rows[0])) if rows else None
    @staticmethod
    def get_count_by_category(uid):
        rows = app.db.execute('''
SELECT COUNT(Cart.cid), COUNT(Contents.pid), COUNT(Contents.product_name), SUM(Contents.price), Contents.category, COUNT(Contents.store), SUM(Contents.quantity)
FROM OldCartContents AS Contents, OldCarts AS Cart
WHERE Cart.uid = :uid
AND Cart.cid = Contents.cid
GROUP BY category
''',
                              uid=uid)
        return [OldCartContentModel(*row) for row in rows]

    @staticmethod
    def get_last_cart_prices(uid):
        rows = app.db.execute('''
SELECT COUNT(Cart.cid), COUNT(Contents.pid), MIN(Contents.product_name), SUM(Contents.price), COUNT(Contents.category), COUNT(Contents.store), SUM(Contents.quantity)
FROM OldCartContents AS Contents, OldCarts AS Cart
WHERE Cart.uid = :uid
AND Contents.cid = (SELECT cid
    FROM OldCarts
    WHERE uid = :uid
    ORDER BY time_created DESC
    limit 1)
GROUP BY pid
''',
                              uid=uid)
        return [OldCartContentModel(*row) for row in rows]
    @staticmethod
    def get_most_recent_by_uid(uid):
        rows = app.db.execute('''
SELECT Cart.cid, Contents.pid, Contents.product_name, Contents.price, Contents.category, Contents.store, Contents.quantity
FROM OldCartContents AS Contents, OldCarts AS Cart
WHERE Cart.uid = :uid
AND Cart.cid = Contents.cid
ORDER BY time_created DESC
''',
                              uid=uid)
        return [OldCartContentModel(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT Cart.cid, Contents.pid, Contents.product_name, Contents.price, Contents.category, Contents.store, Contents.quantity
FROM OldCartContents AS Contents, OldCarts AS Cart
WHERE Cart.uid = :uid
AND Cart.time_created >= :since
AND Cart.cid = Contents.cid
ORDER BY time_created DESC
''',
                              uid=uid,
                              since=since)
        return [OldCartContentModel(*row) for row in rows]

    @staticmethod
    def get_all_oldcartcontent_by_uid(uid):
        rows = app.db.execute('''
WITH AllOldCarts AS
(SELECT cid
FROM OldCarts
WHERE uid = :uid
ORDER BY time_created DESC)
SELECT Contents.cid, Contents.pid, Contents.product_name, Contents.price, Contents.category, Contents.store, Contents.quantity
FROM OldCartContents AS Contents, AllOldCarts
WHERE AllOldCarts.cid = Contents.cid
''',
                              uid=uid)        
        return [OldCartContentModel(*row) for row in rows]

    @staticmethod
    def get_content_of_recent_three_by_uid(uid):
        rows = app.db.execute('''
WITH RecentThree AS
(SELECT cid
FROM OldCarts
WHERE uid = :uid
ORDER BY time_created DESC
limit 3)
SELECT Contents.cid, Contents.pid, Contents.product_name, Contents.price, Contents.category, Contents.store, Contents.quantity
FROM OldCartContents AS Contents, RecentThree
WHERE RecentThree.cid = Contents.cid
''',
                              uid=uid)        
        return [OldCartContentModel(*row) for row in rows]

    @staticmethod
    def insert(cid, pid, product_name, price, category, store, quantity=1):
        try:
            app.db.execute("""
INSERT INTO OldCartContents(cid, pid, product_name, price, category, store, quantity)
VALUES(:cid, :pid, :product_name, :price, :category, :store, :quantity)
""",
                                cid=cid,
                                pid=pid, 
                                product_name=product_name, 
                                price=price, 
                                category=category, 
                                store=store,
                                quantity=quantity)
        except Exception as e:
            print(str(e))
            return None
