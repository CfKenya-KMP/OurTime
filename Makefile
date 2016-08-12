testserver:
	compass compile && flask -a otte --debug run --port=5040

runserver:
	compass compile && gunicorn --workers 3 --bind unix:otte.sock --log-level debug --log-file logs/gunicorn.log core:app &
