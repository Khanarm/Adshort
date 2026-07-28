from flask import Blueprint, render_template, session, redirect
from bson import ObjectId
from mongo import db

history_bp = Blueprint("history", __name__)
