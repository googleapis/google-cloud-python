# Copyright 2016 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Face class representing the Vision API's face detection response."""


from enum import Enum

from google.cloud.vision.geometry import BoundsBase
from google.cloud.vision.likelihood import _get_pb_likelihood
from google.cloud.vision.likelihood import Likelihood
from google.cloud.vision.geometry import Position


class Angles(object):
    """Angles representing the positions of a face."""
    def __init__(self, roll, pan, tilt):
        self._roll = roll
        self._pan = pan
        self._tilt = tilt

    @classmethod
    def from_api_repr(cls, angle):
        """Factory: construct the angles from an Vision API response.

        :type angle: dict
        :param angle: Dictionary representation of an angle.

        :rtype: :class:`~google.cloud.vision.face.Angles`
        :returns: An `Angles` instance with data parsed from `response`.
        """
        roll = angle['rollAngle']
        pan = angle['panAngle']
        tilt = angle['tiltAngle']

        return cls(roll, pan, tilt)

    @classmethod
    def from_pb(cls, angle):
        """Factory: convert protobuf Angle object to local Angle object.

        :type angle: :class:`~google.cloud.vision_v1.proto.\
                     image_annotator_pb2.FaceAnnotation`
        :param angle: Protobuf ``FaceAnnotation`` response with angle data.

        :rtype: :class:`~google.cloud.vision.face.Angles`
        :returns: Instance of ``Angles``.
        """
        roll = angle.roll_angle
        pan = angle.pan_angle
        tilt = angle.tilt_angle

        return cls(roll, pan, tilt)

    @property
    def roll(self):
        """Roll angle of face.

        :rtype: float
        :returns: Roll angle of face in degrees.
        """
        return self._roll

    @property
    def pan(self):
        """Pan angle of face.

        :rtype: float
        :returns: Pan angle of face in degrees.
        """
        return self._pan

    @property
    def tilt(self):
        """Tilt angle of face.

        :rtype: float
        :returns: Tilt angle of face in degrees.
        """
        return self._tilt


class Bounds(BoundsBase):
    """The bounding polygon of the entire face."""


class Emotions(object):
    """Emotions displayed by the face detected in an image."""
    def __init__(self, joy_likelihood, sorrow_likelihood,
                 surprise_likelihood, anger_likelihood):
        self._joy_likelihood = joy_likelihood
        self._sorrow_likelihood = sorrow_likelihood
        self._surprise_likelihood = surprise_likelihood
        self._anger_likelihood = anger_likelihood

    @classmethod
    def from_api_repr(cls, emotions):
        """Factory: construct ``Emotions`` from Vision API response.

        :type emotions: dict
        :param emotions: Response dictionary representing a face.

        :rtype: :class:`~google.cloud.vision.face.Emotions`
        :returns: Populated instance of ``Emotions``.
        """
        joy_likelihood = Likelihood[emotions['joyLikelihood']]
        sorrow_likelihood = Likelihood[emotions['sorrowLikelihood']]
        surprise_likelihood = Likelihood[emotions['surpriseLikelihood']]
        anger_likelihood = Likelihood[emotions['angerLikelihood']]

        return cls(joy_likelihood, sorrow_likelihood, surprise_likelihood,
                   anger_likelihood)

    @classmethod
    def from_pb(cls, emotions):
        """Factory: construct ``Emotions`` from Vision API response.

        :type emotions: :class:`~google.cloud.vision_v1.proto.\
                        image_annotator_pb2.FaceAnnotation`
        :param emotions: Response dictionary representing a face with emotions.

        :rtype: :class:`~google.cloud.vision.face.Emotions`
        :returns: Populated instance of ``Emotions``.
        """
        joy_likelihood = _get_pb_likelihood(emotions.joy_likelihood)
        sorrow_likelihood = _get_pb_likelihood(emotions.sorrow_likelihood)
        surprise_likelihood = _get_pb_likelihood(emotions.surprise_likelihood)
        anger_likelihood = _get_pb_likelihood(emotions.anger_likelihood)

        return cls(joy_likelihood, sorrow_likelihood, surprise_likelihood,
                   anger_likelihood)

    @property
    def anger(self):
        """Likelihood of anger in detected face.

        :rtype: str
        :returns: String derived from
                  :class:`~google.cloud.vision.face.Likelihood`.
        """
        return self._anger_likelihood

    @property
    def joy(self):
        """Likelihood of joy in detected face.

        :rtype: str
        :returns: String derived from
                  :class:`~google.cloud.vision.face.Likelihood`.
        """
        return self._joy_likelihood

    @property
    def sorrow(self):
        """Likelihood of sorrow in detected face.

        :rtype: str
        :returns: String derived from
                  :class:`~google.cloud.vision.face.Likelihood`.
        """
        return self._sorrow_likelihood

    @property
    def surprise(self):
        """Likelihood of surprise in detected face.

        :rtype: str
        :returns: String derived from
                  :class:`~google.cloud.vision.face.Likelihood`.
        """
        return self._surprise_likelihood


