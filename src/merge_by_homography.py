import cv2
import numpy as np

def merge_by_homography(base_img, new_img):
    """
    Merge di due immagini assumendo:
    - scale diverse
    - rotazioni diverse
    - traslazioni

    Gestisce shift positivi e negativi.
    
    Ritorna:
        merged_image
    """
        
    # Convert to gray
    gray1 = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)

    # Usa SIFT (molto meglio di ORB per questo caso)
    sift = cv2.SIFT_create()

    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    # Matcher
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # Lowe ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    print("Good matches:", len(good))

    if len(good) < 10:
        print("Troppi pochi match. Non posso calcolare omografia.")
        exit()

    # Costruisci punti
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

    # Calcolo omografia
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Dimensioni canvas finale
    h1, w1 = base_img.shape[:2]
    h2, w2 = new_img.shape[:2]

    corners_base_img = np.float32([[0,0],[0,h1],[w1,h1],[w1,0]]).reshape(-1,1,2)
    transformed_corners = cv2.perspectiveTransform(corners_base_img, H)

    corners = np.concatenate((transformed_corners,
                              np.float32([[0,0],[0,h2],[w2,h2],[w2,0]]).reshape(-1,1,2)), axis=0)

    [x_min, y_min] = np.int32(corners.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(corners.max(axis=0).ravel() + 0.5)

    translation = [-x_min, -y_min]
    H_translation = np.array([[1,0,translation[0]],
                              [0,1,translation[1]],
                              [0,0,1]])

    result = cv2.warpPerspective(base_img, H_translation @ H,
                                 (x_max - x_min, y_max - y_min))

    result[translation[1]:h2+translation[1],
           translation[0]:w2+translation[0]] = new_img

    return result