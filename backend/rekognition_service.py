import sys
from pathlib import Path
from io import BytesIO

from PIL import Image, ImageOps, UnidentifiedImageError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from configuration.config import build_llm

# Reuse your existing AWS configuration
rekognition, _ = build_llm("rekognition")


def detect_image_labels(
    image_bytes: bytes,
    max_labels: int = 10,
    min_confidence: float = 70,
):
    """
    Convert an uploaded image to JPEG and detect labels using AWS.
    """

    if not image_bytes:
        raise ValueError("Uploaded image is empty.")

    try:
        # Read the actual image bytes
        with Image.open(BytesIO(image_bytes)) as original:
            original = ImageOps.exif_transpose(original)
            original.load()

            # Convert RGBA, grayscale, etc. to standard RGB
            image = original.convert("RGB")

            # Resize very large images
            image.thumbnail((3000, 3000))

            # Encode as standard JPEG
            output = BytesIO()
            image.save(output, format="JPEG", quality=90, optimize=True)
            jpeg_bytes = output.getvalue()

            # Keep the image under AWS's 5 MB byte-image limit
            quality = 80
            while len(jpeg_bytes) > 4_800_000 and quality >= 40:
                output = BytesIO()
                image.save(
                    output,
                    format="JPEG",
                    quality=quality,
                    optimize=True,
                )
                jpeg_bytes = output.getvalue()
                quality -= 10

            if len(jpeg_bytes) > 5_000_000:
                raise ValueError(
                    "Image is too large after compression. "
                    "Please upload a smaller image."
                )

    except UnidentifiedImageError as exc:
        raise ValueError(
            "The uploaded file is not a valid image. "
            "Try opening it and saving it as JPEG or PNG."
        ) from exc

    # Call Amazon Rekognition with normalized JPEG bytes
    response = rekognition.detect_labels(
        Image={"Bytes": jpeg_bytes},
        MaxLabels=int(max_labels),
        MinConfidence=float(min_confidence),
    )

    return response.get("Labels", [])
