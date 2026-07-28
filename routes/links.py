from flask import Blueprint, render_template, session, redirect, request, jsonify
from bson import ObjectId
from models.links import links

links_bp = Blueprint("links", __name__)


@links_bp.route("/links")
def all_links():

    if "user_id" not in session:
        return redirect("/login")

    user_links = list(
        links.find(
            {"user_id": session["user_id"]}
        ).sort("created_at", -1)
    )

    return render_template(
        "links.html",
        links=user_links
    )


@links_bp.route("/delete-link/<link_id>", methods=["POST"])
def delete_link():

    if "user_id" not in session:
        return jsonify({"success": False})

    link_id = request.view_args["link_id"]

    links.delete_one({
        "_id": ObjectId(link_id),
        "user_id": session["user_id"]
    })

    return jsonify({
        "success": True
    })
