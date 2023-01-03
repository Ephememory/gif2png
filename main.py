import sys
import io
import os
from PIL import Image


def main(dir, contents) -> None:
    print(dir)
    for i, path in enumerate(contents):
        abs_path = dir + "\\" + path
        with Image.open(abs_path) as gif:
            print(f"Processing: {abs_path} image mode: {gif.mode}")

            if not gif.is_animated or gif.n_frames <= 0:
                continue

            sprite_sheet = Image.new(mode=gif.mode, size=(
                gif.width * gif.n_frames, gif.height))
            sprite_sheet.putpalette(gif.getpalette())

            for n_frame in range(gif.n_frames):
                for y in range(gif.height):
                    for x in range(gif.width):
                        pixel = gif.getpixel((x, y))
                        print(f"{path} : {pixel}")
                        # if type(pixel) is tuple and len(pixel) >= 4 and pixel[3] <= 0:
                        #     pixel = (0, 0, 0)
                        dest_x = x + gif.width * n_frame
                        sprite_sheet.putpixel((dest_x, y), pixel)
                gif.seek(n_frame)
            sprite_sheet_path = path.replace(".gif", ".png")
            sprite_sheet.save(sprite_sheet_path)


if __name__ == "__main__":
    dir = None
    argc = len(sys.argv)

    if argc <= 1:
        print("Expected a filepath to batch convert gifs! Exiting.")
        exit()

    desired_dir = sys.argv[1]
    if os.path.isdir(desired_dir):
        contents = os.listdir(desired_dir)
        if contents == None or contents == []:
            print("No files in desired directory! Exiting.")
            exit()
        dir = desired_dir
        main(dir, contents)
