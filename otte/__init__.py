from flask import (Flask, g, request, session, redirect,
        url_for, render_template, jsonify)
from flask_script import Manager
import redis
import os
from OurTime2Eat.otte import config as config_file

app = Flask(__name__,
        template_folder=os.getenv('OTTE_TEMPLATES'),
        static_folder=os.getenv('OTTE_STATIC'))
app.config.from_object(config_file)

def get_db():
    if not hasattr(g, 'redis'):
        g.redis = redis.StrictRedis(**app.config['REDIS'])
    return g.redis

### VIEWS

@app.route('/')
def home():
    '''
    index.html
    '''
    return render_template('index.html')


### END OF VIEWS

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
