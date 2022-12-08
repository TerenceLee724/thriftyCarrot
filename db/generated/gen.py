from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random

num_users = 100
num_products = 2000
num_preferences = 500
num_itemsInCart = 1000
num_carts = 50
num_oldCarts = 500

Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

# __id__, email, password, firstname, lastname, birthdate, joindate
def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            birthdate = profile['birthdate']
            joindate = str(random.randrange(2021,2023)) + '-' + str(random.randrange(1,13)) + '-' + str(random.randrange(1,29))
            writer.writerow([uid, email, password, firstname, lastname, birthdate, joindate])
        print(f'{num_users} generated')
    return

stores = ["Trader Joes", "Whole Foods", "Harris Teeters"]
categories = ["Baked Goods", "Bread", "Produce", "Cheese", "Dairy & Eggs", "Sauces", "Prepared Food", "Frozen Food", "Produce", "Meat", "Seafood", "Baking", "Pantry", "Canned Goods", "Beverages"]
# __id__, name, price, category, store, last_update
def gen_products(num_products):
    products = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=50))}.{fake.random_int(max=99):02}'
            last_update = fake.date_time_between('-2w')
            category = random.choice(categories)
            store = random.choice(stores)
            writer.writerow([pid, name, price, category, store, last_update])
            products.append([pid, name, price, category, store, last_update])
        print(f'{num_products} generated;')
    return products

# __uid__, __pid__, like_dislike
def gen_preferences(num_preferences):
    with open('Preferences.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Preferences...', end=' ', flush=True)
        counter = 0
        # Generates list of random users of random length
        randomUserList = random.sample(range(0, num_users), random.randint(0, num_users))
        for i in range(min(len(randomUserList), num_preferences)):
            if(counter>=num_preferences): break
            uid = randomUserList[i]
            # Generates list of random products user dislikes
            randomProductList = random.sample(range(0, num_products), random.randint(0, 50))
            for j in randomProductList:
                if(counter>=num_preferences): break
                pid = j
                like_dislike = random.choice([True, False])
                time_created = fake.date_time()
                writer.writerow([uid, pid, like_dislike, time_created])
                counter += 1
        print(f'{num_preferences} generated;')
    return

# __uid__, cart_name, time_started
def gen_carts(num_carts):
    with open('Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush=True)
        randomUserList = random.sample(range(0, num_users), k=num_carts)
        for i in range(num_carts):
            if i % 100 == 0:
                print(f'{i}', end=' ', flush=True)
            uid = randomUserList[i]
            cart_name = fake.sentence(nb_words=2)[:-1]
            time_started = fake.date_time()
            writer.writerow([uid, cart_name, time_started])
        print(f'{num_carts} generated')
    return

# __uid__, product_name
def gen_cartLists(num_itemsInCart):
    with open('CartLists.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('CartLists...', end=' ', flush=True)
        counter = 0
        # Generates list of random users of random length
        randomUserList = random.sample(range(0, num_users), random.randint(0, num_users))
        for i in range(min(len(randomUserList), num_itemsInCart)):
            if(counter>=num_itemsInCart): break
            uid = randomUserList[i]
            # random number of items in current cart
            for j in range(0, random.randint(0, 20)):
                if(counter>=num_itemsInCart): break
                product_name = fake.sentence(nb_words=2)[:-1]
                writer.writerow([uid, product_name])
                counter += 1
        print(f'{counter} generated;')
    return

# __uid__, __pid__, quantity
def gen_cartContents(num_itemsInCart):
    with open('CartContents.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('CartContents...', end=' ', flush=True)
        counter = 0
        # Generates list of random users of random length
        randomUserList = random.sample(range(0, num_users), random.randint(0, num_users))
        for i in range(min(len(randomUserList), num_itemsInCart)):
            if(counter>=num_itemsInCart): break
            uid = randomUserList[i]
            # Generates list of random products user has in cart
            randomProductList = random.sample(range(0, num_products), random.randint(0, 50))
            for j in randomProductList:
                if(counter>=num_itemsInCart): break
                pid = j
                qt = random.randint(0, 20)
                writer.writerow([uid, pid, qt])
                counter += 1
        print(f'{counter} generated;')
    return

# __cid__, uid, cart_name, time_created
def gen_oldCarts(num_oldCarts):
    with open('OldCarts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('OldCarts...', end=' ', flush=True)
        for cid in range(num_oldCarts):
            if cid % 100 == 0:
                print(f'{cid}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            cart_name = fake.sentence(nb_words=2)[:-1]
            time_created = fake.date_time()
            writer.writerow([cid, uid, cart_name, time_created])
        print(f'{num_oldCarts} generated')
    return

# __cid__, __pid__, product_name, price, category, store, quantity
def gen_oldCartContent(num_carts, products):
    with open('OldCartContent.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('OldCartContents...', end=' ', flush=True)
        counter = 0
        for cid in range(num_carts):
            # Generates list of random products user placed in cart
            randomProductList = random.sample(range(0, num_products), random.randint(1, 25))
            for j in randomProductList:
                pid = j
                product_name = products[j][1]
                price = products[j][2]
                category = products[j][3]
                store = products[j][4]
                qt = random.randint(1, 20)
                writer.writerow([cid, pid, product_name, price, category, store, qt])
                counter += 1
        print(f'{counter} generated;')
    return

# users
# gen_users(num_users)
# products
products = gen_products(num_products)
# # preferences
# gen_preferences(num_preferences)
# # current carts
# gen_carts(num_carts)
# gen_cartLists(num_itemsInCart)
# gen_cartContents(num_itemsInCart)
# old carts
gen_oldCarts(num_oldCarts)
gen_oldCartContent(num_oldCarts, products)
