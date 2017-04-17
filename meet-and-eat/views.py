import string
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, g, request, jsonify, abort
from models import Base, User, Request, Proposal, MealDate


engine = create_engine('sqlite:///meetandeat.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
