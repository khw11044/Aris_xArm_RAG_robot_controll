import chromadb
import torch 
import datetime
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch

class SignInService:
    def __init__(self, db_path='./faces'):
        # ChromaDB 초기화
        self.client = chromadb.PersistentClient(db_path)
        self.db = self.client.get_or_create_collection(
            name='facedb',
            metadata={"hnsw:space": 'cosine'}
        )
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.mtcnn = MTCNN(keep_all=True, device=self.device)
        self.resnet = InceptionResnetV1(pretrained='casia-webface').eval().to(self.device)
        

    def get_next_user_id(self):
        """현재 ChromaDB에 등록된 벡터의 개수를 기반으로 다음 사용자 ID 생성"""
        count = self.db.count()
        return f"a{count + 1:04d}"

    def handle_signup_with_embedding(self, embedding):
        """
        이전 임베딩을 사용하여 회원가입을 처리합니다.
        
        Args:
            embedding (np.ndarray): 얼굴 임베딩 벡터.
        """
        try:
            user_id = self.get_next_user_id()
            
            # 현재 시간 추가
            current_time = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')

            # ChromaDB에 사용자 정보 추가
            self.db.add(
                ids=[user_id],
                embeddings=[embedding.tolist()],
                metadatas=[{"filename": user_id, "created_at": current_time}]
            )
            print(f"회원가입 성공: {user_id}")
        except Exception as e:
            print(f"회원가입 실패: {str(e)}")
            raise e

    def embed_face(self, face_image):
        """얼굴 이미지를 임베딩하여 반환"""
        facevector = self.mtcnn(face_image)
        embedding = self.resnet(facevector.to(self.device)).detach().cpu().numpy()[0]
                
        return embedding

    def add_face_to_chroma_db(self, face_image):
        """크롭된 얼굴 이미지를 임베딩하여 ChromaDB에 저장"""
        user_id = self.get_next_user_id()
        embedding = self.embed_face(face_image)

        # 현재 시간 추가
        current_time = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')

        # ChromaDB에 추가
        self.db.add(
            ids=[user_id],
            embeddings=[embedding.tolist()],
            metadatas=[{"filename": user_id, "created_at": current_time}]
        )
        print(f"Face embedding for {user_id} added successfully.")
        return user_id

    def handle_signup(self, session_id: str):
        """기본 테스트용 회원가입 처리를 수행"""
        print(f"회원가입 요청을 처리 중: 세션 ID {session_id}")
        
        # 예제: 기본 임베딩 데이터 사용
        default_face_image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        try:
            user_id = self.add_face_to_chroma_db(default_face_image)
            print(f"회원가입 성공: {user_id}")
        except Exception as e:
            print(f"회원가입 실패: {str(e)}")
            raise e