class Face(object):
    """Representation of a face found by the Vision API"""

    def __init__(self, angles, bounds, detection_confidence, emotions,
                 fd_bounds, headwear_likelihood, image_properties, landmarks,
                 landmarking_confidence):
        self._angles = angles
        self._bounds = bounds
        self._detection_confidence = detection_confidence
        self._emotions = emotions
        self._fd_bounds = fd_bounds
        self._headwear_likelihood = headwear_likelihood
        self._landmarks = landmarks
        self._landmarking_confidence = landmarking_confidence
        self._image_properties = image_properties

    @classmethod
    def from_api_repr(cls, face):
        """Factory: construct an instance of a Face from an API response

        :type face: dict
        :param face: Face annotation dict returned from the Vision API.

        :rtype: :class:`~google.cloud.vision.face.Face`
        :returns: A instance of `Face` with data parsed from `response`.
        """
        face_data = {
            'angles': Angles.from_api_repr(face),
            'bounds': Bounds.from_api_repr(face['boundingPoly']),
            'detection_confidence': face['detectionConfidence'],
            'emotions': Emotions.from_api_repr(face),
            'fd_bounds': FDBounds.from_api_repr(face['fdBoundingPoly']),
            'headwear_likelihood': Likelihood[face['headwearLikelihood']],
            'image_properties': FaceImageProperties.from_api_repr(face),
            'landmarks': Landmarks.from_api_repr(face['landmarks']),
            'landmarking_confidence': face['landmarkingConfidence'],
        }
        return cls(**face_data)

    @classmethod
    def from_pb(cls, face):
        """Factory: construct an instance of a Face from an protobuf response

        :type face: :class:`~google.cloud.vision_v1.proto.\
                       image_annotator_pb2.AnnotateImageResponse`
        :param face: ``AnnotateImageResponse`` from gRPC call.

        :rtype: :class:`~google.cloud.vision.face.Face`
        :returns: A instance of `Face` with data parsed from ``response``.
        """
        face_data = {
            'angles': Angles.from_pb(face),
            'bounds': Bounds.from_pb(face.bounding_poly),
            'detection_confidence': face.detection_confidence,
            'emotions': Emotions.from_pb(face),
            'fd_bounds': FDBounds.from_pb(face.fd_bounding_poly),
            'headwear_likelihood': _get_pb_likelihood(
                face.headwear_likelihood),
            'image_properties': FaceImageProperties.from_pb(face),
            'landmarks': Landmarks.from_pb(face.landmarks),
            'landmarking_confidence': face.landmarking_confidence,
        }
        return cls(**face_data)

    @property
    def anger(self):
        """Accessor to likelihood that the detected face is angry.

        :rtype: str
        :returns: String derived from
                  :class:`~google.cloud.vision.face.Likelihood`.
        """
        return self.emotions.anger

    @property
    def angles(self):
        """Accessor to the pan, tilt and roll angles of a Face.

        :rtype: :class:`~google.cloud.vision.face.Angles`
        :returns: Pan, tilt and roll angles of the detected face.
        """

        return self._angles

    @property
    def bounds(self):
        """Accessor to the bounding poly information of the detected face.

        :rtype: :class:`~google.cloud.vision.face.Bounds`
        :returns: An instance of ``Bounds`` which has a list of vertices.
        """
        return self._bounds

    @property
    def detection_confidence(self):
        """Face detection confidence score determined by the Vision API.

        :rtype: float
        :returns: Float representation of confidence ranging from 0 to 1.
        """
        return self._detection_confidence

    @property
    def emotions(self):
        """Accessor to the possible emotions expressed in the detected face.

        :rtype: :class:`~google.cloud.vision.face.Emotions`
        :returns: An instance of ``Emotions`` with joy, sorrow, anger, surprise
                  likelihood.
        """
        return self._emotions

    @property
    def fd_bounds(self):
        """Accessor to the skin area bounding poly of the detected face.

        :rtype: :class:`~google.cloud.vision.image.FDBounds`
        :returns: An instance of ``FDBounds`` which has a list of vertices.
        """
        return self._fd_bounds

    @property
    def headwear(self):
        """Headwear likelihood.

        :rtype: :class:`~google.cloud.vision.face.Likelihood`
        :returns: String representing the likelihood based on
                  :class:`~google.cloud.vision.face.Likelihood`
        """
        return self._headwear_likelihood

    @property
    def image_properties(self):
        """Image properties from imaged used in face detection.

        :rtype: :class:`~google.cloud.vision.face.FaceImageProperties`
        :returns: ``FaceImageProperties`` object with image properties.
        """
        return self._image_properties

    @property
    def joy(self):
        """Likelihood of joy in detected face.

        :rtype: str
        :returns: String derived from
                  :class:`~google.cloud.vision.face.Likelihood`.
        """
        return self.emotions.joy

    @property
    def landmarks(self):
        """Accessor to the facial landmarks detected in a face.

        :rtype: :class:`~google.cloud.vision.face.Landmarks`
        :returns: ``Landmarks`` object with facial landmarks as properies.
        """
        return self._landmarks

    @property
    def landmarking_confidence(self):
        """Landmarking confidence score determinged by the Vision API.

        :rtype: float
        :returns: Float representing the confidence of the Vision API in
                  determining the landmarks on a face.
        """
        return self._landmarking_confidence

    @property
    def sorrow(self):
        """Likelihood of sorrow in detected face.

        :rtype: str
        :returns: String derived from
                  :class:`~google.cloud.vision.face.Likelihood`.
        """
        return self.emotions.sorrow

    @property
    def surprise(self):
        """Likelihood of surprise in detected face.

        :rtype: str
        :returns: String derived from
                  :class:`~google.cloud.vision.face.Likelihood`.
        """
        return self.emotions.surprise


