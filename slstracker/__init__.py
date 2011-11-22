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

app = App(__name__)

engine = create_engine('postgresql+psycopg2://slstracker:cce@localhost:5432/slstracker', echo=True, strategy='threadlocal', convert_unicode=True)

meta = MetaData()
meta.bind = engine
meta.reflect()

model = Model(meta)

import slstracker.controller
