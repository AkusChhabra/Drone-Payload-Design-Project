import cv2
import numpy as np
import urllib.request
import serial.tools.list_ports
url = 'http://192.168.182.245/cam-hi.jpg'
cap = cv2.VideoCapture(url)
whT = 320
confThreshold = 0.5
nmsThreshold = 0.3
classesfile = 'coco.names'
classNames = []
yolo_net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
classes = [line.strip() for line in f]
layer_names = yolo_net.getUnconnectedOutLayersNames()
ports = serial.tools.list_ports.comports()
serial_inst = serial.Serial()
ports_list = []
for port in ports:
ports_list.append(str(port))

print(str(port))
val: str = input('Select Port: COM')
for i in range(len(ports_list)):
if ports_list[i].startswith(f'COM{val}'):
port_var = f'COM{val}'
print(port_var)
serial_inst.baudrate = 115200
serial_inst.port = port_var
serial_inst.open()

while True:
try:
with urllib.request.urlopen(url) as response:
img_array = np.frombuffer(response.read(), dtype=np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
height, width = img.shape[:2]
# Prepare image for YOLO
blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416),

swapRB=True, crop=False)

yolo_net.setInput(blob)
detections = yolo_net.forward(layer_names)
# Process YOLO output
for detection in detections:
for obj in detection:
scores = obj[5:]
class_id = np.argmax(scores)
confidence = scores[class_id]
if confidence > 0.5 and classes[class_id] ==

"aeroplane":

print("Aeroplane detected!")
command = 'DROP'
print(command)
serial_inst.write(command.encode('utf-8'))

if serial_inst.in_waiting > 0:
serial_data =
serial_inst.readline().decode('utf-8').strip()

print("Arduino says:", serial_data)

cv2.imshow("YOLOv3 Object Detection", img)
if cv2.waitKey(1) & 0xFF == ord('q'):
break
except Exception as e:
print(f"Error: {e}")

# Release resources
cv2.destroyAllWindows()