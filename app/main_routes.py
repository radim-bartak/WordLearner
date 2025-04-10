from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
import random
import base64
import io
import numpy as np
from PIL import Image
import os

from . import db
from .models import User
from .ml import predict_word_from_image, segment_letters_and_boxes


main_bp = Blueprint("main_bp", __name__)

def get_current_user():
    if "user_id" in session:
        return User.query.get(session["user_id"])
    return None

animals = [
    ("CAT", "cat.avif"),
    ("DOG", "dog.jpeg"),
    ("FISH", "fish.png"),
    ("BIRD", "bird.webp"),
    ("LION", "lion.jpg"),
    ("TIGER", "tiger.jpg"),
    ("ELEPHANT", "elephant.jpg"),
    ("BEAR", "bear.jpg"),
    ("HORSE", "horse.jpeg"),
    ("MONKEY", "monkey.jpg"),
    ("GIRAFFE", "giraffe.jpg"),
    ("ZEBRA", "zebra.jpg"),
    ("KANGAROO", "kangaroo.png"),
    ("PANDA", "panda.jpg"),
    ("SNAKE", "snake.png")
]

colors = [
    ("RED", "#FF0000"),
    ("GREEN", "#00FF00"),
    ("BLUE", "#0000FF"),
    ("YELLOW", "#FFFF00"),
    ("PURPLE", "#800080"),
    ("ORANGE", "#FFA500"),
    ("BLACK", "#000000"),
    ("PINK", "#FFC0CB"),
    ("BROWN", "#964B00")
]

fruits_vegetables = [
    ("APPLE", "apple.webp"),
    ("BANANA", "banana.jpg"),
    ("CHERRY", "cherry.jpg"),
    ("GRAPE", "grape.jpg"),
    ("LEMON", "lemon.jpg"),
    ("ORANGE", "orange.jpg"),
    ("PEAR", "pear.jpg"),
    ("CARROT", "carrot.png"),
    ("POTATO", "potato.jpg"),
    ("TOMATO", "tomato.webp"),
    ("ONION", "onion.jpg"),
    ("CUCUMBER", "cucumber.webp")
]


themes = {
    "animals": animals,
    "colors": colors,
    "fruits_vegetables": fruits_vegetables
}

@main_bp.route("/choose-theme")
def choose_theme():
    user = get_current_user()
    if not user:
        return redirect(url_for("auth_bp.login"))
    return render_template("choose_theme.html", themes=themes.keys(), user=user)

@main_bp.route("/play/<theme_name>")
def play(theme_name):
    user = get_current_user()
    if not user:
        return redirect(url_for("auth_bp.login"))

    if theme_name not in themes:
        return "Téma neexistuje!"

    word_list = themes[theme_name]
    chosen = random.choice(word_list)
    chosen_word, chosen_asset = chosen

    session["chosen_word"] = chosen_word
    session["chosen_asset"] = chosen_asset
    session["theme_name"] = theme_name

    return render_template("play.html",
                           user=user,
                           theme=theme_name,
                           word=chosen_word,
                           asset=chosen_asset)

@main_bp.route("/check-word", methods=["POST"])
def check_word():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Nejste přihlášen."}), 401

    data = request.json
    image_data = data.get("image_data", "")
    current_word = session.get("chosen_word", "???")

    if "," in image_data:
        image_data = image_data.split(",")[1]
    try:
        img_bytes = base64.b64decode(image_data)
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("L")
        img_array = np.array(pil_img).astype("float32") / 255.0
    except Exception as e:
        return jsonify({"error": f"Chyba dekódování: {e}"}), 400

    recognized_word = predict_word_from_image(img_array, expected_word=current_word)
    is_correct = recognized_word.upper() == current_word.upper()

    if is_correct:
        segments = segment_letters_and_boxes(img_array, threshold=0.99)

        for i, (sub_img_cropped, _) in enumerate(segments):
            letter = recognized_word[i].upper()
            out_dir = os.path.join("model", "dataset", "new_data", letter)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            file_count = len(os.listdir(out_dir))
            out_name = f"{letter}_n_{file_count}.png"
            out_path = os.path.join(out_dir, out_name)

            pil_sub = Image.fromarray((sub_img_cropped * 255).astype("uint8"))
            pil_sub.save(out_path) 
             
        user.score += 1
        db.session.commit()

    return jsonify({
        "recognized_word": recognized_word,
        "is_correct": is_correct,
        "correct_word": current_word,
        "score": user.score
    })
