#! /bin/bash

python -m webbrowser http://localhost:8000/mains/index.html
python -m http.server --cgi 8000

