from flask import Blueprint, render_template, request, session, redirect
from bson import ObjectId
from datetime import datetime
from mongo import db

report_bp = Blueprint("report", __name__)
