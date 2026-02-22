import cv2
import os

"""
function to sort image names in order to maintain the original order

E.g.
"1.jpg" comes before "10.jpg"
"""
def image_name_smart_sort(x:list):
    number_names = []
    string_names = []
    for n in x:
        name = n[:n.rfind('.')]
        try:
            format = n[n.rfind('.'):]
            number_names.append((float(name), name, format))
        except:
            string_names.append(n)
    output = [f"{name}{format}" for _, name, format in sorted(number_names, key=lambda x: x[0])]
    output.extend(sorted(string_names))
    return output
    
# Load all images
attempt = 2

raw_images_path = f'./raw_images/input_{attempt}'
output_compose_path = f'./composed/'

os.makedirs(output_compose_path, exist_ok=True)
format = '.jpg'
last_composition = f"composition_{attempt-1}{format}"
last_composition_path = os.path.join(output_compose_path, last_composition)
output_file_name = f"composition_{attempt}{format}"

images = []


print(f"Reading raw images from {raw_images_path}")
raw_images_read = 0
sorted_images = image_name_smart_sort(os.listdir(raw_images_path))
for file in image_name_smart_sort(os.listdir(raw_images_path)):
    if file.endswith(format):
        img = cv2.imread(os.path.join(raw_images_path, file))
        images.append(img)
        raw_images_read += 1

print(f"Read {raw_images_read} raw images.")
print(sorted_images)

if os.path.exists(last_composition_path):
    print(f"Reading composed image: {last_composition_path}")
    img = cv2.imread(last_composition_path)
    images.append(img)
    print(f"Composed image read.")

# OpenCV stitcher inizializing
stitcher = cv2.Stitcher_create()
status, result = stitcher.stitch(images)

if status == cv2.Stitcher_OK:
    cv2.imwrite(os.path.join(output_compose_path, output_file_name), result)
    print("Success!")
else:
    print(f"Error during stitching. Code error: {status}")