class FaceImageProperties(object):
    """A representation of the image properties from face detection."""
    def __init__(self, blurred_likelihood, underexposed_likelihood):
        self._blurred_likelihood = blurred_likelihood
        self._underexposed_likelihood = underexposed_likelihood

    @classmethod
    def from_api_repr(cls, face):
        """Factory: construct image properties from image.

        :type face: dict
        :param face: Dictionary representation of a ``Face``.

        :rtype: :class:`~google.cloud.vision.face.FaceImageProperties`
        :returns: Instance populated with image property data.
        """
        blurred = Likelihood[face['blurredLikelihood']]
        underexposed = Likelihood[face['underExposedLikelihood']]

        return cls(blurred, underexposed)

    @classmethod
    def from_pb(cls, face):
        """Factory: construct image properties from image.

        :type face: :class:`~google.cloud.vision_v1.proto.image_annotator_pb2.\
                    FaceAnnotation`
        :param face: Protobuf instace of `Face`.

        :rtype: :class:`~google.cloud.vision.face.FaceImageProperties`
        :returns: Instance populated with image property data.
        """
        blurred = _get_pb_likelihood(face.blurred_likelihood)
        underexposed = _get_pb_likelihood(face.under_exposed_likelihood)

        return cls(blurred, underexposed)

    @property
    def blurred(self):
        """Likelihood of the image being blurred.

        :rtype: str
        :returns: String representation derived from
                  :class:`~google.cloud.vision.face.Position`.
        """
        return self._blurred_likelihood

    @property
    def underexposed(self):
        """Likelihood that the image used for detection was underexposed.

        :rtype: str
        :returns: String representation derived from
                  :class:`~google.cloud.vision.face.Position`.
        """
        return self._underexposed_likelihood


