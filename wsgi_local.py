from waitress import serve
from app.root import app
serve(app, host='0.0.0.0', port=8080)