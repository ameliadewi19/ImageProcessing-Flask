import os
import random
import shutil
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math
from collections import Counter
from pylab import savefig
import cv2
import matplotlib
matplotlib.use('Agg') 


def grayscale():
    if not is_grey_scale("static/img/img_now.jpg"):
        img = Image.open("static/img/img_now.jpg")
        img_arr = np.asarray(img)
        r = img_arr[:, :, 0]
        g = img_arr[:, :, 1]
        b = img_arr[:, :, 2]
        new_arr = r.astype(int) + g.astype(int) + b.astype(int)
        new_arr = (new_arr/3).astype('uint8')
        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")

def is_grey_scale(img_path):
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i, j))
            if r != g != b:
                return False
    return True

def zoomin():
    if is_grey_scale("static/img/img_now.jpg"):
        img = Image.open("static/img/img_now.jpg")
        img_arr = np.asarray(img)
        
        if len(img_arr.shape) == 3:
            # Convert grayscale to 2D array
            img_arr = img_arr[:, :, 0]

        new_size = (img_arr.shape[0] * 2, img_arr.shape[1] * 2)
        new_arr = np.full(new_size, 255, dtype=np.uint8)

        for i in range(len(img_arr)):
            for j in range(len(img_arr[i])):
                new_arr[2*i, 2*j] = img_arr[i, j]
                new_arr[2*i, 2*j+1] = img_arr[i, j]
                new_arr[2*i+1, 2*j] = img_arr[i, j]
                new_arr[2*i+1, 2*j+1] = img_arr[i, j]

        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")
    else:
        img = Image.open("static/img/img_now.jpg")
        img = img.convert("RGB")
        img_arr = np.asarray(img)
        new_size = ((img_arr.shape[0] * 2),
                    (img_arr.shape[1] * 2), img_arr.shape[2])
        new_arr = np.full(new_size, 255)
        new_arr.setflags(write=1)

        r = img_arr[:, :, 0]
        g = img_arr[:, :, 1]
        b = img_arr[:, :, 2]

        new_r = []
        new_g = []
        new_b = []

        for row in range(len(r)):
            temp_r = []
            temp_g = []
            temp_b = []
            for i in r[row]:
                temp_r.extend([i, i])
            for j in g[row]:
                temp_g.extend([j, j])
            for k in b[row]:
                temp_b.extend([k, k])
            for _ in (0, 1):
                new_r.append(temp_r)
                new_g.append(temp_g)
                new_b.append(temp_b)

        for i in range(len(new_arr)):
            for j in range(len(new_arr[i])):
                new_arr[i, j, 0] = new_r[i][j]
                new_arr[i, j, 1] = new_g[i][j]
                new_arr[i, j, 2] = new_b[i][j]

        new_arr = new_arr.astype('uint8')
        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")


def zoomout():
    if is_grey_scale("static/img/img_now.jpg"):
        img = Image.open("static/img/img_now.jpg")
        img_arr = np.asarray(img)
        
        if len(img_arr.shape) == 3:
            # Convert grayscale to 2D array
            img_arr = img_arr[:, :, 0]

        x, y = img_arr.shape
        new_arr = np.zeros((int(x / 2), int(y / 2)), dtype=np.uint8)

        for i in range(0, int(x/2)):
            for j in range(0, int(y/2)):
                new_arr[i, j] = np.mean(img_arr[2*i:2*i+2, 2*j:2*j+2])

        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")
    else:
        img = Image.open("static/img/img_now.jpg")
        img = img.convert("RGB")
        x, y = img.size
        new_arr = Image.new("RGB", (int(x / 2), int(y / 2)))
        r = [0, 0, 0, 0]
        g = [0, 0, 0, 0]
        b = [0, 0, 0, 0]

        for i in range(0, int(x/2)):
            for j in range(0, int(y/2)):
                r[0], g[0], b[0] = img.getpixel((2 * i, 2 * j))
                r[1], g[1], b[1] = img.getpixel((2 * i + 1, 2 * j))
                r[2], g[2], b[2] = img.getpixel((2 * i, 2 * j + 1))
                r[3], g[3], b[3] = img.getpixel((2 * i + 1, 2 * j + 1))
                new_arr.putpixel((int(i), int(j)), (int((r[0] + r[1] + r[2] + r[3]) / 4), int(
                    (g[0] + g[1] + g[2] + g[3]) / 4), int((b[0] + b[1] + b[2] + b[3]) / 4)))
        new_arr = np.uint8(new_arr)
        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_now.jpg")