class LandmarkTypes(Enum):
    """A representation of the face detection landmark types.

    See
    https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate#type_1
    """
    UNKNOWN_LANDMARK = 0
    LEFT_EYE = 1
    RIGHT_EYE = 2
    LEFT_OF_LEFT_EYEBROW = 3
    RIGHT_OF_LEFT_EYEBROW = 4
    LEFT_OF_RIGHT_EYEBROW = 5
    RIGHT_OF_RIGHT_EYEBROW = 6
    MIDPOINT_BETWEEN_EYES = 7
    NOSE_TIP = 8
    UPPER_LIP = 9
    LOWER_LIP = 10
    MOUTH_LEFT = 11
    MOUTH_RIGHT = 12
    MOUTH_CENTER = 13
    NOSE_BOTTOM_RIGHT = 14
    NOSE_BOTTOM_LEFT = 15
    NOSE_BOTTOM_CENTER = 16
    LEFT_EYE_TOP_BOUNDARY = 17
    LEFT_EYE_RIGHT_CORNER = 18
    LEFT_EYE_BOTTOM_BOUNDARY = 19
    LEFT_EYE_LEFT_CORNER = 20
    RIGHT_EYE_TOP_BOUNDARY = 21
    RIGHT_EYE_RIGHT_CORNER = 22
    RIGHT_EYE_BOTTOM_BOUNDARY = 23
    RIGHT_EYE_LEFT_CORNER = 24
    LEFT_EYEBROW_UPPER_MIDPOINT = 25
    RIGHT_EYEBROW_UPPER_MIDPOINT = 26
    LEFT_EAR_TRAGION = 27
    RIGHT_EAR_TRAGION = 28
    LEFT_EYE_PUPIL = 29
    RIGHT_EYE_PUPIL = 30
    FOREHEAD_GLABELLA = 31
    CHIN_GNATHION = 32
    CHIN_LEFT_GONION = 33
    CHIN_RIGHT_GONION = 34


class FDBounds(BoundsBase):
    """The bounding polygon of just the skin portion of the face."""


class Landmark(object):
    """A face-specific landmark (for example, a face feature, left eye).

    :type landmark_type: :class:`~google.cloud.vision.face.LandmarkTypes`
    :param landmark_type: Instance of ``LandmarkTypes``.

    :type position: :class:`~google.cloud.vision.face.Position`
    :param position:
    """
    def __init__(self, position, landmark_type):
        self._position = position
        self._landmark_type = landmark_type

    @classmethod
    def from_api_repr(cls, landmark):
        """Factory: construct an instance of a Landmark from a response.

        :type landmark: dict
        :param landmark: Landmark representation from Vision API.

        :rtype: :class:`~google.cloud.vision.face.Landmark`
        :returns: Populated instance of ``Landmark``.
        """
        position = Position.from_api_repr(landmark['position'])
        landmark_type = LandmarkTypes[landmark['type']]
        return cls(position, landmark_type)

    @classmethod
    def from_pb(cls, landmark):
        """Factory: construct an instance of a Landmark from a response.

        :type landmark: :class:`~google.cloud.vision_v1.proto.\
                        image_annotator_pb.FaceAnnotation.Landmark`
        :param landmark: Landmark representation from Vision API.

        :rtype: :class:`~google.cloud.vision.face.Landmark`
        :returns: Populated instance of ``Landmark``.
        """
        position = Position.from_pb(landmark.position)
        landmark_type = LandmarkTypes(landmark.type)
        return cls(position, landmark_type)

    @property
    def position(self):
        """Landmark position on face.

        :rtype: :class:`~google.cloud.vision.face.Position`
        :returns: Instance of `Position` with landmark coordinates.
        """
        return self._position

    @property
    def landmark_type(self):
        """Landmark type of facial feature.

        :rtype: str
        :returns: String representation of facial landmark type.
        """
        return self._landmark_type


class Landmarks(object):
    """Landmarks detected on a face represented as properties.

    :type landmarks: list
    :param landmarks: List of :class:`~google.cloud.vision.face.Landmark`.
    """
    def __init__(self, landmarks):
        for landmark in landmarks:
            setattr(self, landmark.landmark_type.name.lower(), landmark)

    @classmethod
    def from_api_repr(cls, landmarks):
        """Factory: construct facial landmarks from Vision API response.

        :type landmarks: dict
        :param landmarks: JSON face annotation.

        :rtype: :class:`~google.cloud.vision.face.Landmarks`
        :returns: Instance of ``Landmarks`` populated with facial landmarks.
        """
        return cls([Landmark.from_api_repr(landmark)
                    for landmark in landmarks])

    @classmethod
    def from_pb(cls, landmarks):
        """Factory: construct facial landmarks from Vision gRPC response.

        :type landmarks: :class:`~google.protobuf.internal.containers.\
                         RepeatedCompositeFieldContainer`
        :param landmarks: List of facial landmarks.

        :rtype: :class:`~google.cloud.vision.face.Landmarks`
        :returns: Instance of ``Landmarks`` populated with facial landmarks.
        """
        return cls([Landmark.from_pb(landmark) for landmark in landmarks])
