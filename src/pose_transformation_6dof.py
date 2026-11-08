import cv2
import numpy as np

def build_homogenous_matrix(rvec, tvec):
    """
    Constrói a Matriz de Transformação Homogênea 4x4 (T_camera^robot)
    a partir do vetor de rotação e vetor de translação obtidos via SolvePnP.
    """
    R_matrix, _ = cv2.Rodrigues(rvec)
    T_homogenous = np.eye(4, dtype=np.float32)
    T_homogenous[:3, :3] = R_matrix
    T_homogenous[:3, 3] = tvec.ravel()
    return T_homogenous

def estimate_6dof_pose(object_points, image_points, camera_matrix, dist_coeffs):
    """
    Resolve o problema Perspective-n-Point (PnP) para extração dos 6DoF
    em células de visão industrial VMT / Eisenmann.
    """
    success, rvec, tvec = cv2.solvePnP(
        object_points, 
        image_points, 
        camera_matrix, 
        dist_coeffs, 
        flags=cv2.SOLVEPNP_ITERATIVE
    )
    
    if not success:
        raise ValueError("[VMT Error] Falha na convergência iterativa do 6DoF pose estimation.")
        
    T_matrix = build_homogenous_matrix(rvec, tvec)
    
    print(f"[VMT 6DoF Engine] Translação (X, Y, Z) mm: {tvec.ravel()}")
    return rvec, tvec, T_matrix

if __name__ == "__main__":
    # Mock de pontos 3D da carroceria e projeção 2D na câmera
    obj_pts = np.array([[0, 0, 0], [200, 0, 0], [0, 200, 0], [200, 200, 0]], dtype=np.float32)
    img_pts = np.array([[300, 200], [500, 200], [300, 400], [500, 400]], dtype=np.float32)
    cam_mat = np.array([[1000, 0, 320], [0, 1000, 240], [0, 0, 1]], dtype=np.float32)
    dist = np.zeros((4, 1), dtype=np.float32)
    
    estimate_6dof_pose(obj_pts, img_pts, cam_mat, dist)
