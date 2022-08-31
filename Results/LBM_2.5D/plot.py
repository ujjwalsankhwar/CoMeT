import matplotlib.pyplot as plt
import os

file = open("4_Core_LBM_2.5D.trace", "r")

time_4 = []
maxCore_4 = []
maxMem_4 = []
gradMem_4 = []
gradCore_4 = []
count_4 = 0

for line in file:
	if count_4 == 0:
		count_4 += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_4.append(max(arr[0:4]))
	maxMem_4.append(max(arr[4:]))
	gradMem_4.append(max(arr[4:20])-min(arr[4:20]))
	gradCore_4.append(max(arr[0:4])-min(arr[0:4]))
	time_4.append(count_4)
	count_4 += 1

file.close()

file = open("16_Core_LBM_2.5D.trace", "r")

time_16 = []
maxCore_16 = []
maxMem_16 = []
gradMem_16 = []
gradCore_16 = []
count_16 = 0

for line in file:
	if count_16 == 0:
		count_16 += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_16.append(max(arr[0:16]))
	maxMem_16.append(max(arr[16:]))
	gradMem_16.append(max(arr[16:32])-min(arr[16:32]))
	gradCore_16.append(max(arr[0:16])-min(arr[0:16]))
	time_16.append(count_16)
	count_16 += 1

file.close()

file = open("32_Core_LBM_2.5D.trace", "r")

time_32 = []
maxCore_32 = []
maxMem_32 = []
gradMem_32 = []
gradCore_32 = []
count_32 = 0

for line in file:
	if count_32 == 0:
		count_32 += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_32.append(max(arr[0:32]))
	maxMem_32.append(max(arr[32:]))
	gradMem_32.append(max(arr[32:48])-min(arr[32:48]))
	gradCore_32.append(max(arr[0:32])-min(arr[0:32]))
	time_32.append(count_32)
	count_32 += 1

file.close()

directory = ["4_Core","16_Core","32_Core"]

for i in directory:
	os.makedirs(i, exist_ok=True)
	os.makedirs(i+"/Max_Mem_Temperature", exist_ok=True)
	os.makedirs(i+"/Max_Core_Temperature", exist_ok=True)
	os.makedirs(i+"/Max_Mem_Core_Temperature", exist_ok=True)
	os.makedirs(i+"/Max_Core_Temperature_Gradient", exist_ok=True)
	os.makedirs(i+"/Max_Mem_Temperature_Gradient", exist_ok=True)

os.makedirs("Combined", exist_ok=True)
os.makedirs("Combined/Max_Mem_Temperature", exist_ok=True)
os.makedirs("Combined/Max_Core_Temperature", exist_ok=True)

plt.plot(time_4,maxMem_4)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('4_Core/Max_Mem_Temperature/4_Core_Mem_LBM_2.5D.png')
plt.close()

plt.plot(time_4,maxCore_4)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('4_Core/Max_Core_Temperature/4_Core_Core_LBM_2.5D.png')
plt.close()

plt.plot(time_4,maxMem_4,label = "Max Mem Temp")
plt.plot(time_4,maxCore_4,label = "Max Core Temp")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core-Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('4_Core/Max_Mem_Core_Temperature/4_Core_Mem_Core_LBM_2.5D.png')
plt.close()

plt.plot(time_16,maxMem_16)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('16_Core/Max_Mem_Temperature/16_Core_Mem_LBM_2.5D.png')
plt.close()

plt.plot(time_16,maxCore_16)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('16_Core/Max_Core_Temperature/16_Core_Core_LBM_2.5D.png')
plt.close()

plt.plot(time_16,maxMem_16,label = "Max Mem Temp")
plt.plot(time_16,maxCore_16,label = "Max Core Temp")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core-Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('16_Core/Max_Mem_Core_Temperature/16_Core_Mem_Core_LBM_2.5D.png')
plt.close()
 
plt.plot(time_32,maxMem_32)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('32_Core/Max_Mem_Temperature/32_Core_Mem_LBM_2.5D.png')
plt.close()

plt.plot(time_32,maxCore_32)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('32_Core/Max_Core_Temperature/32_Core_Core_LBM_2.5D.png')
plt.close()

plt.plot(time_32,maxMem_32,label = "Max Mem Temp")
plt.plot(time_32,maxCore_32,label = "Max Core Temp")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core-Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('32_Core/Max_Mem_Core_Temperature/32_Core_Mem_Core_LBM_2.5D.png')
plt.close()

plt.plot(time_4,maxMem_4,label = "4_Core")
plt.plot(time_16,maxMem_16,label = "16_Core")
plt.plot(time_32,maxMem_32,label = "32_Core")
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('Combined/Max_Mem_Temperature/Mem_LBM_2.5D.png')
plt.close()

plt.plot(time_4,maxCore_4,label = "4_Core")
plt.plot(time_16,maxCore_16,label = "16_Core")
plt.plot(time_32,maxCore_32,label = "32_Core")
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('Combined/Max_Core_Temperature/Core_LBM_2.5D.png')
plt.close()

plt.plot(time_4,gradMem_4)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('4_Core/Max_Mem_Temperature_Gradient/4_Core_Mem_Grad_LBM_2.5D.png')
plt.close()

plt.plot(time_16,gradMem_16)
plt.ylabel('Temperature Gradient in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('16_Core/Max_Mem_Temperature_Gradient/16_Core_Mem_Grad_LBM_2.5D.png')
plt.close()

plt.plot(time_32,gradMem_32)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('32_Core/Max_Mem_Temperature_Gradient/32_Core_Mem_Grad_LBM_2.5D.png')
plt.close()

plt.plot(time_4,gradCore_4)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('4_Core/Max_Core_Temperature_Gradient/4_Core_Grad_LBM_2.5D.png')
plt.close()

plt.plot(time_16,gradCore_16)
plt.ylabel('Temperature Gradient in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('16_Core/Max_Core_Temperature_Gradient/16_Core_Grad_LBM_2.5D.png')
plt.close()

plt.plot(time_32,gradCore_32)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('32_Core/Max_Core_Temperature_Gradient/32_Core_Grad_LBM_2.5D.png')
plt.close()