def move_left():
    img_path = "static/img/img_now.jpg"
    img = Image.open(img_path)
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr[:, :]
        g = np.pad(g, ((0, 0), (0, 50)), 'constant')[:, 50:]
        new_arr = g
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((0, 0), (0, 50)), 'constant')[:, 50:]
        g = np.pad(g, ((0, 0), (0, 50)), 'constant')[:, 50:]
        b = np.pad(b, ((0, 0), (0, 50)), 'constant')[:, 50:]
        new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_right():
    img_path = "static/img/img_now.jpg"
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr[:, :]
        g = np.pad(g, ((0, 0), (50, 0)), 'constant')[:, :-50]
        new_arr = g
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((0, 0), (50, 0)), 'constant')[:, :-50]
        g = np.pad(g, ((0, 0), (50, 0)), 'constant')[:, :-50]
        b = np.pad(b, ((0, 0), (50, 0)), 'constant')[:, :-50]
        new_arr = np.dstack((r, g, b))        
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_up():
    img_path = "static/img/img_now.jpg"
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        r, g, b = img_arr[:, :], img_arr[:, :], img_arr[:, :]
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 50), (0, 0)), 'constant')[50:, :]
    g = np.pad(g, ((0, 50), (0, 0)), 'constant')[50:, :]
    b = np.pad(b, ((0, 50), (0, 0)), 'constant')[50:, :]
    if is_grey_scale(img_path):
        new_arr = r
    else:
        new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_down():
    img_path = "static/img/img_now.jpg"
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr[:, :]
        g = np.pad(g, ((50, 0), (0, 0)), 'constant')[0:-50, :]
        new_arr = g
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((50, 0), (0, 0)), 'constant')[0:-50, :]
        g = np.pad(g, ((50, 0), (0, 0)), 'constant')[0:-50, :]
        b = np.pad(b, ((50, 0), (0, 0)), 'constant')[0:-50, :]
        new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_addition():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img).astype('uint16')
    img_arr = img_arr+100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_substraction():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img).astype('int16')
    img_arr = img_arr-100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_multiplication():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    img_arr = img_arr*1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_division():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    img_arr = img_arr/1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def convolution(img, kernel):
    if len(img.shape) == 3 and img.shape[2] == 3:  # Color image
        h_img, w_img, _ = img.shape
        out = np.zeros((h_img-2, w_img-2), dtype=np.float64)
        new_img = np.zeros((h_img-2, w_img-2, 3))
        if np.array_equal((img[:, :, 1], img[:, :, 0]), img[:, :, 2]) == True:
            array = img[:, :, 0]
            for h in range(h_img-2):
                for w in range(w_img-2):
                    S = np.multiply(array[h:h+3, w:w+3], kernel)
                    out[h, w] = np.sum(S)
            out_ = np.clip(out, 0, 255)
            for channel in range(3):
                new_img[:, :, channel] = out_
        else:
            for channel in range(3):
                array = img[:, :, channel]
                for h in range(h_img-2):
                    for w in range(w_img-2):
                        S = np.multiply(array[h:h+3, w:w+3], kernel)
                        out[h, w] = np.sum(S)
                out_ = np.clip(out, 0, 255)
                new_img[:, :, channel] = out_
        new_img = np.uint8(new_img)
        return new_img

    elif len(img.shape) == 2:  # Grayscale image
        h_img, w_img = img.shape
        out = np.zeros((h_img-2, w_img-2), dtype=np.float64)

        for h in range(h_img-2):
            for w in range(w_img-2):
                S = np.multiply(img[h:h+3, w:w+3], kernel)
                out[h, w] = np.sum(S)

        out_ = np.clip(out, 0, 255)
        new_img = np.uint8(out_)
        return new_img

    else:
        raise ValueError("Unsupported image format")

