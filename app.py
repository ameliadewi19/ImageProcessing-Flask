import numpy as np
from PIL import Image
import image_processing
import os
from flask import Flask, render_template, request, make_response
from datetime import datetime
from functools import wraps, update_wrapper
from shutil import copyfile

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


@app.route("/index")
@app.route("/")
@nocache
def index():
    return render_template("home.html", file_path="img/image_here.jpg")


@app.route("/about")
@nocache
def about():
    return render_template('about.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/upload", methods=["POST"])
@nocache
def upload():
    target = os.path.join(APP_ROOT, "static/img")
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now.jpg")
    copyfile("static/img/img_now.jpg", "static/img/img_normal.jpg")
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/divide_image", methods=["POST"])
@nocache
def divide_image():
    num_puzzles = int(request.form['num_puzzles'])
    image_path = "static/img/img_now.jpg"  # Assuming this is the path of your uploaded image
    rows = num_puzzles
    cols = num_puzzles

    parts = image_processing.divide_image(image_path, rows, cols)

    if parts is not None:
        return render_template("divided_images.html", image_paths=[f"static/img/divided_part_{i}_{j}.jpg" for i in range(rows) for j in range(cols)], rows=rows, cols=cols)
    else:
        return "Terjadi kesalahan saat membagi gambar. Silakan coba lagi."
    
@app.route("/random_image", methods=["POST"])
@nocache
def random_image():
    num_puzzles = int(request.form['num_puzzles'])
    image_path = "static/img/img_now.jpg"  # Assuming this is the path of your uploaded image
    rows = num_puzzles
    cols = num_puzzles

    parts = image_processing.divide_image(image_path, rows, cols)

    if parts is not None:
        return render_template("random_images.html", image_paths=[f"static/img/divided_part_{i}_{j}.jpg" for i in range(rows) for j in range(cols)], rows=rows, cols=cols)
    else:
        return "Terjadi kesalahan saat membagi gambar. Silakan coba lagi."

@app.route('/show_image_values', methods=['POST'])
@nocache
def show_image_values():
    # Mendapatkan nilai dari gambar
    pixel_values, width, height = image_processing.get_image_values('static/img/img_now.jpg')
    
    # Menentukan apakah gambar berwarna atau grayscale
    img = Image.open('static/img/img_now.jpg')
    is_color = img.mode == 'RGB'  # Atau tentukan logika untuk menentukan apakah gambar berwarna atau grayscale
    
    # Mengirimkan nilai-nilai tersebut ke template HTML
    return render_template("pixel_images.html", is_color=is_color, pixel_values=pixel_values, width=width, height=height)

@app.route("/normal", methods=["POST"])
@nocache
def normal():
    copyfile("static/img/img_normal.jpg", "static/img/img_now.jpg")
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/game_card", methods=["POST"])
@nocache
def game_card():
    image_processing.game_grayscale()
    image_processing.game_mean_blur()
    image_processing.game_sepia_tone()
    image_processing.game_edge_detection()
    image_processing.game_blue()
    image_processing.game_emboss()
    image_processing.game_invert_colors()
    image_processing.game_purple_tint()
    image_processing.game_bilateral()
    image_processing.game_pencil_sketch()
    image_processing.game_green_tint()
    image_processing.game_gamma_correction()
    image_processing.game_solarize()
    image_processing.game_orange()
    folder_path = "static/game/"
    images = image_processing.load_images_from_folder(folder_path)
    image_processing.duplicate_images(images)
    paired_images = image_processing.combine_and_shuffle(images)
    return render_template("game_card.html", paired_images=paired_images)


@app.route("/grayscale", methods=["POST"])
@nocache
def grayscale():
    image_processing.grayscale()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/zoomin", methods=["POST"])
@nocache
def zoomin():
    image_processing.zoomin()
    return render_template("zoom.html", file_path="img/img_now.jpg")


@app.route("/zoomout", methods=["POST"])
@nocache
def zoomout():
    image_processing.zoomout()
    return render_template("zoom.html", file_path="img/img_now.jpg")


@app.route("/move_left", methods=["POST"])
@nocache
def move_left():
    image_processing.move_left()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_right", methods=["POST"])
@nocache
def move_right():
    image_processing.move_right()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_up", methods=["POST"])
@nocache
def move_up():
    image_processing.move_up()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_down", methods=["POST"])
@nocache
def move_down():
    image_processing.move_down()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_addition", methods=["POST"])
@nocache
def brightness_addition():
    image_processing.brightness_addition()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_substraction", methods=["POST"])
@nocache
def brightness_substraction():
    image_processing.brightness_substraction()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_multiplication", methods=["POST"])
@nocache
def brightness_multiplication():
    image_processing.brightness_multiplication()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_division", methods=["POST"])
@nocache
def brightness_division():
    image_processing.brightness_division()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/histogram_equalizer", methods=["POST"])
@nocache
def histogram_equalizer():
    image_processing.histogram_equalizer()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/edge_detection", methods=["POST"])
@nocache
def edge_detection():
    image_processing.edge_detection()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/blur", methods=["POST"])
@nocache
def blur():
    image_processing.blur()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/sharpening", methods=["POST"])
@nocache
def sharpening():
    image_processing.sharpening()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/histogram_rgb", methods=["POST"])
@nocache
def histogram_rgb():
    image_processing.histogram_rgb()
    if image_processing.is_grey_scale("static/img/img_now.jpg"):
        return render_template("histogram.html", file_paths=["img/grey_histogram.jpg"])
    else:
        return render_template("histogram.html", file_paths=["img/red_histogram.jpg", "img/green_histogram.jpg", "img/blue_histogram.jpg"])


@app.route("/thresholding", methods=["POST"])
@nocache
def thresholding():
    lower_thres = int(request.form['lower_thres'])
    upper_thres = int(request.form['upper_thres'])
    image_processing.threshold(lower_thres, upper_thres)
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/mean_blur", methods=["POST"])
def mean_blur():
    kernel_size = int(request.form.get("kernel_size"))
    image_processing.mean_blur(kernel_size)
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/gaussian_blur", methods=["POST"])
def gaussian_blur():
    kernel_size = int(request.form.get("kernel_size"))
    image_processing.gaussian_blur(kernel_size)
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/median_blur", methods=["POST"])
def median_blur():
    kernel_size = int(request.form.get("kernel_size"))
    image_processing.median_blur(kernel_size)
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/identitas", methods=["POST"])
@nocache
def identitas():
    image_processing.apply_identity()
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/bilateral_filter", methods=["POST"])
def bilateral_filter():
    image_processing.bilateral_filter()
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/zero_padding", methods=["POST"])
def zero_padding():
    image_processing.zero_padding()
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/apply_random_kernel", methods=["POST"])
def apply_random_kernel():
    kernel_size = int(request.form.get("kernel_size"))
    kernel_type = request.form.get("kernel_type")

    kernel = image_processing.generate_and_apply_kernel(kernel_type, kernel_size)
    # image_processing.apply_filter("static/img/img_now.jpg", kernel)

    return render_template("uploaded.html", file_path="img/img_now.jpg")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
