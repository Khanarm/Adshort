from flask import Blueprint, render_template, session, redirect
from bson import ObjectId
from mongo import db

links_bp = Blueprint("links", __name__)
