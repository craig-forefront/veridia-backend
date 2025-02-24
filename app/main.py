import cv2
import insightface
import numpy as np
import uvicorn
from fastapi import FastAPI, File, UploadFile
from app.schemas.detect_faces import DetectFacesResponse

app = FastAPI()

# Initialize InsightFace for face analysis.
# (Make sure to install the version of insightface that provides 
# the FaceAnalysis API.)
face_app = insightface.app.FaceAnalysis(name='buffalo_l',
                                        providers=['CPUExecutionProvider']
                                        )
face_app.prepare(ctx_id=0, det_size=(640, 640))


@app.post("/detect_faces/", response_model=DetectFacesResponse)
async def detect_faces(file: UploadFile = File(...)):
    """
    Accepts an image file and returns detected faces along with bounding boxes,
    estimated age, gender, and a similar face query result from Qdrant.
    """
    # Read the uploaded file into memory.
    contents = await file.read()

    # Convert bytes data to a NumPy array and decode to an image.
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Get the size of the image.
    img_height, img_width, _ = img.shape

    # Use InsightFace to detect faces in the image.
    faces = face_app.get(img)

    results = []

    for face in faces:
        # Extract bounding box. Expected format: [x1, y1, x2, y2]
        bbox = face.bbox.tolist() if hasattr(face.bbox, 'tolist') else list(face.bbox)

        # Calculate the size of the detected face.
        face_width = bbox[2] - bbox[0]
        face_height = bbox[3] - bbox[1]
        face_size = {"width": face_width, "height": face_height, "area": face_width * face_height}

        # Extract age and gender estimates.
        age = getattr(face, 'age', None)
        gender = getattr(face, 'gender', None)

        # Extract the face embedding (if available).
        # This embedding can be used for similarity search in Qdrant.
        embedding = face.embedding.tolist() if hasattr(face, 'embedding') else None

        # Extract confidence score.
        confidence = getattr(face, 'det_score', None)

        # Extract key points.
        kps = face.kps.tolist() if hasattr(face.kps, 'tolist') else list(face.kps)

        results.append({
            "bbox": bbox,
            "estimated_age": age,
            "estimated_gender": int(gender) if gender is not None else None,
            "confidence": float(confidence) if confidence is not None else None,
            "embedding": embedding,   # Optionally include the embedding.
            "face_size": face_size,
            "key_points": kps
        })

    return {
        "image_size": {"width": img_width, "height": img_height},
        "faces": results
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    # Run the app with Uvicorn.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