def edge_detection():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int64)
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")

def blur():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int64)
    kernel = np.array(
        [[0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def sharpening():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int64)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def histogram_rgb():
    img_path = "static/img/img_now.jpg"
    img = Image.open(img_path)
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr[:, :].flatten()
        data_g = Counter(g)
        plt.bar(list(data_g.keys()), data_g.values(), color='black')
        plt.savefig(f'static/img/grey_histogram.jpg', dpi=300)
        plt.clf()
    else:
        r = img_arr[:, :, 0].flatten()
        g = img_arr[:, :, 1].flatten()
        b = img_arr[:, :, 2].flatten()
        data_r = Counter(r)
        data_g = Counter(g)
        data_b = Counter(b)
        data_rgb = [data_r, data_g, data_b]
        warna = ['red', 'green', 'blue']
        data_hist = list(zip(warna, data_rgb))
        for data in data_hist:
            plt.bar(list(data[1].keys()), data[1].values(), color=f'{data[0]}')
            plt.savefig(f'static/img/{data[0]}_histogram.jpg', dpi=300)
            plt.clf()


def df(img):  # to make a histogram (count distribution frequency)
    values = [0]*256
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            values[img[i, j]] += 1
    return values


def cdf(hist):  # cumulative distribution frequency
    cdf = [0] * len(hist)  # len(hist) is 256
    cdf[0] = hist[0]
    for i in range(1, len(hist)):
        cdf[i] = cdf[i-1]+hist[i]
    # Now we normalize the histogram
    # What your function h was doing before
    cdf = [ele*255/cdf[-1] for ele in cdf]
    return cdf


def histogram_equalizer():
    img = cv2.imread('static\img\img_now.jpg', 0)
    my_cdf = cdf(df(img))
    # use linear interpolation of cdf to find new pixel values. Scipy alternative exists
    image_equalized = np.interp(img, range(0, 256), my_cdf)
    cv2.imwrite('static/img/img_now.jpg', image_equalized)


def threshold(lower_thres, upper_thres):
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    condition = np.logical_and(np.greater_equal(img_arr, lower_thres),
                               np.less_equal(img_arr, upper_thres))
    print(lower_thres, upper_thres)
    img_arr = np.asarray(img).copy()
    img_arr[condition] = 255
    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_now.jpg")

def divide_image(image_path, rows, cols):
    try:
        # Baca gambar
        img = Image.open(image_path)
        
        # Periksa apakah ukuran gambar memungkinkan untuk dibagi menjadi bagian sejumlah rows x cols
        if img.size[0] % cols != 0 or img.size[1] % rows != 0:
            # Resize the image to be evenly divisible by rows and cols
            new_width = (img.size[0] // cols) * cols
            new_height = (img.size[1] // rows) * rows
            img = img.resize((new_width, new_height))
        
        # Hitung lebar dan tinggi dari setiap bagian
        part_width = img.size[0] // cols
        part_height = img.size[1] // rows
        
        parts = []
        
        for i in range(rows):
            for j in range(cols):
                # Pilih bagian dari gambar
                left = j * part_width
                upper = i * part_height
                right = (j + 1) * part_width
                lower = (i + 1) * part_height
                
                part = img.crop((left, upper, right, lower))
                # parts.append(part)
                part.save(f"static/img/divided_part_{i}_{j}.jpg")
                parts.append(part)

        return parts
    
    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")
        return None

def get_image_values(image_path):
    try:
        img = Image.open(image_path)
        width, height = img.size
        pixel_values = []

        is_color = len(img.getbands()) == 3

        for y in range(height):
            for x in range(width):
                if is_color:
                    pixel = img.getpixel((x, y))
                else:
                    pixel = (img.getpixel((x, y)),)

                pixel_values.append((pixel, is_color))

        return pixel_values, width, height
    except Exception as e:
        print(f"Error: {e}")
        return [], None, None

def mean_blur(kernel_size):
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.uint8)
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size**2)
    blur = cv2.filter2D(src=img_arr, ddepth=-1, kernel=kernel)
    new_img = Image.fromarray(blur)
    new_img.save("static/img/img_now.jpg")

def gaussian_blur(kernel_size):
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.uint8)
    blur = cv2.GaussianBlur(img_arr, (kernel_size, kernel_size), sigmaX=0)
    new_img = Image.fromarray(blur)
    new_img.save("static/img/img_now.jpg")

def median_blur(kernel_size):
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.uint8)
    blur = cv2.medianBlur(img_arr, kernel_size)
    new_img = Image.fromarray(blur)
    new_img.save("static/img/img_now.jpg")

