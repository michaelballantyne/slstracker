from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from slstracker.model import Model
import os, sys, ConfigParser

path = os.path.abspath(os.path.dirname(sys.argv[0]))
config_filename = os.path.join(path, 'tracker.cfg')

config = ConfigParser.RawConfigParser()
config.read(config_filename)

class App(Flask):
    def dispatch_request(self):
        t = engine.contextual_connect().begin()
        try: 
            rv = super(App, self).dispatch_request()
            t.commit()
            return rv
        except:
            t.rollback()
            raise

app = App(__name__)
app.secret_key="dfjasld1r9sdj5w0gsldjd6rezg0fx"
app.debug = True

connection_string = 'postgresql+psycopg2://%s:%s@%s:%d/%s' % (config.get('db', 'username'), config.get('db', 'password'), config.get('db', 'host'), config.getint('db', 'port'), config.get('db', 'database'))

engine = create_engine(connection_string, echo=config.getboolean('db', 'echosql'), strategy='threadlocal', convert_unicode=True)

meta = MetaData()
meta.bind = engine
meta.reflect()

model = Model(meta)

import slstracker.controller
