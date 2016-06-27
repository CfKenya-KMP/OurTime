testserver:
	flask -a otte --debug run --port=5040

runserver:
	gunicorn -w 5 -b 0.0.0.0:5040 --log-level debug --log-file logs/gunicorn-otte.log core:app &
