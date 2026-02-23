import cv2
import numpy as np


def merge_by_translation(base_img, new_img, x_dir = 1, y_dir = 1):
    """
    Merge di due immagini assumendo:
    - stessa scala
    - stessa rotazione
    - solo traslazione

    Gestisce shift positivi e negativi.
    
    Ritorna:
        merged_image
        (dx, dy)
        response
    """

    # Convert to grayscale float32 (richiesto da phaseCorrelate)
    gray_base = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
    gray_new = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    
    # edge detection
    edges_base = cv2.Canny(base_img, 50, 150)
    edges_new  = cv2.Canny(new_img, 50, 150)

    # Per usare phaseCorrelate devono avere stessa dimensione.
    # Quindi le portiamo su un canvas comune temporaneo.
    h = max(edges_base.shape[0], edges_new.shape[0])
    w = max(edges_base.shape[1], edges_new.shape[1])

    pad_base = np.zeros((h, w), dtype=np.float32)
    pad_new = np.zeros((h, w), dtype=np.float32)

    pad_base[:edges_base.shape[0], :edges_base.shape[1]] = edges_base
    pad_new[:edges_new.shape[0], :edges_new.shape[1]] = edges_new

    # Calcolo shift tramite applicazione finestra di Hanning 
    window = cv2.createHanningWindow((w, h), cv2.CV_32F)
    shift, response = cv2.phaseCorrelate(pad_base, pad_new, window)

    dx, dy = shift
    dx = int(round(dx)) * x_dir#
    dy = int(round(dy)) * y_dir

    # Calcolo coordinate min/max considerando shift
    h_base, w_base = base_img.shape[:2]
    h_new, w_new = new_img.shape[:2]

    x_min = min(0, dx)
    y_min = min(0, dy)
    x_max = max(w_base, dx + w_new)
    y_max = max(h_base, dy + h_new)

    canvas_w = x_max - x_min
    canvas_h = y_max - y_min

    # Offset per rendere tutto positivo
    offset_x = -x_min
    offset_y = -y_min

    canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

    # Inserisci base
    canvas[offset_y:offset_y + h_base,
           offset_x:offset_x + w_base] = base_img

    # Inserisci new
    canvas[offset_y + dy:offset_y + dy + h_new,
           offset_x + dx:offset_x + dx + w_new] = new_img

    return canvas, (dx, dy), response