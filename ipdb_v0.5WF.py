import json

# Leer el JSON
with open("ips.json", "r") as file:
    JSONfile = json.load(file)

# Crear la lista
IPlist = []

for entry in JSONfile:
    
    # Extraccion y limpieza
    extractedIPs = entry['label'].split(',')
    
    # Volcado a la lista
    IPlist.extend(extractedIPs)
    
    # Eliminar duplicadas
    cleanIPlist = list(set(IPlist))
    
# Volcar resultados    
with open("IPdump.txt", "w") as output_file:
    for ip in cleanIPlist:
        output_file.write(ip + "\n")

# Leer BD principal
with open("IPDB.txt", "r") as file_A:
    ipdb = set(file_A.read().splitlines())

# Leer Volcado semanal
with open("IPdump.txt", "r") as file_B:
    ipdump = set(file_B.read().splitlines())

# Descartamos las IP que ya existen en la BD principal
ip2report = ipdump - ipdb
ip2workflow = ipdump - ip2report

# Volcar resultados
#with open("IP2report.txt", "w") as file_c:
 #   for ip in ip2report:
  #      file_c.write(ip + "\n")

with open("IP2WF.txt", "w") as file_c:
    cabecera = "(data['Trigger.Category.Investigatable.Product.EPP.Behavior.IOCValue'] in ["
    cierre = "])"
    capsize = 4600

    buffer = cabecera
    
    for ip in ip2workflow:
        IPload = f"'{ip}',"
        if len(buffer) + len(IPload) + len(cierre) < capsize:
            buffer += IPload
            
        else:
            buffer += IPload
            file_c.write(buffer + cierre + "\n\n")
            buffer = cabecera
            
    if buffer != cabecera:
        file_c.write(buffer + cierre)
        

input("\n Hecho.")
