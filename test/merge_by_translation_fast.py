import cv2
from src.merge_by_traslation import merge_by_translation
from src.main import load_images_from_folder
def compute_merge_with_log(base, new_img, iteration, x_direction, y_direction):
    print(f"Iteration {iteration}:")
    merged, shift, response = merge_by_translation(base, new_img, x_direction, y_direction)
    print("Shift:", shift)
    print("Response:", response)
    return merged
	
imgs = load_images_from_folder("raw_images\\input_5")
base = compute_merge_with_log(imgs[0], imgs[1], 1, 1, -1)
cv2.imwrite("test\\translation_merged.jpg", base)
