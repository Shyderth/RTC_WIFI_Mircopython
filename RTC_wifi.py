from machine import Pin, I2C, RTC
from sh1106 import SH1106_I2C
import network, urequests, utime

ssid = 'FAMILIA AREVALO'
password = 'Cdp1006691858'
url = "https://worldtimeapi.org/api/timezone/America/Bogota"
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
width = 128
height = 64

oled = SH1106_I2C(width,height,i2c,rotate=180)
oled.text("Conectando...",0,2)
oled.show()

rtc = RTC()

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
if wifi.isconnected():
    wifi.disconnect()
if not wifi.isconnected():
    wifi.connect(ssid, password)
#wifi.scan()
#wifi.connect("Daniela", "jhon0418")

while not wifi.isconnected():
    pass

print(f"IP: {wifi.ifconfig()[0]}\n")
oled.text("Conectado con IP: ",0,25)
oled.text("" + str(wifi.ifconfig()[0]),0,35)
oled.show()

ultimaOpcion = 0
intervaloPet = 60  #s

while True:
    
    if not wifi.isconnected():
        print("Fallo de conexion")
        
    if (utime.time() - ultimaOpcion) >= intervaloPet:
        response = urequests.get(url)
        
        if response.status_code == 200:
            print("Respuesta: \n", response.text)
            
            datosObjeto = response.json()
            fecha_hora = str(datosObjeto["datetime"])
            año = int(fecha_hora[0:4])
            mes = int(fecha_hora[5:7])
            dia = int(fecha_hora[8:10])
            hora = int(fecha_hora[11:13])
            minuto = int(fecha_hora[14:16])
            segs = int(fecha_hora[17:19])
            mSegs = int(round(int(fecha_hora[20:26])/10000))
            
            rtc.datetime((año, mes, dia, 0, hora, minuto, segs, mSegs))
            ultimaOpcion = utime.time()
            print("RTC actualizado\n ")
            
        else:
            print("Respuesta no valida: RTC no actualizado")
    
    fechaOled = "Fecha: {2:02d}/{1:02d}/{0:4d}".format(*rtc.datetime())
    horaOled = "Hora: {4:02d}:{5:02d}:{6:02d}".format(*rtc.datetime())
    
    oled.fill(0)
    oled.text("Reloj Web ESP32",0,5)
    oled.text(fechaOled,0,25)
    oled.text(horaOled,0,45)
    oled.show()
    
    utime.sleep(0.1)


