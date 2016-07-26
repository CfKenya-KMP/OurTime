testserver:
	flask -a otte --debug run --port=5040

runserver:
	gunicorn --workers 3 --bind unix:otte.sock --log-level debug --log-file logs/gunicorn.log core:app &
