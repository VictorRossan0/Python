import cv2
import mediapipe as mp

webcam = cv2.VideoCapture(0)  # Para conectar o Python com a nossa webcam.

reconhecimento_rosto = mp.solutions.face_detection  # Ativando a solução de reconhecimento de rosto
desenho = mp.solutions.drawing_utils  # Ativando a solução de desenho
reconhecedor_rosto = reconhecimento_rosto.FaceDetection()  # Criando o item que consegue ler uma imagem e reconhecer os rostos

while webcam.isOpened():
    validacao, frame = webcam.read()  # Lê a imagem da webcam
    if not validacao:
        break
    imagem = frame
    lista_rostos = reconhecedor_rosto.process(imagem)  # Usa o reconhecedor para criar uma lista com os rostos reconhecidos
    
    if lista_rostos.detections:  # Caso algum rosto tenha sido reconhecido
        for rosto in lista_rostos.detections:  # Para cada rosto que foi reconhecido
            desenho.draw_detection(imagem, rosto)  # Desenha o rosto na imagem
    
    cv2.imshow("Rostos na sua webcam", imagem)  # Mostra a imagem da webcam para a gente
    
    # Salvar imagem com os rostos desenhados
    cv2.imwrite("image.png", imagem)  # Salva a imagem com os rostos desenhados
    
    if cv2.waitKey(5) == 27:  # ESC
        break

webcam.release()  # Encerra a conexão com a webcam
cv2.destroyAllWindows()  # Fecha a janela que mostra o que a webcam está vendo
