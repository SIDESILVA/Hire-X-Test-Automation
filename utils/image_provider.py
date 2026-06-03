import os
import random

class ImageProvider:

    def __init__(self):

        base_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "images"
        )

        self.base_dir = base_dir

        # ✅ LOAD ALL IMAGES DYNAMICALLY (img1 → img15 etc.)
        self.images = [
            os.path.join(self.base_dir, f)
            for f in os.listdir(self.base_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        if not self.images:
            raise Exception("❌ No images found in data/images folder")

        # optional: shuffle once at start
        random.shuffle(self.images)

    def get_next_image_file(self):

        image_path = random.choice(self.images)

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        return image_path