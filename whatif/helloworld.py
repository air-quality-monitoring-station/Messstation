from sense_hat import SenseHat

sense = SenseHat()



mibar = sense.get_pressure()
print(mibar)
intbar = int(mibar)
strbar = str(intbar)
sense.show_message(strbar + "mB")

temp = sense.get_temperature()
print(temp)
inttemp = int(temp)
strtemp = str(inttemp)
sense.show_message(strtemp + "c")

hum = sense.get_humidity()
print(hum)
inthum = int(hum)
strhum = str(inthum)
sense.show_message(strhum + "%")
