import cv2
import mediapipe as mp
from processer.common.base import Base
from processer.common.parameter import Parameter

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)


class MediaPipeFaceMesh(Base):
    def __init__(self):
        super().__init__()
        self.params["thickness"] = Parameter(current=1, min=0, max=100)
        self.params["circle_radius"] = Parameter(current=1, min=0, max=100)
        # self.params["CoreSize"] = Parameter(current=9, min=3, max=100)

    def process(self, inputImage_BGR):
        with mp_face_mesh.FaceMesh(static_image_mode=True,
                                   max_num_faces=1,
                                   refine_landmarks=True,
                                   min_detection_confidence=0.5) as face_mesh:
            results = face_mesh.process(
                cv2.cvtColor(inputImage_BGR, cv2.COLOR_BGR2RGB))
            # Draw face detections of each face.
            if not results.multi_face_landmarks:
                return inputImage_BGR
            annotated_image = inputImage_BGR.copy()
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.
                    get_default_face_mesh_tesselation_style())
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.
                    get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.
                    get_default_face_mesh_iris_connections_style())
            return annotated_image
