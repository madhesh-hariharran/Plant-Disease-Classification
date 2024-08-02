from ultralyticsplus import YOLO, render_result
import numpy as np
import tensorflow as tf
import cv2
from PIL import Image


def crop(file_path):
    model = YOLO('foduucom/plant-leaf-detection-and-classification')
    model.overrides['conf'] = 0.25  # NMS confidence threshold
    model.overrides['iou'] = 0.45  # NMS IoU threshold
    model.overrides['agnostic_nms'] = False  # NMS class-agnostic
    model.overrides['max_det'] = 1000  # maximum number of detections per image
    image=file_path #the input image
    results = model.predict(image)

    if results[0].boxes.cls.tolist() == []:
        return False

    # Load the original image
    original_image = Image.open(image)

    # # Iterate over each detected bounding box
    for box in results[0].boxes.data.tolist():
    #     # Get the coordinates of the bounding box
        x_min, y_min, x_max, y_max = box[0],box[1],box[2],box[3]

    #     # Crop the image to the bounding box region
        cropped_image = original_image.crop((x_min, y_min, x_max, y_max))

    return cropped_image

    
model_path = r"Backend\Model"
model = tf.keras.models.load_model(model_path)
plant_class=['Pepper__bell___Bacterial_spot',
 'Pepper__bell___healthy',
 'Potato___Early_blight',
 'Potato___Late_blight',
 'Potato___healthy',
 'Tomato_Bacterial_spot',
 'Tomato_Early_blight',
 'Tomato__Target_Spot',
 'Tomato__Tomato_YellowLeaf__Curl_Virus',
 'Tomato__Tomato_mosaic_virus',
 'Tomato_healthy']
disease=[0,2,3,5,6,7,8,9]

def _predict(model, img):
    img=tf.expand_dims(img,0)
    predictions=model.predict(img)
    index=np.argmax(predictions[0])
    predicted_class=plant_class[np.argmax(predictions[0])]
    confidence =round(100*(np.max(predictions[0])),2)
    return index,predicted_class, confidence


def predict_disease(image_path=None, image_data=None):
    if image_data is None:
        cap = Image.open(image_path)
    else:
        cap = image_data

    live = np.array(cap)
    frame = tf.keras.preprocessing.image.smart_resize(live, (256, 256))
    index, predicted_class, confidence = _predict(model, frame)
    return (index, predicted_class, confidence)

def get_recommendation(key):
    recommended = treatment_dict.get(key)
    
    return recommended

def get_cause(key):
    cause = root_cause_dict.get(key)
    
    return cause

treatment_dict = {
    'Pepper__bell___Bacterial_spot': [
        "Copper sprays",
        "Treat seeds by soaking them for 2 minutes in a 10% chlorine bleach solution (1 part bleach; 9 parts water)",
        "Organic fungicide"
    ],
    'Potato___Early_blight': [
        "Protectant fungicides such as mancozeb and chlorothalonil",
        "Disinfect your pruning shears (one part bleach to 4 parts water)",
        "Prune or stake plants to improve air circulation"
    ],
    'Potato___Late_blight': [
        "Apply fungicides with a spore-killing effect (fluazinam-containing fungicides, Ranman Top)",
        "Dithane (mancozeb) MZ or you can also use Tattoo C or Acrobat MZ"
    ],
    'Tomato_Bacterial_spot': [
        "Copper fungicides, or copper plus mancozeb"
    ],
    'Tomato_Early_blight': [
        "Conika Fungicide, Kasugamycin + Copper Oxychloride",
        "Kocide Fungicide, Copper Hydroxide",
        "Dhanuka M45 Fungicide, Mancozeb"
    ],
    'Tomato__Target_Spot': [
        "Fungicides: Chlorothalonil, Azoxystrobin, Pyraclostrobin, Boscalid"
    ],
    'Tomato__Tomato_YellowLeaf__Curl_Virus': [
        "Azadirachtin (Neem), pyrethrin or insecticidal soap",
        "Yellow sticky traps @ 5nos./ac",
        "Remove alternate weed host - Abutilon indicum",
        "Spraying Dimethoate 30 EC @ 200 ml/ac or Methyl demeton 25 EC @ 200 ml/ac or Thiamethoxam 25 WG @ 200 g/ac or Imidacloprid 17.8 SL @ 200 ml/ac"
    ]
}

root_cause_dict = {
    'Pepper__bell___Bacterial_spot': 'Bacterial infection caused by Xanthomonas campestris bacteria',
    'Potato___Early_blight': 'Fungal infection caused by Alternaria solani',
    'Potato___Late_blight': 'Fungal infection caused by Phytophthora infestans',
    'Tomato_Bacterial_spot':'Bacterial infection caused by Xanthomonas species bacteria',
    'Tomato_Early_blight': 'Fungal infection caused by Alternaria solani',
    'Tomato__Target_Spot': 'Fungal infection caused by Corynespora cassiicola',
    'Tomato__Tomato_YellowLeaf__Curl_Virus': 'Viral infection caused by Tomato yellow leaf curl virus (TYLCV)',
    'Tomato__Tomato_mosaic_virus':'Viral infection caused by Tomato mosaic virus (ToMV)'
}

