import sys
from api import API_TOKEN
from datetime import datetime
import voice
import datetime
import requests	

import cv2
import numpy as np
import winsound

def weather():
	try:
		params = {'q': 'Saint Petersburg', 'units': 'metric', 'lang': 'ru', 'appid': API_TOKEN}
		response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
		if not response:
			raise
		w = response.json()
		voice.speaker(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")
		
	except:
		voice.speaker('Произошла ошибка')

def offBot():
	sys.exit()

def passive():
	pass

def datas():
    date = datetime.date.today()
    voice.speaker(date)

def time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    voice.speaker(current_time)


	
def calculate_distance(focal_length, real_width, pixel_width):
# Расчет расстояния до объекта по формуле пересчета фокусного расстояния, реальной ширины и ширины в пикселях
	distance = (real_width * focal_length) / pixel_width
	return distance

def draw_rectangle(image, x, y, width, height):
# Обводка объекта в квадрат на изображении
	cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)

def cam():
	camera = cv2.VideoCapture(0)
	focal_length = 500  #Фокусное расстояние камеры
	real_width = 10  #Ширина объекта 

	while True:
		# Получение кадра с камеры
		ret, frame = camera.read()
		if not ret:
			print("Failed to capture frame from camera")
			break

		# Обработка кадра
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (5, 5), 0)
		edges = cv2.Canny(gray, 50, 150)

		# Поиск контуров на изображении
		contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		for contour in contours:
			# Определение момента контура для определения центра объекта
			M = cv2.moments(contour)
			if M["m00"] != 0:
				cx = int(M["m10"] / M["m00"])
				cy = int(M["m01"] / M["m00"])

				# Расчет ширины объекта в пикселях
				x, y, width, height = cv2.boundingRect(contour)
				pixel_width = width

				# Расчет расстояния до объекта
				distance = calculate_distance(focal_length, real_width, pixel_width)

				# Обводка объекта в квадрат и отображение расстояния на изображении
				draw_rectangle(frame, x, y, width, height)
				cv2.putText(frame, f"Distance: {round(distance, 2)} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
							0.5, (0, 255, 0), 2)
				# Издание звука, если расстояние меньше 100 сантиметров
				if distance < 100:
					winsound.Beep(1000, 500)
		# Отображение изображения с обведенным объектом и расстоянием
		cv2.imshow("Camera", frame)

		# Прерывание цикла при нажатии клавиши 'q'
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	camera.release()
	cv2.destroyAllWindows()
	voice.speaker(cam)