def apply_identity():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int64)
    kernel = np.array([[0, 0, 0],
                       [0, 1, 0],
                       [0, 0, 0]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")

def bilateral_filter():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.uint8)
    bf = cv2.bilateralFilter(src=img_arr, d=9, sigmaColor=75, sigmaSpace=75)
    new_img = Image.fromarray(bf)
    new_img.save("static/img/img_now.jpg")

def zero_padding():
    image_path = "static/img/img_now.jpg"  # Ganti dengan path gambar yang Anda gunakan
    img = Image.open(image_path)
    img_arr = np.asarray(img, dtype=np.uint8)
    padded_image = cv2.copyMakeBorder(img_arr, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    new_img = Image.fromarray(padded_image)
    new_img.save("static/img/img_now.jpg")

def apply_filter(image_path, kernel, kernel_type):
    img = Image.open(image_path)
    if (kernel_type == "highpass"):
        img_arr = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    else:
        img_arr = np.asarray(img, dtype=np.uint8)
    filtered_image = cv2.filter2D(src=img_arr, ddepth=-1, kernel=kernel)
    new_img = Image.fromarray(filtered_image)
    new_img.save("static/img/img_now.jpg")

def generate_random_kernel(size):
    return np.random.rand(size, size)

def lowpass_kernel(size):
    kernel = generate_random_kernel(size)
    return kernel / np.sum(kernel)

def highpass_kernel(size):
    return np.identity(size) - lowpass_kernel(size)

def bandpass_kernel(size, low_cutoff, high_cutoff):
    highpass = highpass_kernel(size)
    lowpass = lowpass_kernel(size)
    return high_cutoff * highpass - low_cutoff * lowpass

def generate_and_apply_kernel(kernel_type, kernel_size):
    if kernel_type == "lowpass":
        kernel = lowpass_kernel(kernel_size)
    elif kernel_type == "highpass":
        kernel = highpass_kernel(kernel_size)
    elif kernel_type == "bandpass":
        low_cutoff = 0.1
        high_cutoff = 0.9
        kernel = bandpass_kernel(kernel_size, low_cutoff, high_cutoff)
    else:
        raise ValueError("Invalid kernel type. Use 'lowpass', 'highpass', or 'bandpass'.")

    apply_filter("static/img/img_now.jpg", kernel, kernel_type)

# batas game
def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            img_path = os.path.join(folder_path, filename)
            images.append(img_path)
    return images

def duplicate_images(images):
    for img_path in images:
        img_name, img_ext = os.path.splitext(os.path.basename(img_path))
        new_img_path = os.path.join("static/game/", f"{img_name}_copy{img_ext}")
        # Cek apakah file salinan sudah ada di folder tujuan
        if not os.path.exists(img_path):
            # Jika belum ada, salin gambar
            shutil.copy2(img_path, new_img_path)

def combine_and_shuffle(images):
    paired_images = images + images
    random.shuffle(paired_images)
    return paired_images

def game_grayscale():
    if not is_grey_scale("static/img/img_normal.jpg"):
        img = Image.open("static/img/img_normal.jpg")
        img_arr = np.asarray(img)
        r = img_arr[:, :, 0]
        g = img_arr[:, :, 1]
        b = img_arr[:, :, 2]
        new_arr = r.astype(int) + g.astype(int) + b.astype(int)
        new_arr = (new_arr/3).astype('uint8')
        new_img = Image.fromarray(new_arr)
        new_img.save("static/game/img_grayscale.jpg")

def game_mean_blur():
    img = Image.open("static/img/img_normal.jpg")
    img_arr = np.asarray(img, dtype=np.uint8)
    kernel = np.ones((10, 10), np.float32) / (10**2)
    blur = cv2.filter2D(src=img_arr, ddepth=-1, kernel=kernel)
    new_img = Image.fromarray(blur)
    new_img.save("static/game/img_mean_blur.jpg")

def game_sepia_tone():
    img = Image.open("static/img/img_normal.jpg")
    img_arr = np.asarray(img)

    # Matriks transformasi untuk sepia
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])

    # Terapkan transformasi
    sepia_image = cv2.transform(img_arr, kernel)

    # Batasi nilai piksel ke 255
    sepia_image = np.where(sepia_image > 255, 255, sepia_image)

    new_img = Image.fromarray(sepia_image.astype('uint8'))
    new_img.save("static/game/img_sepia_tone.jpg")

