import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO


def load_img(path):
    """Load an image given a filename or url.

    Args:
        path: data path, may be local or url as a string beginning with
        http.

    Returns:
        Grayscale image
    """

    if path[0:4] == "http":
        response = requests.get(path)
        local_image = Image.open(BytesIO(response.content))
    else:
        local_image = Image.open(path)  # read image

    local_image = local_image.convert('L')
    local_image = local_image.convert('F')

    return local_image


def display_image_nrmse(input_image, reference_image, title="", cmap='gray'):
    """Display an image along with the NRMSE relative to the reference
       image in the title.

    Args:
        input_image: image to be displayed
        reference_image: reference image for calculating nrmse of input_image
        title: title for the plot
        cmap: colormap for image display
    """
    title = title + ", NRMSE = " + str(nrmse(input_image, reference_image))
    display_img_console(input_image, title=title, cmap=cmap)


def display_img_console(input_image, title="", cmap='gray'):
    """Display an image in console using :mod:`matplotlib.pyplot`

    Args:
        input_image: image to be displayed
        title: title for the plot
        cmap: colormap for image display
    """
    plt.imshow(np.asarray(input_image), vmin=0, vmax=1, cmap=cmap)
    plt.colorbar()
    plt.title(title)
    plt.show()


def stack_init_image(init_image, num_images):
    """Create a list from a single image.

    Args:
        init_image: a single image to be copied and stacked
        num_images: number of copies to be included

    Returns:
        A list of copies of the original image
    """
    init_images = []
    for j in range(num_images):
        init_images.append(np.asarray(init_image.copy()))

    return init_images


def downscale(input_image, scale_factor, resample):
    """Downscale the image via decimation by the given factor in each
    direction.

    Args:
        input_image: input image as a numpy array
        scale_factor: upscale factor
        resample: interpolation type as in PIL.Image.py
                  (NEAREST = NONE = 0, LANCZOS = 1, BILINEAR = 2,
                   BICUBIC = 3, BOX = 4, HAMMING = 5)

    Returns:
        Downscaled image
    """
    return upscale(input_image, 1/scale_factor, resample)


def upscale(input_image, scale_factor, resample):
    """Upscale the image via replication by the given factor in each
    direction.

    Args:
        input_image: input image
        scale_factor: upscale factor
        resample: interpolation type as in PIL.Image.py
                   (NEAREST = NONE = 0, LANCZOS = 1, BILINEAR = 2,
                    BICUBIC = 3, BOX = 4, HAMMING = 5)

    Returns:
        Upscaled image
    """
    new_img = input_image.copy()
    size = np.round(scale_factor * np.array(input_image.size)).astype(np.int)
    return new_img.resize(size, resample)


def nrmse(image, reference):
    """Calculate the NRMSE of an image with respect to a reference.

    Args:
        image: input image to be compared with reference
        reference: reference image

    Returns:
        Root mean square error of the difference of image and reference,
        divided by the root mean square of the reference
    """
    nrmse = (np.sqrt(np.mean((np.asarray(image) - np.asarray(reference))**2)) /
             np.sqrt(np.mean(np.asarray(reference)**2)))
    return np.round(nrmse, decimals=3)


def add_noise(clean_image, noise_std, seed=None):
    """Add Gaussian white noise to an image.

    Args:
        clean_image: input image
        noise_std: standard deviation of noise to be added
        seed: seed for random number generator

    Returns:
        image with noise added, clipped to valid range of values
    """
    if seed is not None:
        np.random.seed(seed)
    noise = noise_std * np.random.standard_normal(clean_image.size)
    noise = np.squeeze(noise)
    noisy_data = np.asarray(clean_image) + noise
    noisy_data = np.clip(noisy_data, 0, 1)
    noisy_image = Image.fromarray(noisy_data)
    return noisy_image
