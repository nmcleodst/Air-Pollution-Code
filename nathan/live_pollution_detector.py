import os
#comment so live pol can remember my changes
import sys
import time
import shutil
import subprocess
import cv2
import numpy as np
import onnxruntime as ort

MODEL_PATH = "/home/nvidia12/jetson-inference/python/training/classification/models/datase5t/resnet18.onnx"
IMAGE_SIZE = (224, 224)
THRESHOLD = 0.75
HIGH_CLASS_INDEX = 1
ALERT_COOLDOWN_SEC = 2.0

def ensure_display():
    if os.environ.get("DISPLAY"):
        return True

    xvfb = shutil.which("Xvfb")
    if xvfb:
        display_num = ":99"
        subprocess.Popen(
            [xvfb, display_num, "-screen", "0", "1280x720x24"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)
        os.environ["DISPLAY"] = display_num
        print(f"Started virtual display {display_num}")
        return True

    print("No DISPLAY detected and Xvfb is not installed.")
    return False

print("Python:", sys.executable)
print("Model exists:", os.path.exists(MODEL_PATH))

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

print("Input:", session.get_inputs()[0].shape)
print("Output:", session.get_outputs()[0].shape)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

show_window = ensure_display()
if show_window:
    try:
        cv2.namedWindow("Pollution Camera", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Pollution Camera", 1280, 720)
    except cv2.error as exc:
        print(f"Could not open display window: {exc}")
        show_window = False

alert_active = False
last_alert_time = 0.0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    blob = cv2.dnn.blobFromImage(
        frame,
        scalefactor=1.0 / 255.0,
        size=IMAGE_SIZE,
        mean=(0, 0, 0),
        swapRB=True,
        crop=False,
    )

    outputs = session.run([output_name], {input_name: blob})[0]
    values = np.asarray(outputs, dtype=np.float32).reshape(-1)

    if values.size <= HIGH_CLASS_INDEX:
        raise RuntimeError(f"Model output too small: {values.shape}")

    if np.all(values >= 0) and np.isclose(values.sum(), 1.0, atol=1e-3):
        probs = values
    else:
        values = values - np.max(values)
        exp_vals = np.exp(values)
        probs = exp_vals / exp_vals.sum()

    high_conf = float(probs[HIGH_CLASS_INDEX])

    now = time.time()

    if high_conf >= THRESHOLD:
        status = f"High pollution: {high_conf:.2%}"
        if (not alert_active) and (now - last_alert_time >= ALERT_COOLDOWN_SEC):
            print("air is polluted")
            alert_active = True
            last_alert_time = now
    else:
        status = f"Low/uncertain: {high_conf:.2%}"
        if alert_active:
            alert_active = False

    if show_window:
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(frame, "Press q to quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (40, 30, 0), 2)
        cv2.imshow("Pollution Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        print(status)

    time.sleep(0.1)

cap.release()
if show_window:
    cv2.destroyAllWindows()