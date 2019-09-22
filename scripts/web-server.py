"""
Luz Vision
A world made with words for those visually impaired or blinds.
"""
from flask import Flask, jsonify, request, url_for, render_template
import json
from flask_cors import CORS
import urllib.request
import imageclassifier
import imagecaption
import random
from PIL import Image
from io import BytesIO
import re, time, base64

def getI420FromBase64(codec, image_path="temp/"):
    base64_data = re.sub('^data:image/.+;base64,', '', codec)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    t = time.time()
    img.save(image_path + 'temp.png', "PNG")

# JSON display handler.
def display_msg(request_obj, input_obj):
    post_content = request_obj.args.get('url')
    if not request_obj.args.get('url'):
        post_content = request_obj.form['url']
    if not post_content:
        return jsonify({"Error": 'No URL entered'})
    try:
        return jsonify(input_obj(post_content))
    except Exception as e:
        return jsonify({"Error": 'There was an error while processing your request. ' + str(e)})

# Web Server declaration.
def flask_app():
    app = Flask(__name__, static_url_path='/static')
    CORS(app)

    # Declare the mapped url
    a_new_static_path = ''

    # Set the static_url_path property.
    app.static_url_path = a_new_static_path

    # Add the updated rule.
    app.add_url_rule(f'{a_new_static_path}/<path:filename>',
                    endpoint='static',
                    view_func=app.send_static_file)

    # Root route.
    @app.route('/', methods=['GET', 'POST'])
    def form_example():
        return render_template("index.html")
        
    # Image prediction route.
    @app.route('/predict_image', methods=['GET', 'POST'])
    def start():
        getI420FromBase64(request.form['url'])
        return display_msg(request, imageclassifier.classify_image)

    # Image caption route.
    @app.route('/image_caption', methods=['GET', 'POST'])
    def image_caption():
        getI420FromBase64(request.form['url'])
        return display_msg(request, imagecaption.gen_caption)

    return app

# Initiate Web Server
if __name__ == '__main__':
    app = flask_app()
    app.run(debug=False, host='0.0.0.0', port=5002)
