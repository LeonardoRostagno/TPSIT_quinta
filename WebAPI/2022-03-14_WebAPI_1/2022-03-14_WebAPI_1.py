import flask as fl

app = fl.Flask(__name__)
app.config["DEBUG"] = True

books = [
    {'id':0, 'title':'Il Nome della Rosa', 'author':'Umberto Eco', 'year_published':'1980'},
    {'id':1, 'title':'Il Problema dei 3 Corpi', 'author':'Liu Cixin', 'year_published':'2008'},
    {'id':2, 'title':'Fondazione', 'author':'Isaac Asimov', 'year_published':'1951'}
]

@app.route('/', methods = ['GET'])
def home():
    return "<h1>Biblioteca onLine</h1><p>Prototipo di WebAPI.</p>"

@app.route('/api/v1/resources/books/all', methods = ['GET'])
def api_all():
    return fl.jsonify(books)

@app.route('/api/v1/resources/books', methods = ['GET'])
def api_id():
    if 'id' in fl.request.args:
        id = int(fl.request.args['id'])
    else:
        return "ERROR: No ID field provided. Please specify"
    
    results = []

    for book in books:
        if book['id'] == id:
            results.append(book)

    return fl.jsonify(results)

app.run()