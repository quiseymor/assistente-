import pyttsx3	


engine = pyttsx3.init()
engine.setProperty('rate', 200)				#скорость речи


def speaker(text):
	engine.say(text)
	engine.runAndWait()

	