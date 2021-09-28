import cv2
import matplotlib.image as mpimg


IMAGE_PATH = '../src/data/img/'
template = mpimg.imread(f'{IMAGE_PATH}template.png')
image = mpimg.imread(f'{IMAGE_PATH}full.png')

# convertendo imagem template e source para escala de cinza
# retorna um array
imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

result = cv2.matchTemplate(
    imageGray, templateGray,
	cv2.TM_CCOEFF_NORMED  # coeficiente de correlação normalizado
    # template matching method
)

(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)  #  encontrar o local com o maior valor -> a correspondência mais provável

# extraindo as coordenadas e bounding box
(startX, startY) = maxLoc
# adicionando a largura e altura do modelo às coordenadas startX e endX
endX = startX + template.shape[1]
endY = startY + template.shape[0]

# Desenhando a caixa delimitadora (bounding box) detectada na imagem
cv2.rectangle(image, (startX, startY), (endX, endY), (255, 0, 0), 3)
cv2.imshow("Output", image)  # exibe a imagem
cv2.waitKey(0)