def game_edge_detection():
    img = Image.open("static/img/img_normal.jpg")
    img_arr = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

    # Terapkan filter deteksi tepi
    edges = cv2.Canny(img_arr, 100, 200)

    new_img = Image.fromarray(edges)
    new_img.save("static/game/img_edge_detection.jpg")

def game_blue():
    img = Image.open("static/img/img_normal.jpg")
    img_arr = np.array(img)

    # Buat salinan gambar agar dapat dimodifikasi
    new_img_arr = np.copy(img_arr)

    # Tingkatkan saluran warna biru (B) dan kurangi saluran merah (R) dan hijau (G)
    new_img_arr[:, :, 0] = new_img_arr[:, :, 0] * 0.8  # Saluran merah dikurangi
    new_img_arr[:, :, 1] = new_img_arr[:, :, 1] * 0.8  # Saluran hijau dikurangi
    new_img_arr[:, :, 2] = 100  # Saluran biru ditingkatkan

    # Pastikan nilai piksel tetap dalam rentang 0-255
    new_img_arr = np.clip(new_img_arr, 0, 255)

    new_img = Image.fromarray(new_img_arr.astype('uint8'))
    new_img.save("static/game/img_blue.jpg")


def game_emboss():
    img = Image.open("static/img/img_normal.jpg")
    img_arr = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

    # Matriks kernel untuk emboss
    kernel = np.array([[-2,-1,0], [-1,1,1], [0,1,2]])

    # Terapkan filter
    embossed = cv2.filter2D(img_arr, -1, kernel)

    new_img = Image.fromarray(embossed)
    new_img.save("static/game/img_emboss.jpg")

def game_invert_colors():
    img = Image.open("static/img/img_normal.jpg")
    img_arr = 255 - np.asarray(img)
    new_img = Image.fromarray(img_arr.astype('uint8'))
    new_img.save("static/game/img_invert_colors.jpg")

