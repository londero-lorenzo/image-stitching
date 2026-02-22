import cv2
import os
import argparse


def image_name_smart_sort(files: list):
    number_names = []
    string_names = []

    for n in files:
        name, ext = os.path.splitext(n)
        try:
            number_names.append((float(name), name, ext))
        except ValueError:
            string_names.append(n)

    sorted_numeric = [
        f"{name}{ext}"
        for _, name, ext in sorted(number_names, key=lambda x: x[0])
    ]

    return sorted_numeric + sorted(string_names)


def load_images_from_folder(folder_path, extension=".jpg"):
    images = []
    files = image_name_smart_sort(os.listdir(folder_path))

    for file in files:
        if file.lower().endswith(extension):
            img = cv2.imread(os.path.join(folder_path, file))
            if img is not None:
                images.append(img)

    return images


def stitch_images(images, output_path):
    if len(images) < 2:
        print("Need at least 2 images to stitch.")
        return

    stitcher = cv2.Stitcher_create()
    status, result = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        cv2.imwrite(output_path, result)
        print(f"Stitching successful. Saved to {output_path}")
    else:
        print(f"Error during stitching. Code: {status}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Stitch DrawNote exported images."
    )

    parser.add_argument(
        "--raw_images",
        type=str,
        required=True,
        help="Folder containing raw images"
    )

    parser.add_argument(
        "--composed_image",
        type=str,
        help="Path to an already composed image"
    )

    parser.add_argument(
        "--order",
        choices=["before", "after"],
        help="Whether to use composed image before or after raw images"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="composition_result.jpg",
        help="Output file path"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    images = []

    # Load raw images
    print(f"Loading raw images from {args.raw_images}")
    raw_images = load_images_from_folder(args.raw_images)
    print(f"Loaded {len(raw_images)} raw images.")

    # Optional composed image
    composed_img = None
    if args.composed_image:
        if os.path.exists(args.composed_image):
            print(f"Loading composed image: {args.composed_image}")
            composed_img = cv2.imread(args.composed_image)
        else:
            print("Composed image path not found.")
            return

    # Decide order
    if composed_img is not None:
        if args.order == "before":
            images = [composed_img] + raw_images
        elif args.order == "after":
            images = raw_images + [composed_img]
        else:
            print("You must specify --order before|after when using --composed_image")
            return
    else:
        images = raw_images

    stitch_images(images, args.output)


if __name__ == "__main__":
    main()