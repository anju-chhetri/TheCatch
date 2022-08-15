from src.imageRecog import ImageRecog
import numpy as np




paths = ["/home/anju_chhetri/Desktop/DBMSPhotos/trib81.jpg", "/home/anju_chhetri/Desktop/DBMSPhotos/trib_db.jpg", "/home/anju_chhetri/Desktop/DBMSPhotos/trib_db1.jpg", "/home/anju_chhetri/Desktop/DBMSPhotos/sandesh_db.jpg"]
for path in paths:
    detect = ImageRecog(path)
    (name, conf) = detect.detection()
    print(path)
    print(f"{name} conf: {conf}")
