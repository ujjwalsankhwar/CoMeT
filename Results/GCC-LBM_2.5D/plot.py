import matplotlib.pyplot as plt
import os

file = open("4_Core_GCC_LBM_2.5D.trace", "r")

time_4_GCC_LBM = []
maxCore_4_GCC_LBM = []
maxMem_4_GCC_LBM = []
gradMem_4_GCC_LBM = []
gradCore_4_GCC_LBM = []
count_4_GCC_LBM = 0

for line in file:
	if count_4_GCC_LBM == 0:
		count_4_GCC_LBM += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_4_GCC_LBM.append(max(arr[0:4]))
	maxMem_4_GCC_LBM.append(max(arr[4:]))
	gradMem_4_GCC_LBM.append(max(arr[4:20])-min(arr[4:20]))
	gradCore_4_GCC_LBM.append(max(arr[0:4])-min(arr[0:4]))
	time_4_GCC_LBM.append(count_4_GCC_LBM)
	count_4_GCC_LBM += 1

file.close()

file = open("4_Core_LBM_GCC_2.5D.trace", "r")

time_4_LBM_GCC = []
maxCore_4_LBM_GCC = []
maxMem_4_LBM_GCC = []
gradMem_4_LBM_GCC = []
gradCore_4_LBM_GCC = []
count_4_LBM_GCC = 0

for line in file:
	if count_4_LBM_GCC == 0:
		count_4_LBM_GCC += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_4_LBM_GCC.append(max(arr[0:4]))
	maxMem_4_LBM_GCC.append(max(arr[4:]))
	gradMem_4_LBM_GCC.append(max(arr[4:20])-min(arr[4:20]))
	gradCore_4_LBM_GCC.append(max(arr[0:4])-min(arr[0:4]))
	time_4_LBM_GCC.append(count_4_LBM_GCC)
	count_4_LBM_GCC += 1

file.close()

file = open("16_Core_GCC_LBM_2.5D.trace", "r")

time_16_GCC_LBM = []
maxCore_16_GCC_LBM = []
maxMem_16_GCC_LBM = []
gradMem_16_GCC_LBM = []
gradCore_16_GCC_LBM = []
count_16_GCC_LBM = 0

for line in file:
	if count_16_GCC_LBM == 0:
		count_16_GCC_LBM += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_16_GCC_LBM.append(max(arr[0:16]))
	maxMem_16_GCC_LBM.append(max(arr[16:]))
	gradMem_16_GCC_LBM.append(max(arr[16:])-min(arr[16:]))
	gradCore_16_GCC_LBM.append(max(arr[0:16])-min(arr[0:16]))
	time_16_GCC_LBM.append(count_16_GCC_LBM)
	count_16_GCC_LBM += 1

file.close()

file = open("16_Core_LBM_GCC_2.5D.trace", "r")

time_16_LBM_GCC = []
maxCore_16_LBM_GCC = []
maxMem_16_LBM_GCC = []
gradMem_16_LBM_GCC = []
gradCore_16_LBM_GCC = []
count_16_LBM_GCC = 0

for line in file:
	if count_16_LBM_GCC == 0:
		count_16_LBM_GCC += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_16_LBM_GCC.append(max(arr[0:16]))
	maxMem_16_LBM_GCC.append(max(arr[16:]))
	gradMem_16_LBM_GCC.append(max(arr[16:])-min(arr[16:]))
	gradCore_16_LBM_GCC.append(max(arr[0:16])-min(arr[0:16]))
	time_16_LBM_GCC.append(count_16_LBM_GCC)
	count_16_LBM_GCC += 1

file.close()

file = open("32_Core_GCC_LBM_2.5D.trace", "r")

time_32_GCC_LBM = []
maxCore_32_GCC_LBM = []
maxMem_32_GCC_LBM = []
gradMem_32_GCC_LBM = []
gradCore_32_GCC_LBM = []
count_32_GCC_LBM = 0

