import cv2
import os

#确定脚本位置
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print(f"Working directory: {os.getcwd()}")

#视频名称
video_path = "A1.mp4"

# 检测视频存在不
if not os.path.exists(video_path):
    print(f"ERROR: Video file '{video_path}' not found!")
    print(f"Please make sure '{video_path}' is in: {os.getcwd()}")
    exit()

# 截屏并输出到screenshots里面
output_dir = "screenshots"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("ERROR: Cannot open video file")
    exit()

#视频属性
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps

print(f"Video loaded successfully!")
print(f"  - FPS: {fps:.2f}")
print(f"  - Total frames: {total_frames}")
print(f"  - Duration: {duration:.1f} seconds")
print(f"  - Saving frames to: {output_dir}/")

# Extract frames
frame_interval = int(fps)  #每秒一帧
frame_count = 0
saved_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if frame_count % frame_interval == 0:
        timestamp = frame_count / fps
        save_path = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
        
        cv2.putText(frame, f"{timestamp:.1f}s", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imwrite(save_path, frame)
        saved_count += 1
        print(f"Saved frame {saved_count} at {timestamp:.1f}s")
    
    frame_count += 1

cap.release()
print(f"\nDONE! Extracted {saved_count} frames to '{output_dir}/'")
