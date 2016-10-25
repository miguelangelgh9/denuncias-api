# -*- coding: UTF-8 -*-
 
import subprocess

def cpuUso():
	
        result=subprocess.check_output("top -d 1 -b -n2 | grep 'Cpu(s)' | tail -n 1", shell=True)

 
        if result.find("%inact,")>=0:
 
		# si nuestro top es del tipo:
		#Cpu(s):  1.7%us,  3.4%sy,  0.0%ni, 94.9%id,  0.0%wa,  0.0%hi,  0.0%si,  0.0%st
            result=result[result.find("%inact,")-5:result.find("%inact,")]
 
        elif result.find(" inact,")>=0:
 
		# si nuestro top es del tipo:
		#%Cpu(s):  1,0 us,  1,5 sy,  0,0 ni, 97,5 id,  0,0 wa,  0,0 hi,  0,0 si,  0,0 st
             result=result[result.find(" inact,")-5:result.find(" inact,")]
	    # eliminamos la coma decimal por un punto
             result=result.replace(",",".")

        if result.find("%id,")>=0:
 
		# si nuestro top es del tipo:
		#Cpu(s):  1.7%us,  3.4%sy,  0.0%ni, 94.9%id,  0.0%wa,  0.0%hi,  0.0%si,  0.0%st
            result=result[result.find("%id,")-5:result.find("%id,")]
 
        elif result.find(" id,")>=0:
 
		# si nuestro top es del tipo:
		#%Cpu(s):  1,0 us,  1,5 sy,  0,0 ni, 97,5 id,  0,0 wa,  0,0 hi,  0,0 si,  0,0 st
             result=result[result.find(" id,")-5:result.find(" id,")]
	    # eliminamos la coma decimal por un punto
             result=result.replace(",",".")
 
	# devolvemos el % de uso
        return 100 - float(result.strip())
print("El uso de procesador es del: %.2f%%" % cpuUso())



