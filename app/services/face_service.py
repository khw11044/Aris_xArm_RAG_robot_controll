import cv2
import chromadb
import numpy as np
import mediapipe as mp
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch

# 전역 상태 저장소
global_face_state = {
    "previous_embeddings": None  # 단일 임베딩 값 저장
}

def update_global_embeddings(embedding):
    """전역 상태에 임베딩을 업데이트합니다."""
    global_face_state["previous_embeddings"] = embedding

def get_global_embeddings():
    """전역 상태에서 임베딩을 가져옵니다."""
    return global_face_state["previous_embeddings"]

class FaceService:
    def __init__(self, db_path='./faces', similarity_threshold=0.15):
        # Mediapipe Face Detection 초기화
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.4
        )

        # ChromaDB 초기화
        self.client = chromadb.PersistentClient(db_path)
        self.db = self.client.get_or_create_collection(
            name='facedb',
            metadata={"hnsw:space": 'cosine'}
        )

        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.mtcnn = MTCNN(keep_all=True, device=self.device)
        self.resnet = InceptionResnetV1(pretrained='casia-webface').eval().to(self.device)
        

        # 유사도 임계값 설정
        self.similarity_threshold = similarity_threshold

        # 이전 프레임의 바운딩 박스와 라벨
        self.previous_bboxes = []
        self.previous_labels = []
        self.previous_embeddings = None
        self.force_recognition = False  # 얼굴 인식을 강제할 플래그

    def detect_faces(self, image):
        """얼굴 탐지를 수행하고 바운딩 박스를 반환합니다."""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(image_rgb)

        bboxes = []
        if results.detections:
            h, w, _ = image.shape
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x1 = int(bbox.xmin * w )
                y1 = int(bbox.ymin * h )
                x2 = int((bbox.xmin + bbox.width) * w )
                y2 = int((bbox.ymin + bbox.height) * h )
                bboxes.append((x1, y1, x2, y2))
        return bboxes

    def recognize_faces(self, image, bboxes):
        """탐지된 얼굴을 인식하여 라벨을 반환합니다."""
        labels = []
        for bbox in bboxes:
            x1, y1, x2, y2 = bbox
            cropped_face = image[y1:y2, x1:x2]
            if cropped_face.size > 0:
                cropped_face_rgb = Image.fromarray(cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB))
                facevector = self.mtcnn(cropped_face_rgb)
                
                if facevector is None:
                    continue
                
                embedding = self.resnet(facevector.to(self.device)).detach().cpu().numpy()[0]
                
                # ChromaDB에서 유사한 얼굴 검색
                search_results = self.db.query(
                    query_embeddings=[embedding.tolist()],
                    n_results=1,
                    include=["distances", "metadatas"]
                )
                # print('search_results["distances"][0][0]:', search_results["distances"][0][0])
                try:
                    if search_results["distances"][0][0] < self.similarity_threshold:
                        label = search_results["metadatas"][0][0]["filename"]
                    else:
                        label = "Unknown"
                        self.previous_embeddings = embedding  # Unknown일 때만 임베딩 저장
                        update_global_embeddings(embedding)  # 전역 상태에 업데이트
                except (IndexError, KeyError):
                    label = "Unknown"
                    self.previous_embeddings = embedding  # 검색 결과가 없을 때도 Unknown으로 처리
                    update_global_embeddings(embedding)  # 전역 상태에 업데이트
                labels.append(label)
        return labels

    def process_frame(self, image, frame_count):
        """단일 프레임을 처리하여 얼굴 탐지 및 인식을 수행합니다."""
        image = cv2.flip(image, 1)
        bboxes = self.detect_faces(image)
        if self.force_recognition or len(bboxes) != len(self.previous_bboxes):
            labels = self.recognize_faces(image, bboxes)
            self.force_recognition = False  # 강제 인식 플래그 초기화, 한번 인식 수행하면 한번 작동 
        else:
            labels = self.previous_labels

        self.previous_bboxes = bboxes
        self.previous_labels = labels

        if bboxes and not labels:
            self.force_recognition = True
        
        # 바운딩 박스 및 라벨 그리기
        for bbox, label in zip(bboxes, labels):
            x1, y1, x2, y2 = bbox
            
            if label != "Unknown":
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 255, 0) if label != "Unknown" else (0, 0, 255), 2)
            else:
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                
                
        return image
    
    def trigger_recognition(self):
        """얼굴 인식을 강제하도록 플래그 설정."""
        self.force_recognition = True

    def close(self):
        """리소스 해제."""
        if self.face_detection is not None:
            try:
                self.face_detection.close()
                self.face_detection = None  # 인스턴스를 None으로 설정하여 닫힘 상태 표시
            except ValueError as e:
                print(f"Face detection already closed: {e}")
        else:
            print("Face detection was already closed.")

# 싱글톤 인스턴스 생성
face_service_instance = FaceService()
