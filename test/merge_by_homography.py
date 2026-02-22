import cv2
from src.merge_by_homography import merge_by_homography
from src.main import load_images_from_folder
def compute_merge_with_log(base, new_img, iteration):
    print(f"Iteration {iteration}:")
    merged = merge_by_homography(base, new_img)
    return merged

imgs = load_images_from_folder("raw_images\\input_5")
    
base = compute_merge_with_log(imgs[0], imgs[1], 1)

#for i, img in enumerate(imgs[2:]):
#    base = compute_merge_with_log(base, img, i +2)


cv2.imwrite("test\\homography_merged.jpg", base)