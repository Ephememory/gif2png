import sys
import io
import os
from PIL import Image
from PIL import ImageSequence


def main(dir, contents, output_dir_prefix) -> None:
    if output_dir_prefix is not None and len(output_dir_prefix) > 0:
        destination_dir = dir + "\\" + output_dir_prefix + "_" + "sheets"
    else:
        destination_dir = dir + "\\" + "sheets"

    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)

    for i, filename in enumerate(contents):
        abs_path = dir + "\\" + filename
        with Image.open(abs_path) as gif:
            print(f"Processing: {abs_path} image mode: {gif.mode}")

            if not gif.is_animated or gif.n_frames <= 0:
                continue

            sprite_sheet = Image.new(mode="RGBA", size=(
                gif.width * gif.n_frames, gif.height))

            n_frame = 0
            for frame in ImageSequence.Iterator(gif):
                sprite_sheet.paste(
                    frame, (n_frame * frame.width, 0))
                n_frame += 1

            sheet_filename = filename.replace(".gif", ".png")
            sprite_sheet.save(destination_dir + "\\" + sheet_filename)


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
        output_prefix = None
        if argc >= 3:
            output_prefix = sys.argv[2]
        main(dir, contents, output_prefix)
