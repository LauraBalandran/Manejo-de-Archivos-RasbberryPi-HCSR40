# Blibliotecas
import RPi.GPIO as GPIO #Biblioteca para manejo de pines
import time    #Biblioteca para funciones de tiempo
from datetime import datetime  #Biblioteca para manejo de fechas

#Configuración de pines 
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO_ECHO    = 24
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)   #Definen pin de salida
GPIO.setup(GPIO_ECHO,GPIO.IN)          #Definen pin de entrada
GPIO.output(GPIO_TRIGGER, False)    #Inicializa salida en false

sFileStamp = time.strftime('%Y%m%d%H')
sFileName = '\out' + sFileStamp + '.txt'
f=open(sFileName, 'a')
f.write('TimeStamp,Value' + '\n')
print "Inicia la toma de datos"

try:  # este try maneja un while si por alguna situacion no funciona, envia la excepcion
	while True:
		print ("acerque el objeto para medir la distancia")
		GPIO.output(GPIO_TRIGGER,True)
		time.sleep(0.00001)      #Lanza un pulso de tiempo durante 1 microseg y espera
		GPIO.output(GPIO_TRIGGER,False)
		start = time.time()      #Despues el sensor responde con el pulso
		while GPIO.input(GPIO_ECHO)==0:  #Estos whiles verifican constantemente si hay pulso
			start = time.time()
		while GPIO.input(GPIO_ECHO)==1:
			stop = time.time()
		elapsed = stop-start   #cuando termina el pulso hace una comparacion de tiempo en lo que se envio el pulso y se recibio 
		distance = (elapsed * 34300)/2  #calcula distancia en base al tiempo por vel de sonido /2
		sTimeStamp = time.strftime('%Y%m%d%H%M%S')
		f.write(sTimeStamp + ',' + str(distance) + '\n')
		print (sTimeStamp + ' ' + str(distance))
		time.sleep(1)
		sTmpFileStamp = time.strftime('%Y%m%d%H')
		if sTmpFileStamp <> sFileStamp:
		  	    f.close
		   	    sFileName = 'out/' + sTmpFileStamp + '.txt' 
                f=open(sFileName, 'a')
		     	sFileStamp = sTmpFileStamp
			    print ("creando el archivo")
                
except KeyboardInterrupt:     # esta excepcion tiene la keyboard... para funcionar tambien con ctrl+C
	    print '\n' + 'termina la captura de datos.' + '\n'
	    f.close
	    GPIO.cleanup()