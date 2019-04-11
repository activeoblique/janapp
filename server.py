import os, time
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, Response, render_template, jsonify, request, g, redirect

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.debug = True

DATABASEURI = "postgresql://jana:4001@localhost"
