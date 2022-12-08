from flask import current_app as app

#exception handling
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

# __uid__, cart_name, time_started
# name of current cart user is working on
class CartModel:
    def __init__(self, uid, cart_name, time_started):
        self.uid = uid
        self.cart_name = cart_name
        self.time_started = time_started

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT uid, cart_name, time_started
FROM Carts
WHERE uid = :uid
''',
                              uid=uid)
        return [CartModel(*row) for row in rows]
    
    @staticmethod
    def startCart(uid, cart_name, time_started):
        try:
            rows = app.db.execute('''
INSERT INTO Carts(uid, cart_name, time_started)
VALUES(:uid, :cart_name, :time_started)
''', 
                                uid=uid,
                                cart_name=cart_name,
                                time_started=time_started)
        except IntegrityError as e:
            assert isinstance(e.orig, UniqueViolation)
        finally:
            print(str(Exception))

    @staticmethod
    def clearCart(uid):
        app.db.execute("""
DELETE FROM Carts
WHERE Carts.uid = :uid
""",
                                uid=uid)


# __uid__, product_name
# list of things user wants to buy
class CartListModel:
    def __init__(self, uid, product_name):
        self.uid = uid
        self.product_name = product_name
    
    @staticmethod
    def get(uid):
        rows = app.db.execute("""
SELECT uid, product_name
FROM CartLists
WHERE uid = :uid
""",
                                uid=uid)
        return [CartListModel(*row) for row in rows]
    
    @staticmethod
    def addToCartList(uid, product_name):
        app.db.execute("""
INSERT INTO CartLists(uid, product_name)
VALUES(:uid, :product_name)
""",
                                uid=uid,
                                product_name=product_name)
    
    @staticmethod
    def clearCartList(uid):
        app.db.execute("""
DELETE FROM CartLists
WHERE CartLists.uid = :uid
""",
                                uid=uid)


# __uid__, __pid__, quantity
# exact pids user will buy
class CartContentsModel:
    def __init__(self, uid, pid, quantity):
        self.uid = uid
        self.pid = pid
        self.quantity = quantity

    @staticmethod
    def get(uid):
        rows = app.db.execute("""
SELECT uid, pid, quantity
FROM CartContents
WHERE uid = :uid
""",
                                uid=uid)
        return [CartContentsModel(*row) for row in rows]

    @staticmethod
    def insert(uid, pid, quantity=1):
        try:
            app.db.execute("""
INSERT INTO CartContents(uid, pid, quantity)
VALUES(:uid, :pid, :quantity)
""",
                                uid=uid,
                                pid=pid,
                                quantity=quantity)
        except Exception as e:
            # product may already be in cart
            print(str(e))
            return None

    @staticmethod
    def clearCartContents(uid):
        app.db.execute("""
DELETE FROM CartContents
WHERE CartContents.uid = :uid
""",
                                uid=uid)