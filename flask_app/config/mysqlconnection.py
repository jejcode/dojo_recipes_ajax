import pymysql.cursors # import cursor to interact with database

class MySQLConnection: # we will create an instance of the connection to the database
    def __init__(self, db) -> None:
        connection = pymysql.connect(host = 'localhost',
                                     user = 'root',
                                     password = 'rootroot',
                                     db = db,
                                     charset = 'utf8',
                                     cursorclass = pymysql.cursors.DictCursor,
                                     autocommit = False)
        # establish connection with database
        self.connection = connection
    # the method to query the database
    def query_db(self, query:str, data:dict=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query)
                if query.lower().find('insert') >=0:
                    # INSERT queries will return the ID NUMBER of inserted row
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find('select') >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE AND DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                #if the query fails the method will return False
                print('Something went wrong.', e)
                return False
            finally:
                # close the connection
                self.connection.close()
# connectToMySQL receives the database we're using and uses it to create an instance of the class
def connectToMySQL(db):
    return MySQLConnection(db)
