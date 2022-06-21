import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

pg_engine = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
    user=os.getenv('POSTGRES_USER', 'merchant_api'),
    password=os.getenv('POSTGRES_PASSWORD', 'merchant_api'),
    host=os.getenv('POSTGRES_HOST', 'merchant_api'),
    port=os.getenv('POSTGRES_PORT', 'merchant_api'),
    db=os.getenv('POSTGRES_DB', 'merchant_api')
)

Base = automap_base()
engine = create_engine(pg_engine)
Base.prepare(engine, reflect=True)

Payment = Base.classes.payment_requests_paymentrequest

session = Session(engine)
