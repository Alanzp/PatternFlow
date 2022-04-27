import cv2
import mediapipe as mp
from processer.common.base import Base
from processer.common.parameter import Parameter

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


class MediaPipeHands(Base):
    def __init__(self):
        super().__init__()
        self.params["test"] = Parameter(current=5, min=0, max=100)
        # self.params["CoreSize"] = Parameter(current=9, min=3, max=100)

    def process(self, inputImage_BGR):
        with mp_hands.Hands(static_image_mode=True,
                            max_num_hands=2,
                            min_detection_confidence=0.5) as hands:
            results = hands.process(
                cv2.cvtColor(inputImage_BGR, cv2.COLOR_BGR2RGB))
            annotated_image = inputImage_BGR.copy()
            if not results.multi_hand_landmarks:
                return inputImage_BGR
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        return annotated_image