def game_purple_tint():
    img = Image.open("static/img/img_normal.jpg")

    # Matriks transformasi untuk mengubah nuansa ke ungu
    purple_tint_matrix = [
        [0.7, 0.3, 0.7],
        [0.3, 0.6, 0.3],
        [0.4, 0.4, 0.9]
    ]

    img = img.convert("RGB")  # Pastikan gambar dalam mode warna RGB
    width, height = img.size
    pixels = img.load()

    for py in range(height):
        for px in range(width):
            r, g, b = img.getpixel((px, py))

            new_r = int(r * purple_tint_matrix[0][0] + g * purple_tint_matrix[0][1] + b * purple_tint_matrix[0][2])
            new_g = int(r * purple_tint_matrix[1][0] + g * purple_tint_matrix[1][1] + b * purple_tint_matrix[1][2])
            new_b = int(r * purple_tint_matrix[2][0] + g * purple_tint_matrix[2][1] + b * purple_tint_matrix[2][2])

            # Pastikan nilai tidak melebihi 255
            new_r = min(new_r, 255)
            new_g = min(new_g, 255)
            new_b = min(new_b, 255)

            pixels[px, py] = (new_r, new_g, new_b)

    img.save("static/game/img_purple_tint.jpg")

def game_bilateral():
    img = Image.open("static/img/img_normal.jpg")
    img_arr = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

    # Terapkan filter bilateral
    bilateral = cv2.bilateralFilter(img_arr, 9, 75, 75)

    new_img = Image.fromarray(bilateral)
    new_img.save("static/game/img_bilateral.jpg")

def game_pencil_sketch():
    img = Image.open("static/img/img_normal.jpg")
    img_gray = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2GRAY)

    # Invert warna gambar
    inverted_img = 255 - img_gray

    # Terapkan Gaussian Blur
    blurred_img = cv2.GaussianBlur(inverted_img, (21, 21), 0)

    # Gabungkan gambar asli dan gambar blur
    pencil_sketch = cv2.divide(255 - blurred_img, 255, scale=256)

    new_img = Image.fromarray(pencil_sketch)
    new_img.save("static/game/img_pencil_sketch.jpg")

def game_gamma_correction():
    img = Image.open("static/img/img_normal.jpg")
    img_arr = np.asarray(img)

    # Koreksi gamma
    gamma = 2.0
    corrected_img = 255 * (img_arr / 255) ** (1 / gamma)

    new_img = Image.fromarray(corrected_img.astype('uint8'))
    new_img.save("static/game/img_gamma_correction.jpg")

def game_solarize():
    img = Image.open("static/img/img_normal.jpg")
    img_arr = 255 - np.asarray(img)

    # Terapkan thresholding
    threshold = 128
    img_arr[img_arr > threshold] = 255 - img_arr[img_arr > threshold]

    new_img = Image.fromarray(img_arr.astype('uint8'))
    new_img.save("static/game/img_solarize.jpg")

def game_orange():
    img = Image.open("static/img/img_normal.jpg")
    img_arr = np.array(img)

    # Buat salinan gambar agar dapat dimodifikasi
    new_img_arr = np.copy(img_arr)

    # Kurangi saluran warna merah (R) dan tingkatkan saluran biru (B) dan hijau (G)
    new_img_arr[:, :, 0] = 100  # Saluran merah maksimum
    new_img_arr[:, :, 1] = new_img_arr[:, :, 1] * 0.5  # Saluran hijau setengah
    new_img_arr[:, :, 2] = new_img_arr[:, :, 2] * 0  # Saluran biru minimum

    new_img = Image.fromarray(new_img_arr)
    new_img.save("static/game/img_orange.jpg")

def game_green_tint():
    img = Image.open("static/img/img_normal.jpg")
    img_arr = np.array(img, dtype=np.uint8)  # Create a copy of the array

    img_arr[:, :, 1] = img_arr[:, :, 1] + 50  # Modify the copy

    new_img = Image.fromarray(img_arr)
    new_img.save("static/game/img_green_tint.jpg")

