import sys
from PIL import Image
import random

class ImageTransformer:
    def __init__(self, image_path, key, output_path, operation, method):
        self.image_path = image_path
        self.key = key
        self.output_path = output_path
        self.operation = operation
        self.method = method

    def swap_pixels(self, image):
        random.seed(self.key)
        width, height = image.size
        pixel_data = list(image.getdata())
        indices = list(range(len(pixel_data)))
        random.shuffle(indices)
        shuffled_pixel_data = [pixel_data[i] for i in indices]
        return shuffled_pixel_data, indices

    def unswap_pixels(self, image, indices):
        random.seed(self.key)
        width, height = image.size
        pixel_data = list(image.getdata())
        unshuffled_pixel_data = [None] * len(pixel_data)
        for original_index, shuffled_index in enumerate(indices):
            unshuffled_pixel_data[shuffled_index] = pixel_data[original_index]
        return unshuffled_pixel_data

    def apply_key_to_pixels(self, pixel_data):
        transformed_pixel_data = []
        for pixel in pixel_data:
            if self.operation == "encrypt":
                transformed_pixel = tuple((p + self.key) % 256 for p in pixel)
            else:
                transformed_pixel = tuple((p - self.key) % 256 for p in pixel)
            transformed_pixel_data.append(transformed_pixel)
        return transformed_pixel_data

    def transform_image(self):
        image = Image.open(self.image_path)
        width, height = image.size
        if self.method == "swap":
            if self.operation == "encrypt":
                transformed_pixel_data, indices = self.swap_pixels(image)
                image.putdata(transformed_pixel_data)
                with open(self.output_path + ".key", 'w') as key_file:
                    key_file.write(str(indices))
            else:
                with open(self.output_path + ".key", 'r') as key_file:
                    indices = eval(key_file.read())
                transformed_pixel_data = self.unswap_pixels(image, indices)
                image.putdata(transformed_pixel_data)
        else:
            pixel_data = list(image.getdata())
            transformed_pixel_data = self.apply_key_to_pixels(pixel_data)
            image.putdata(transformed_pixel_data)

        image.save(self.output_path)
        print(f"Image {self.operation}ed successfully and saved to {self.output_path}!")

def main():
    if len(sys.argv) != 6:
        print("Usage: python script.py <encrypt/decrypt> <input_path> <key> <output_path> <method>")
        print("Method can be 'swap' or 'math'")
        return
    
    action = sys.argv[1]
    input_path = sys.argv[2]
    key = int(sys.argv[3])
    output_path = sys.argv[4]
    method = sys.argv[5]

    if method not in ["swap", "math"]:
        print("Invalid method. Use 'swap' or 'math'.")
        return

    transformer = ImageTransformer(input_path, key, output_path, action, method)
    transformer.transform_image()

if __name__ == "__main__":
    main()
