from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from slstracker.model import Model

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

app = App(__name__, instance_relative_config=True)
app.debug = True
app.config.from_pyfile('application.cfg')
print app.instance_path

connection_string = 'postgresql+psycopg2://%s:%s@%s:%d/%s' % (app.config['DB_USERNAME'], app.config['DB_PASSWORD'], app.config['DB_HOST'], app.config['DB_PORT'], app.config['DB_DATABASE'])

engine = create_engine(connection_string, echo=app.config['DB_ECHOSQL'], strategy='threadlocal', convert_unicode=True)

meta = MetaData()
meta.bind = engine
meta.reflect()

model = Model(meta)

import slstracker.controller
