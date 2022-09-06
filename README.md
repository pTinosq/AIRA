# AIFA
> Argumentation Is F***ing Awesome

## What is AIFA?
AIFA is a web platform used to demonstrate a variety of argumentation methods currently being researched by Nico Potyka at Imperial College London.
The original Uncertainpy argumentation library was built with Java and is available for download on its [sourceforge page](https://sourceforge.net/projects/attractorproject/).

## Running locally
I suggest using waitress to host the Flask project locally.

`pip install waitress`

Create a new wsgi (wsgi_local.py) for local testing in the root folder.

```
from waitress import serve
from app.root import app
serve(app, host='0.0.0.0', port=8080)
```

Run the new local wsgi script

`python wsgi_local.py`

## Image showcase

![BAG Editor - Home page](https://i.imgur.com/TVJUyN2.png "BAG Editor - Home page")
![Line graph viewer](https://i.imgur.com/bWyT5Dp.png "Line graph viewer")
![Node graph viewer](https://i.imgur.com/rFUuhL0.png "Node graph viewer")
![Verbose output viewer](https://i.imgur.com/8qrrn38.png "Verbose output viewer")
