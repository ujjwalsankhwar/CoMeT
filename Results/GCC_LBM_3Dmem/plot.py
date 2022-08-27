import matplotlib.pyplot as plt
import os

file = open("4_Core_GCC_LBM_3D.trace", "r")

time_4_GCC_LBM_3D = []
maxCore_4_GCC_LBM_3D = []
maxMem_4_GCC_LBM_3D = []
gradMem_4_GCC_LBM_3D = []
count_4_GCC_LBM_3D = 0

for line in file:
	if count_4_GCC_LBM_3D == 0:
		count_4_GCC_LBM_3D += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_4_GCC_LBM_3D.append(max(arr[0:4]))
	maxMem_4_GCC_LBM_3D.append(max(arr[4:]))
	gradMem_4_GCC_LBM_3D.append(max(arr[4:20])-min(arr[4:20]))
	time_4_GCC_LBM_3D.append(count_4_GCC_LBM_3D)
	count_4_GCC_LBM_3D += 1

file.close()

file = open("4_Core_LBM_GCC_3D.trace", "r")

time_4_LBM_GCC_3D = []
maxCore_4_LBM_GCC_3D = []
maxMem_4_LBM_GCC_3D = []
gradMem_4_LBM_GCC_3D = []
count_4_LBM_GCC_3D = 0

for line in file:
	if count_4_LBM_GCC_3D == 0:
		count_4_LBM_GCC_3D += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_4_LBM_GCC_3D.append(max(arr[0:4]))
	maxMem_4_LBM_GCC_3D.append(max(arr[4:]))
	gradMem_4_LBM_GCC_3D.append(max(arr[4:20])-min(arr[4:20]))
	time_4_LBM_GCC_3D.append(count_4_LBM_GCC_3D)
	count_4_LBM_GCC_3D += 1

file.close()

directory = ["4_Core"]
subdir = ["GCC_LBM","LBM_GCC"]

for i in directory:
	os.makedirs(i, exist_ok=True)
	for j in subdir:
		os.makedirs(i+"/"+j, exist_ok=True)
		os.makedirs(i+"/"+j+"/Max_Mem_Temperature", exist_ok=True)

for i in directory:
	os.makedirs(i+"/Combined/Max_Mem_Temperature", exist_ok=True)

plt.plot(time_4_GCC_LBM_3D,maxMem_4_GCC_LBM_3D)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('4_Core/GCC_LBM/Max_Mem_Temperature/4_Core_3D_Mem_GCC_LBM.png')

plt.plot(time_4_LBM_GCC_3D,maxMem_4_LBM_GCC_3D)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('4_Core/LBM_GCC/Max_Mem_Temperature/4_Core_3D_Mem_LBM_GCC.png')

plt.plot(time_4_GCC_LBM_3D,maxMem_4_GCC_LBM_3D,label = "GCC_LBM")
plt.plot(time_4_LBM_GCC_3D,maxMem_4_LBM_GCC_3D,label = "LBM_GCC")
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('4_Core/Combined/Max_Mem_Temperature/4_Core_3D.png')