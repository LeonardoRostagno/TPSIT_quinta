import flask as fl
import sqlite3

app = fl.Flask(__name__)
app.config["DEBUG"] = True

connection = sqlite3.connect('./database.db') 
cursor = connection.cursor()
books = cursor.execute("SELECT * FROM Books").fetchall()
connection.close()

@app.route('/', methods = ['GET'])
def home():
    return "<h1>Biblioteca onLine</h1><p>Prototipo di WebAPI.</p>"

@app.route('/api/v1/resources/books/all', methods = ['GET'])
def api_all():
    return fl.jsonify(books)

@app.route('/api/v1/resources/books/id', methods = ['GET'])
def api_id(): # ricerca per ID
    if 'id' in fl.request.args:
        id = int(fl.request.args['id'])
    else:
        return "ERROR: No ID field provided. Please specify"

    connection = sqlite3.connect('./database.db') 
    cursor = connection.cursor()
    book_id = cursor.execute(f"SELECT * FROM Books WHERE id = {id}").fetchall()
    connection.close()

    return fl.jsonify(book_id)

@app.route('/api/v1/resources/books/title', methods=['GET'])
def api_title(): # ricerca per title
    if 'title' in fl.request.args:
        title = fl.request.args['title']
    else:
        return "ERROR: No TITLE field provided. Please specify"

    connection = sqlite3.connect('./database.db') 
    cursor = connection.cursor()
    book_title = cursor.execute(f"SELECT * FROM Books WHERE title = '{title}'").fetchall()
    connection.close()

    return fl.jsonify(book_title)

app.run()