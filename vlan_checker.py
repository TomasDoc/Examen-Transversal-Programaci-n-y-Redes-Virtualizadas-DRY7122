# vlan_checker.py

vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print("VLAN en el rango normal.")
elif 1006 <= vlan <= 4094:
    print("VLAN en el rango extendido.")
else:
    print("Número de VLAN no válido.")
