from flask import current_app as app

# __uid__, __pid__, quantity
class Cart:
    """
    This is just a TEMPLATE for Cart, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, uid, pid, quantity):
        self.uid = uid
        self.pid = pid
        self.quantity = quantity

    @staticmethod
    def get(uid):
        rows = app.db.execute('''
SELECT uid, pid, quantity
FROM Carts
WHERE uid = :uid
''',
                              uid=uid)
        return [Cart(*row) for row in rows]