for line in file:
	if count_32_GCC_LBM == 0:
		count_32_GCC_LBM += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_32_GCC_LBM.append(max(arr[0:32]))
	maxMem_32_GCC_LBM.append(max(arr[32:]))
	gradMem_32_GCC_LBM.append(max(arr[32:])-min(arr[32:]))
	gradCore_32_GCC_LBM.append(max(arr[0:32])-min(arr[0:32]))
	time_32_GCC_LBM.append(count_32_GCC_LBM)
	count_32_GCC_LBM += 1

file.close()

file = open("32_Core_LBM_GCC_2.5D.trace", "r")

time_32_LBM_GCC = []
maxCore_32_LBM_GCC = []
maxMem_32_LBM_GCC = []
gradMem_32_LBM_GCC = []
gradCore_32_LBM_GCC = []
count_32_LBM_GCC = 0

for line in file:
	if count_32_LBM_GCC == 0:
		count_32_LBM_GCC += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_32_LBM_GCC.append(max(arr[0:32]))
	maxMem_32_LBM_GCC.append(max(arr[32:]))
	gradMem_32_LBM_GCC.append(max(arr[32:])-min(arr[32:]))
	gradCore_32_LBM_GCC.append(max(arr[0:32])-min(arr[0:32]))
	time_32_LBM_GCC.append(count_32_LBM_GCC)
	count_32_LBM_GCC += 1

file.close()

directory = ["4_Core","16_Core","32_Core"]
subdir = ["GCC_LBM","LBM_GCC"]

for i in directory:
	os.makedirs(i, exist_ok=True)
	for j in subdir:
		os.makedirs(i+"/"+j, exist_ok=True)
		os.makedirs(i+"/"+j+"/Max_Mem_Temperature", exist_ok=True)
		os.makedirs(i+"/"+j+"/Max_Core_Temperature", exist_ok=True)
		os.makedirs(i+"/"+j+"/Max_Mem_Core_Temperature", exist_ok=True)
		os.makedirs(i+"/"+j+"/Max_Core_Temperature_Gradient", exist_ok=True)
		os.makedirs(i+"/"+j+"/Max_Mem_Temperature_Gradient", exist_ok=True)

for i in directory:
	os.makedirs(i+"/Combined/Max_Mem_Temperature", exist_ok=True)
	os.makedirs(i+"/Combined/Max_Core_Temperature", exist_ok=True)

plt.plot(time_4_GCC_LBM,maxMem_4_GCC_LBM)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('4_Core/GCC_LBM/Max_Mem_Temperature/4_Core_Mem_GCC_LBM_2.5D.png')
plt.close()

