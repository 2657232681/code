import sys

sys.path.append("yolov5")
import json
import re
import time
import traceback
import uuid
from .models import *
from django.shortcuts import render
from datetime import datetime
from PIL import Image as PImage
import os, numpy as np
from io import BytesIO
from demo import ocr
import matplotlib.pyplot as plt
import base64
from django.http import JsonResponse
from app.views import checkLogin


@checkLogin
def nets(request):
    img = request.POST["image"].split(",")[1]
    img = PImage.open(BytesIO(base64.b64decode(img))).convert("RGB")
    image_path = f"app/static/images/{uuid.uuid4()}.jpg"
    img.save(image_path, "jpeg")

    t = time.time()
    img1s, result = ocr(np.array(img)[..., ::-1])
    ocr_time = time.time() - t

    img = PImage.fromarray(img1s[..., ::-1])
    img.save(image_path.replace(".jpg", "_pred.jpg"), "jpeg")

    for x in result:
        try:
            obj = Object.objects.get(name=x["label"])
            x['detail'] = obj.to_dict()
        except:
            x['detail'] = {}

    log = OcrLog.objects.create(username=request.user.username,
                                result=json.dumps(result, ensure_ascii=False),
                                target=image_path.replace(".jpg", "_pred.jpg").replace("app/", "/"),
                                origin=image_path.replace("app/", "/"),
                                ocr_time=ocr_time)

    return JsonResponse({"code": 200,
                         "data": log.to_dict()})
