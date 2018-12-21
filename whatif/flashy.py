from sense_hat import SenseHat
sense = SenseHat()
sense.clear()

sense.show_message("Humidity")
humidity = sense.get_humidity()
print(humidity)
numba = str(humidity)
sense.show_message(numba + "%")

sense.show_message("Temperature")
temp = sense.get_temperature()
print(temp)
numba = str(temp)
sense.show_message(numba + "%")


