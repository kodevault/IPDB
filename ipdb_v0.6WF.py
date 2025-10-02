# Este script parsea un json con las IP que han generado alertas recientes en crowdstrike y las matchea con las IP existentes en la lista negra de NIX. Devuelve un txt formateado con las IP que existen en ambas listas para poder automatizar su cierre desde un workflow

import json
import time
import sys

# Leer el JSON
with open("ips.json", "r") as file:
    JSONfile = json.load(file)

# Convierte el JSON en una lista plana
rawIPlist = []
for entry in JSONfile:
    extractedIPs = entry['label'].split(',')
    rawIPlist.extend(extractedIPs)
    
# Elimina IP duplicadas
cleanIPlist = list(set(rawIPlist))
    
# Volcar resultados    
with open("IPfromJSON.txt", "w") as output_file:
    for ip in cleanIPlist:
        output_file.write(ip + "\n")

# Lee la blacklist de NIX
with open("blacklist.txt", "r") as file_A:
    blacklist = set(file_A.read().splitlines())

# Lee las IP exportadas de Falcon
with open("IPfromJSON.txt", "r") as file_B:
    ipdump = set(file_B.read().splitlines())

# Cruzamos las listas para obtener unicamente las IP que generan alerta en Falcon Y estan bloqueadas en NIX
ip2report = ipdump - blacklist
ip2workflow = ipdump - ip2report

# Volcar IP con alertas y sin bloqueo en NIX
"""with open("IP2report.txt", "w") as file_c:
    for ip in ip2report:
        file_c.write(ip + "\n")"""

# Divide el output en bloques que Falcon puede procesar. Añade las cabecera y cierre para facilitar exportacion a Workflow. Vuelca a txt.
with open("IP2WF.txt", "w") as file_c:
    cabecera = "(data['Trigger.Category.Investigatable.Product.EPP.Behavior.IOCValue'] in ["
    cierre = "])"
    capsize = 4600 # Limite real 5000

    buffer = cabecera
    
    for ip in ip2workflow:
        IPload = f"'{ip}',"
        if len(buffer) + len(IPload) + len(cierre) < capsize:
            buffer += IPload
            
        else:
            buffer += IPload
            file_c.write(buffer + cierre + "\n\n")
            buffer = cabecera
            
    if buffer != cabecera: # Fuerza el volcado del ultimo bloque aunque no llegue a capsize.
        file_c.write(buffer + cierre)
        
print("\n Finalizado sin errores.")
time.sleep(1.5)
sys.exit()
