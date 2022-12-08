from flask import current_app as app

# model
# __cid__, uid, time_created, cart_name
class OldCartModel:
    def __init__(self, cid, uid, cart_name, time_created):
        self.cid = cid
        self.uid = uid
        self.cart_name = cart_name
        self.time_created = time_created

    @staticmethod
    def get(cid):
        rows = app.db.execute('''
SELECT cid, uid, cart_name, time_created
FROM OldCarts
WHERE cid = :cid
''',
                              cid=cid)
        return OldCartModel(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT cid, uid, cart_name, time_created
FROM OldCarts
WHERE uid = :uid
ORDER BY time_created DESC
''',
                              uid=uid)
        return [OldCartModel(*row) for row in rows]

    @staticmethod
    def get_recent_three_by_uid(uid):
        rows = app.db.execute('''
SELECT cid, uid, cart_name, time_created
FROM OldCarts
WHERE uid = :uid
ORDER BY time_created DESC
limit 3
''',
                              uid=uid)        
        return [OldCartModel(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT cid, uid, cart_name, time_created
FROM OldCarts
WHERE uid = :uid
AND time_created >= :since
ORDER BY time_created DESC
''',
                              uid=uid,
                              since=since)
        return [OldCartModel(*row) for row in rows]

# __cid__, uid, time_created, cart_name
    @staticmethod
    def insert(uid, cart_name):
        try:
            rows = app.db.execute("""
INSERT INTO OldCarts(uid, cart_name)
VALUES(:uid, :cart_name)
RETURNING cid
""",
                                uid=uid,
                                cart_name=cart_name)
            cid = rows[0][0]
            return cid
        except Exception as e:
            # product may already be in cart
            print(str(e))
            return None