import os

import requests
from apng import APNG

WIDTH = 640
HEIGHT = 480
ITERATIONS = 500
OUTPUT_DIR = "frames"
NUM_FRAMES = 600
DELAY = 60


keyframes = [
    (-0.75, 0.0, 2.5),
    (-1.2, 0.0, 1.0),
    (-1.35, 0.05, 0.5),
    (-1.0, -0.2, 0.2),
    (-0.8, 0.2, 0.1),
    (-0.743643887037151, 0.1318259, 0.01),
    (-0.743643887037151, 0.1318259, 0.0005),
    (-0.743643887037151, 0.1318259, 0.01),
    (-0.748, 0.1, 0.005),
    (-0.75, 0.0, 0.5),
    (-0.75, 0.0, 2.5),
]


def ease_in_out(t):
    return 3 * t**2 - 2 * t**3


def interpolate_keyframes(kf0, kf1, t):
    t = ease_in_out(t)
    (re0, im0, scale0) = kf0
    (re1, im1, scale1) = kf1
    re = re0 + (re1 - re0) * t
    im = im0 + (im1 - im0) * t
    scale = scale0 * (scale1 / scale0) ** t
    return re, im, scale


def generate_frames():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    frames = []
    seg_frames = NUM_FRAMES // (len(keyframes) - 1)

    frame_idx = 0
    for i in range(len(keyframes) - 1):
        for j in range(seg_frames):
            t = j / seg_frames
            re_c, im_c, scale = interpolate_keyframes(
                keyframes[i], keyframes[i + 1], t
            )

            aspect_ratio = HEIGHT / WIDTH
            re_min = re_c - scale
            re_max = re_c + scale
            im_min = im_c - scale * aspect_ratio
            im_max = im_c + scale * aspect_ratio

            payload = {
                "width": WIDTH,
                "height": HEIGHT,
                "iterations": ITERATIONS,
                "re_min": re_min,
                "re_max": re_max,
                "im_min": im_min,
                "im_max": im_max,
                "kind": "png",
            }

            print(
                f"Rendering frame {frame_idx}: "
                f"center=({re_c:.6f},{im_c:.6f}), scale={scale:.8f}"
            )
            try:
                r = requests.post(
                    "http://localhost:8080/generate", json=payload
                )
                r.raise_for_status()
                filename = f"{OUTPUT_DIR}/frame_{frame_idx:04d}.png"
                with open(filename, "wb") as f:
                    f.write(r.content)
                frames.append(filename)
                frame_idx += 1
            except requests.RequestException as e:
                print(f"Error generating frame {frame_idx}: {e}")
                break

    return frames


def create_apng(frames, output_file="walk.png"):
    apng = APNG()
    for frame in frames:
        apng.append_file(frame, delay=DELAY)
    apng.save(output_file)
    print(f"Saved looping animation to {output_file}")


if __name__ == "__main__":
    frames = generate_frames()
    if frames:
        create_apng(frames)