plt.plot(time_4_LBM_GCC,maxMem_4_LBM_GCC)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('4_Core/LBM_GCC/Max_Mem_Temperature/4_Core_Mem_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_4_GCC_LBM,maxCore_4_GCC_LBM)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('4_Core/GCC_LBM/Max_Core_Temperature/4_Core_Core_GCC_LBM_2.5D.png')
plt.close()

plt.plot(time_4_LBM_GCC,maxCore_4_LBM_GCC)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('4_Core/LBM_GCC/Max_Core_Temperature/4_Core_Core_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_4_GCC_LBM,maxMem_4_GCC_LBM,label = "Max Mem Temp")
plt.plot(time_4_GCC_LBM,maxCore_4_GCC_LBM,label = "Max Core Temp")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core-Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('4_Core/GCC_LBM/Max_Mem_Core_Temperature/4_Core_Mem_Core_GCC_LBM_2.5D.png')
plt.close()

plt.plot(time_4_LBM_GCC,maxMem_4_LBM_GCC,label = "Max Mem Temp")
plt.plot(time_4_LBM_GCC,maxCore_4_LBM_GCC,label = "Max Core Temp")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core-Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('4_Core/LBM_GCC/Max_Mem_Core_Temperature/4_Core_Mem_Core_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_4_GCC_LBM,gradMem_4_GCC_LBM)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('4_Core/GCC_LBM/Max_Mem_Temperature_Gradient/4_Core_Mem_Grad_GCC_LBM_2.5D.png')
plt.close()

plt.plot(time_4_LBM_GCC,gradMem_4_LBM_GCC)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('4_Core/LBM_GCC/Max_Mem_Temperature_Gradient/4_Core_Mem_Grad_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_4_GCC_LBM,gradCore_4_GCC_LBM)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('4_Core/GCC_LBM/Max_Core_Temperature_Gradient/4_Core_Grad_GCC_LBM_2.5D.png')
plt.close()

plt.plot(time_4_LBM_GCC,gradCore_4_LBM_GCC)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('4_Core/LBM_GCC/Max_Core_Temperature_Gradient/4_Core_Grad_LBM_GCC_2.5D.png')
plt.close()
 
plt.plot(time_16_GCC_LBM,maxMem_16_GCC_LBM)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('16_Core/GCC_LBM/Max_Mem_Temperature/16_Core_Mem_GCC_LBM_2.5D.png')
plt.close()

plt.plot(time_16_LBM_GCC,maxMem_16_LBM_GCC)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('16_Core/LBM_GCC/Max_Mem_Temperature/16_Core_Mem_LBM_GCC_2.5D.png')
plt.close()
 
plt.plot(time_16_GCC_LBM,maxCore_16_GCC_LBM)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('16_Core/GCC_LBM/Max_Core_Temperature/16_Core_Core_GCC_LBM_2.5D.png')
plt.close()

plt.plot(time_16_LBM_GCC,maxCore_16_LBM_GCC)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('16_Core/LBM_GCC/Max_Core_Temperature/16_Core_Core_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_16_GCC_LBM,maxMem_16_GCC_LBM,label = "Max Mem Temp")
plt.plot(time_16_GCC_LBM,maxCore_16_GCC_LBM,label = "Max Core Temp")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core-Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('16_Core/GCC_LBM/Max_Mem_Core_Temperature/16_Core_Mem_Core_GCC_LBM_2.5D.png')
plt.close()

plt.plot(time_16_LBM_GCC,maxMem_16_LBM_GCC,label = "Max Mem Temp")
plt.plot(time_16_LBM_GCC,maxCore_16_LBM_GCC,label = "Max Core Temp")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core-Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('16_Core/LBM_GCC/Max_Mem_Core_Temperature/16_Core_Mem_Core_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_16_GCC_LBM,gradMem_16_GCC_LBM)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('16_Core/GCC_LBM/Max_Mem_Temperature_Gradient/16_Core_Mem_Grad_GCC_LBM_2.5D.png')
plt.close()

plt.plot(time_16_LBM_GCC,gradMem_16_LBM_GCC)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('16_Core/LBM_GCC/Max_Mem_Temperature_Gradient/16_Core_Mem_Grad_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_16_GCC_LBM,gradCore_16_GCC_LBM)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('16_Core/GCC_LBM/Max_Core_Temperature_Gradient/16_Core_Grad_GCC_LBM_2.5D.png')
plt.close()

plt.plot(time_16_LBM_GCC,gradCore_16_LBM_GCC)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('16_Core/LBM_GCC/Max_Core_Temperature_Gradient/16_Core_Grad_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_32_GCC_LBM,maxMem_32_GCC_LBM)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('32_Core/GCC_LBM/Max_Mem_Temperature/32_Core_Mem_GCC_LBM_2.5D.png')
plt.close()

plt.plot(time_32_LBM_GCC,maxMem_32_LBM_GCC)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('32_Core/LBM_GCC/Max_Mem_Temperature/32_Core_Mem_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_32_GCC_LBM,maxCore_32_GCC_LBM)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('32_Core/GCC_LBM/Max_Core_Temperature/32_Core_Core_GCC_LBM_2.5D.png')
plt.close()
 
plt.plot(time_32_LBM_GCC,maxCore_32_LBM_GCC)
plt.ylabel('Max Core TemLBM_GCC/perature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('32_Core/LBM_GCC/Max_Core_Temperature/32_Core_Core_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_32_GCC_LBM,maxMem_32_GCC_LBM,label = "Max Mem Temp")
plt.plot(time_32_GCC_LBM,maxCore_32_GCC_LBM,label = "Max Core Temp")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core-Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('32_Core/GCC_LBM/Max_Mem_Core_Temperature/32_Core_Mem_Core_GCC_LBM_2.5D.png')
plt.close()

plt.plot(time_32_LBM_GCC,maxMem_32_LBM_GCC,label = "Max Mem Temp")
plt.plot(time_32_LBM_GCC,maxCore_32_LBM_GCC,label = "Max Core Temp")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core-Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('32_Core/LBM_GCC/Max_Mem_Core_Temperature/32_Core_Mem_Core_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_32_GCC_LBM,gradMem_32_GCC_LBM)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('32_Core/GCC_LBM/Max_Mem_Temperature_Gradient/32_Core_Mem_Grad_GCC_LBM_2.5D.png')
plt.close()
 
plt.plot(time_32_LBM_GCC,gradMem_32_LBM_GCC)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('32_Core/LBM_GCC/Max_Mem_Temperature_Gradient/32_Core_Mem_Grad_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_32_GCC_LBM,gradCore_32_GCC_LBM)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('32_Core/GCC_LBM/Max_Core_Temperature_Gradient/32_Core_Grad_GCC_LBM_2.5D.png')
plt.close()
 
plt.plot(time_32_LBM_GCC,gradCore_32_LBM_GCC)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('32_Core/LBM_GCC/Max_Core_Temperature_Gradient/32_Core_Grad_LBM_GCC_2.5D.png')
plt.close()

plt.plot(time_4_GCC_LBM,maxMem_4_GCC_LBM,label = "GCC_LBM")
plt.plot(time_4_LBM_GCC,maxMem_4_LBM_GCC,label = "LBM_GCC")
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('4_Core/Combined/Max_Mem_Temperature/4_Core_Mem_2.5D.png')
plt.close()
 
plt.plot(time_16_GCC_LBM,maxMem_16_GCC_LBM,label = "GCC_LBM")
plt.plot(time_16_LBM_GCC,maxMem_16_LBM_GCC,label = "LBM_GCC")
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('16_Core/Combined/Max_Mem_Temperature/16_Core_Mem_2.5D.png')
plt.close()
 
plt.plot(time_32_GCC_LBM,maxMem_32_GCC_LBM,label = "GCC_LBM")
plt.plot(time_32_LBM_GCC,maxMem_32_LBM_GCC,label = "LBM_GCC")
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('32_Core/Combined/Max_Mem_Temperature/32_Core_Mem_2.5D.png')
plt.close()

plt.plot(time_4_GCC_LBM,maxCore_4_GCC_LBM,label = "GCC_LBM")
plt.plot(time_4_LBM_GCC,maxCore_4_LBM_GCC,label = "LBM_GCC")
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.legend()
plt.title('Max Core Temperature vs Time')
plt.savefig('4_Core/Combined/Max_Core_Temperature/4_Core_Core_2.5D.png')
plt.close()

plt.plot(time_16_GCC_LBM,maxCore_16_GCC_LBM,label = "GCC_LBM")
plt.plot(time_16_LBM_GCC,maxCore_16_LBM_GCC,label = "LBM_GCC")
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.legend()
plt.title('Max Core Temperature vs Time')
plt.savefig('16_Core/Combined/Max_Core_Temperature/16_Core_Core_2.5D.png')
plt.close()

plt.plot(time_32_GCC_LBM,maxCore_32_GCC_LBM,label = "GCC_LBM")
plt.plot(time_32_LBM_GCC,maxCore_32_LBM_GCC,label = "LBM_GCC")
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.legend()
plt.title('Max Core Temperature vs Time')
plt.savefig('32_Core/Combined/Max_Core_Temperature/32_Core_Core_2.5D.png')
plt.close()