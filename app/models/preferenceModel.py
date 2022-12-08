from flask import current_app as app

# __uid__, __pid__, like_dislike
class PreferenceModel:
    def __init__(self, uid, pid, product_name, like_dislike, time_created):
        self.uid = uid
        self.pid = pid
        self.product_name = product_name
        self.like_dislike = like_dislike
        self.time_created = time_created

    # This method retrieves all reviews, whether fresh or rotten carrots, for user
    # with the given uid.
    @staticmethod
    def get_all_reviews(uid):
        rows = app.db.execute('''
SELECT uid, pid, like_dislike, time_created
FROM Preferences
WHERE uid = :uid
''',
                              uid=uid)
        return [PreferenceModel(*row) for row in rows]
    
    # This method retrieves the 5 most recent FRESH carrots (likes) for the user with the given uid.
    # It returns the uid, pid, product name, like or dislike boolean, and the time of creation for each
    # freshy carrot review.

    @staticmethod
    def get_5_recent_fresh_by_uid(uid):
        rows = app.db.execute('''
SELECT Pref.uid, Pref.pid, Prod.name, Pref.like_dislike, Pref.time_created
FROM Preferences AS Pref, Products AS Prod
WHERE Pref.uid = :uid 
AND Pref.like_dislike = True 
AND Pref.pid = Prod.id
ORDER BY Pref.time_created DESC
limit 5
''',
                              uid=uid)
        return [PreferenceModel(*row) for row in rows]

    # This method retrieves the 5 most recent ROTTEN carrots (dislikes) for the user with the given uid.
    # It returns the uid, pid, product name, like or dislike boolean, and the time of creation for each
    # freshy carrot review.
    @staticmethod
    def get_5_recent_rotten_by_uid(uid):
        rows = app.db.execute('''
SELECT Preferences.uid, Preferences.pid, Products.name, Preferences.like_dislike, Preferences.time_created
FROM Preferences, Products
WHERE Preferences.uid = :uid 
AND Preferences.like_dislike = False 
AND Preferences.pid = Products.id
ORDER BY Preferences.time_created DESC
limit 5
''',
                              uid=uid)
        return [PreferenceModel(*row) for row in rows]

    # This method retrieves the review by the given user
    # for the given product, as well as product name from Products table
    @staticmethod
    def get_product_review(uid,pid):
        rows = app.db.execute('''
SELECT Preferences.uid, Preferences.pid, Products.name, Preferences.like_dislike, Preferences.time_created
FROM Preferences, Products
WHERE Preferences.uid = :uid 
AND Preferences.pid = :pid
AND Preferences.pid = Products.id
''', uid=uid, pid = pid)
        return [PreferenceModel(*row) for row in rows]

    #This method adds the user's preference/review
    #for the given product
    @staticmethod
    def insert(uid, pid, like_dislike):
        try:
            rows = app.db.execute("""
INSERT INTO Preferences(uid, pid, like_dislike)
VALUES(:uid, :pid, :like_dislike)
RETURNING uid, pid
""",
                                  uid=uid,
                                  pid=pid,
                                  like_dislike=like_dislike)
            uid1 = rows[0][0]
            pid1 = rows[0][1]
            return PreferenceModel.get_product_review(uid1,pid1)
        except Exception as e:
            # likely issue with product already reviewed
            print(str(e))
        try:
            rows = app.db.execute("""
UPDATE Preferences
SET like_dislike = :like_dislike
WHERE uid = :uid
AND pid = :pid
RETURNING uid, pid
""",
                                  uid=uid,
                                  pid=pid,
                                  like_dislike=like_dislike)
            uid1 = rows[0][0]
            pid1 = rows[0][1]
            return PreferenceModel.get_product_review(uid1,pid1)
        except Exception as e:
            print(str(e))
            return None

