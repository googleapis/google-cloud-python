# Copyright 2016 Google Inc.
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
from google.cloud.vision.likelihood import Likelihood
from google.cloud.vision.geometry import Position


class Angles(object):
    """Angles representing the positions of a face."""
    def __init__(self, roll, pan, tilt):
        self._roll = roll
        self._pan = pan
        self._tilt = tilt

    @classmethod
    def from_api_repr(cls, response):
        """Factory: construct the angles from an Vision API response.

        :rtype: :class:`~google.cloud.vision.face.Angles`
        :returns: An `Angles` instance with data parsed from `response`.
        """
        roll = response['rollAngle']
        pan = response['panAngle']
        tilt = response['tiltAngle']

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
    def from_api_repr(cls, response):
        """Factory: construct `Emotions` from Vision API response.

        :type response: dict
        :param response: Response dictionary representing a face.

        :rtype: :class:`~google.cloud.vision.face.Emotions`
        :returns: Populated instance of `Emotions`.
        """
        joy_likelihood = Likelihood[response['joyLikelihood']]
        sorrow_likelihood = Likelihood[response['sorrowLikelihood']]
        surprise_likelihood = Likelihood[response['surpriseLikelihood']]
        anger_likelihood = Likelihood[response['angerLikelihood']]

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
    def from_api_repr(cls, response):
        """Factory: construct an instance of a Face from an API response

        :type response: dict
        :param response: Face annotation dict returned from the Vision API.

        :rtype: :class:`~google.cloud.vision.face.Face`
        :returns: A instance of `Face` with data parsed from `response`.
        """
        angles = Angles.from_api_repr(response)
        bounds = Bounds.from_api_repr(response['boundingPoly'])
        detection_confidence = response['detectionConfidence']
        emotions = Emotions.from_api_repr(response)
        fd_bounds = FDBounds.from_api_repr(response['fdBoundingPoly'])
        headwear_likelihood = Likelihood[response['headwearLikelihood']]
        image_properties = FaceImageProperties.from_api_repr(response)
        landmarks = Landmarks(response['landmarks'])
        landmarking_confidence = response['landmarkingConfidence']

        return cls(angles, bounds, detection_confidence, emotions, fd_bounds,
                   headwear_likelihood, image_properties, landmarks,
                   landmarking_confidence)

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
    def from_api_repr(cls, response):
        """Factory: construct image properties from image.

        :rtype: :class:`~google.cloud.vision.face.FaceImageProperties`
        :returns: Instance populated with image property data.
        """
        blurred = Likelihood[response['blurredLikelihood']]
        underexposed = Likelihood[response['underExposedLikelihood']]

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

    See:
    https://cloud.google.com/vision/reference/rest/v1/images/annotate#Type_1
    """
    UNKNOWN_LANDMARK = 'UNKNOWN_LANDMARK'
    LEFT_EYE = 'LEFT_EYE'
    RIGHT_EYE = 'RIGHT_EYE'
    LEFT_OF_LEFT_EYEBROW = 'LEFT_OF_LEFT_EYEBROW'
    RIGHT_OF_LEFT_EYEBROW = 'RIGHT_OF_LEFT_EYEBROW'
    LEFT_OF_RIGHT_EYEBROW = 'LEFT_OF_RIGHT_EYEBROW'
    RIGHT_OF_RIGHT_EYEBROW = 'RIGHT_OF_RIGHT_EYEBROW'
    MIDPOINT_BETWEEN_EYES = 'MIDPOINT_BETWEEN_EYES'
    NOSE_TIP = 'NOSE_TIP'
    UPPER_LIP = 'UPPER_LIP'
    LOWER_LIP = 'LOWER_LIP'
    MOUTH_LEFT = 'MOUTH_LEFT'
    MOUTH_RIGHT = 'MOUTH_RIGHT'
    MOUTH_CENTER = 'MOUTH_CENTER'
    NOSE_BOTTOM_RIGHT = 'NOSE_BOTTOM_RIGHT'
    NOSE_BOTTOM_LEFT = 'NOSE_BOTTOM_LEFT'
    NOSE_BOTTOM_CENTER = 'NOSE_BOTTOM_CENTER'
    LEFT_EYE_TOP_BOUNDARY = 'LEFT_EYE_TOP_BOUNDARY'
    LEFT_EYE_RIGHT_CORNER = 'LEFT_EYE_RIGHT_CORNER'
    LEFT_EYE_BOTTOM_BOUNDARY = 'LEFT_EYE_BOTTOM_BOUNDARY'
    LEFT_EYE_LEFT_CORNER = 'LEFT_EYE_LEFT_CORNER'
    RIGHT_EYE_TOP_BOUNDARY = 'RIGHT_EYE_TOP_BOUNDARY'
    RIGHT_EYE_RIGHT_CORNER = 'RIGHT_EYE_RIGHT_CORNER'
    RIGHT_EYE_BOTTOM_BOUNDARY = 'RIGHT_EYE_BOTTOM_BOUNDARY'
    RIGHT_EYE_LEFT_CORNER = 'RIGHT_EYE_LEFT_CORNER'
    LEFT_EYEBROW_UPPER_MIDPOINT = 'LEFT_EYEBROW_UPPER_MIDPOINT'
    RIGHT_EYEBROW_UPPER_MIDPOINT = 'RIGHT_EYEBROW_UPPER_MIDPOINT'
    LEFT_EAR_TRAGION = 'LEFT_EAR_TRAGION'
    RIGHT_EAR_TRAGION = 'RIGHT_EAR_TRAGION'
    LEFT_EYE_PUPIL = 'LEFT_EYE_PUPIL'
    RIGHT_EYE_PUPIL = 'RIGHT_EYE_PUPIL'
    FOREHEAD_GLABELLA = 'FOREHEAD_GLABELLA'
    CHIN_GNATHION = 'CHIN_GNATHION'
    CHIN_LEFT_GONION = 'CHIN_LEFT_GONION'
    CHIN_RIGHT_GONION = 'CHIN_RIGHT_GONION'


class FDBounds(BoundsBase):
    """The bounding polygon of just the skin portion of the face."""


class Landmark(object):
    """A face-specific landmark (for example, a face feature, left eye)."""
    def __init__(self, position, landmark_type):
        self._position = position
        self._landmark_type = landmark_type

    @classmethod
    def from_api_repr(cls, response_landmark):
        """Factory: construct an instance of a Landmark from a response.

        :type response_landmark: dict
        :param response_landmark: Landmark representation from Vision API.

        :rtype: :class:`~google.cloud.vision.face.Landmark`
        :returns: Populated instance of `Landmark`.
        """
        position = Position.from_api_repr(response_landmark['position'])
        landmark_type = LandmarkTypes[response_landmark['type']]
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
    """Landmarks detected on a face represented as properties."""
    def __init__(self, landmarks):
        for landmark_response in landmarks:
            landmark = Landmark.from_api_repr(landmark_response)
            setattr(self, landmark.landmark_type.value.lower(), landmark)
