from root import app
from waitress import server

if __name__ == '__main__':
    # application.run(debug=True)
    serve(app, host='0.0.0.0', port=5000)
