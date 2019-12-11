import sqlite3
import numpy as np


class DBWebShop:
    def __init__(self, filename):
        self.filename = filename

    def create_db(self):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        curs.execute('''CREATE TABLE goods
            (   id integer PRIMARY KEY,
                name text,
                price FLOAT,
                categoryID integer,
                description text, 
                params text, 
                photos text,
                FOREIGN KEY (categoryID) REFERENCES categories (categoryID))''')

    def create_categories_db(self):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        curs.execute('''CREATE TABLE categories
            ( name text,
              categoryID integer PRIMARY KEY)''')

    @staticmethod
    def convert_to_binary_data(filename):
        with open(filename, 'rb') as file:
            blob_data = file.read()
        return blob_data

    def create_new_category(self, name):
        try:
            sqlite_connection = sqlite3.connect(self.filename)
            cursor = sqlite_connection.cursor()
            print("Connected to SQLite")
            sqlite_insert_query = """ INSERT INTO categories (name)
                                          VALUES (?)"""
            data_tuple = (name,)
            cursor.execute(sqlite_insert_query, data_tuple)
            sqlite_connection.commit()
            print("Image and file inserted successfully as a BLOB into a table")
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to insert blob data into sqlite table", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("the sqlite connection is closed")

    def insert_new(self, name, price, category, description, params, photos):
        try:
            sqlite_connection = sqlite3.connect(self.filename)
            cursor = sqlite_connection.cursor()
            cursor.execute("PRAGMA foreign_keys = 1")
            print("Connected to SQLite")
            sqlite_insert_blob_query = """ INSERT INTO goods (name, price, categoryID, description, params, photos)
                                          VALUES (?, ?, ?, ?, ?, ?)"""
            #photo = self.convert_to_binary_data(photos)
            data_tuple = (name, price, category, description, params, photos)
            cursor.execute(sqlite_insert_blob_query, data_tuple)
            sqlite_connection.commit()
            print("Image and file inserted successfully as a BLOB into a table")
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to insert blob data into sqlite table", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("the sqlite connection is closed")

    def clear_element_by_name(self, art_param):
        try:
            sqlite_connection = sqlite3.connect(self.filename)
            cursor = sqlite_connection.cursor()
            print("Connected to SQLite")
            delete_smth = """ DELETE FROM goods
                                          WHERE name = ?"""
            cursor.execute(delete_smth, (art_param,))
            sqlite_connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print(error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("the sqlite connection is closed")

    def category_search(self, cat_name):
        try:
            sqlite_connection = sqlite3.connect(self.filename)
            cursor = sqlite_connection.cursor()
            cursor.execute("PRAGMA case_sensitive_like = 0")
            find_category = """ SELECT goods.id, goods.name, goods.price, categories.name, 
                                       goods.description, goods.params, goods.photos
                                FROM goods, categories
                                WHERE categories.name LIKE ? AND categories.categoryID = goods.categoryID"""
            cursor.execute(find_category, ("%"+cat_name+"%", ))
            rows = cursor.fetchall()
            sqlite_connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print(error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                return rows

    def name_search(self, art_name):
        try:
            sqlite_connection = sqlite3.connect(self.filename)
            cursor = sqlite_connection.cursor()
            print("Connected to SQLite")
            find_article = """ SELECT goods.id, goods.name, goods.price, categories.name, 
                                      goods.description, goods.params, goods.photos
                                FROM goods, categories
                                WHERE goods.name LIKE ? AND goods.categoryID = categories.categoryID"""
            cursor.execute(find_article, ("%"+art_name+"%", ))
            rows = cursor.fetchall()
            sqlite_connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print(error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("the sqlite connection is closed")
            return rows

    def get_by_id(self, _id):
        try:
            sqlite_connection = sqlite3.connect(self.filename)
            cursor = sqlite_connection.cursor()
            print("Connected to SQLite")
            find_by_id = """ SELECT goods.name, goods.price
                             FROM goods
                             WHERE goods.id = ?"""
            cursor.execute(find_by_id, (_id, ))
            rows = cursor.fetchone()
            sqlite_connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print(error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("the sqlite connection is closed")
            return rows

    def get_table(self):
        try:
            sqlite_connection = sqlite3.connect(self.filename)
            cursor = sqlite_connection.cursor()
            cursor.execute("PRAGMA case_sensitive_like = 0")
            return_all = """SELECT g.id, g.name, g.price, c.name,
                            g.description, g.params, g.photos
                            FROM goods g, categories c
                            WHERE g.categoryID = c.categoryID"""
            cursor.execute(return_all)
            rows = cursor.fetchall()
            sqlite_connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print(error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
            return list(rows)


if __name__ == '__main__':
    dd = DBWebShop('shop.db')
    #dd.create_categories_db()
    #dd.create_db()
    #dd.create_new_category("Programming")
    #dd.insert_new("Auto 98", 100, 4, "oh god yes please", "Are you satisfied?", "ded-ulybaetsya-foto.jpg")
    #dd.insert_new("Test product2", np.random.randint(1000), 2, "something red", "not nice nice",
    #              "copy_karl_schwarz_41_9_5_10_5805e07a3446f_images_1766094338.jpg")
    #dd.insert_new("Test product4", np.random.randint(1000), 3, "something white", "don't buy it",
    #              "Kermit_the_Frog.jpg")
    #dd.clear_element_by_name("Гітара акустична")
    #dd.create_new_category("Струнні інструменти")
    #dd.category_search("test")

    #for r in dd.category_search("Духові інструменти"):
     #   print(r)
    #for i in dd.get_table():
    #    print(i)