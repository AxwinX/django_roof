import os

from django.core.exceptions import ValidationError
from PIL import Image

MAX_IMAGE_SIZE_MB = 2
MIN_DIMENSION = 100      # px
MAX_DIMENSION = 4000     # px
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}


def validate_image_extension(file):
    ext = os.path.splitext(file.name)[1].lower().lstrip(".")
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file type '.{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}."
        )


def validate_image_size(file):
    if file.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"Image is too large. Maximum size is {MAX_IMAGE_SIZE_MB} MB.")


def validate_image_content(file):
    """Check the bytes really are an image (not just a renamed file) and check dimensions."""
    error = None
    fmt = width = height = None
    try:
        file.seek(0)
        img = Image.open(file)
        img.verify()                 # integrity check
        file.seek(0)
        img = Image.open(file)       # verify() invalidates the object, reopen
        fmt = img.format
        width, height = img.size
    except Exception:
        error = "This file is not a valid image."
    finally:
        file.seek(0)

    if error:
        raise ValidationError(error)
    if fmt not in ALLOWED_FORMATS:
        raise ValidationError("Image content must be JPEG, PNG or WebP.")
    if width < MIN_DIMENSION or height < MIN_DIMENSION:
        raise ValidationError(
            f"Image is too small ({width}x{height}). Minimum is {MIN_DIMENSION}x{MIN_DIMENSION} px."
        )
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValidationError(
            f"Image is too large ({width}x{height}). Maximum is {MAX_DIMENSION}x{MAX_DIMENSION} px."
        )
