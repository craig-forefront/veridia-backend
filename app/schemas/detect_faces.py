"""
This module defines the Pydantic models used for the face detection API responses.

The models include:
- FaceSize: Represents the size of a detected face.
- FaceDetection: Represents a detected face with various attributes.
- ImageSize: Represents the size of the image.
- DetectFacesResponse: Represents the response for the face detection API.
"""

from typing import List, Optional
from pydantic import BaseModel


class FaceSize(BaseModel):
    """
    Represents the size of a detected face.

    Attributes:
        width (float): The width of the face.
        height (float): The height of the face.
        area (float): The area of the face.
    """
    width: float
    height: float
    area: float


class FaceDetection(BaseModel):
    """
    Represents a detected face with various attributes.

    Attributes:
        bbox (List[float]): The bounding box of the face in the format [x1, y1, x2, y2].
        estimated_age (Optional[int]): The estimated age of the person.
        estimated_gender (Optional[int]): The estimated gender of the person.
        confidence (Optional[float]): The confidence score of the detection.
        embedding (Optional[List[float]]): The face embedding vector.
        face_size (FaceSize): The size of the detected face.
        key_points (List[List[float]]): The key points of the face.
    """
    bbox: List[float]
    estimated_age: Optional[int]
    estimated_gender: Optional[int]
    confidence: Optional[float]
    embedding: Optional[List[float]]
    face_size: FaceSize
    key_points: List[List[float]]


class ImageSize(BaseModel):
    """
    Represents the size of the image.

    Attributes:
        width (int): The width of the image.
        height (int): The height of the image.
    """
    width: int
    height: int


class DetectFacesResponse(BaseModel):
    """
    Represents the response for the face detection API.

    Attributes:
        image_size (ImageSize): The size of the image.
        faces (List[FaceDetection]): The list of detected faces.
    """
    image_size: ImageSize
    faces: List[FaceDetection]
