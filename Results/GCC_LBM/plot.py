import matplotlib.pyplot as plt

file = open("4_Core_GCC_LBM.trace", "r")

time_4_GCC_LBM = []
maxCore_4_GCC_LBM = []
maxMem_4_GCC_LBM = []
gradMem_4_GCC_LBM = []
count_4_GCC_LBM = 0

for line in file:
	if count_4_GCC_LBM == 0:
		count_4_GCC_LBM += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_4_GCC_LBM.append(max(arr[0:4]))
	maxMem_4_GCC_LBM.append(max(arr[4:]))
	gradMem_4_GCC_LBM.append(max(arr[4:20])-min(arr[4:20]))
	time_4_GCC_LBM.append(count_4_GCC_LBM)
	count_4_GCC_LBM += 1

file.close()

file = open("4_Core_LBM_GCC.trace", "r")

time_4_LBM_GCC = []
maxCore_4_LBM_GCC = []
maxMem_4_LBM_GCC = []
gradMem_4_LBM_GCC = []
count_4_LBM_GCC = 0

for line in file:
	if count_4_LBM_GCC == 0:
		count_4_LBM_GCC += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_4_LBM_GCC.append(max(arr[0:4]))
	maxMem_4_LBM_GCC.append(max(arr[4:]))
	gradMem_4_LBM_GCC.append(max(arr[4:20])-min(arr[4:20]))
	time_4_LBM_GCC.append(count_4_LBM_GCC)
	count_4_LBM_GCC += 1

file.close()

file = open("16_Core_GCC_LBM.trace", "r")

time_16_GCC_LBM = []
maxCore_16_GCC_LBM = []
maxMem_16_GCC_LBM = []
gradMem_16_GCC_LBM = []
count_16_GCC_LBM = 0

for line in file:
	if count_16_GCC_LBM == 0:
		count_16_GCC_LBM += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_16_GCC_LBM.append(max(arr[0:16]))
	maxMem_16_GCC_LBM.append(max(arr[16:]))
	gradMem_16_GCC_LBM.append(max(arr[16:])-min(arr[16:]))
	time_16_GCC_LBM.append(count_16_GCC_LBM)
	count_16_GCC_LBM += 1

file.close()

file = open("16_Core_LBM_GCC.trace", "r")

time_16_LBM_GCC = []
maxCore_16_LBM_GCC = []
maxMem_16_LBM_GCC = []
gradMem_16_LBM_GCC = []
count_16_LBM_GCC = 0

for line in file:
	if count_16_LBM_GCC == 0:
		count_16_LBM_GCC += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_16_LBM_GCC.append(max(arr[0:16]))
	maxMem_16_LBM_GCC.append(max(arr[16:]))
	gradMem_16_LBM_GCC.append(max(arr[16:])-min(arr[16:]))
	time_16_LBM_GCC.append(count_16_LBM_GCC)
	count_16_LBM_GCC += 1

file.close()

file = open("32_Core_GCC_LBM.trace", "r")

time_32_GCC_LBM = []
maxCore_32_GCC_LBM = []
maxMem_32_GCC_LBM = []
gradMem_32_GCC_LBM = []
count_32_GCC_LBM = 0

for line in file:
	if count_32_GCC_LBM == 0:
		count_32_GCC_LBM += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_32_GCC_LBM.append(max(arr[0:32]))
	maxMem_32_GCC_LBM.append(max(arr[32:]))
	gradMem_32_GCC_LBM.append(max(arr[32:])-min(arr[32:]))
	time_32_GCC_LBM.append(count_32_GCC_LBM)
	count_32_GCC_LBM += 1

file.close()

file = open("32_Core_LBM_GCC.trace", "r")

time_32_LBM_GCC = []
maxCore_32_LBM_GCC = []
maxMem_32_LBM_GCC = []
gradMem_32_LBM_GCC = []
count_32_LBM_GCC = 0

for line in file:
	if count_32_LBM_GCC == 0:
		count_32_LBM_GCC += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_32_LBM_GCC.append(max(arr[0:32]))
	maxMem_32_LBM_GCC.append(max(arr[32:]))
	gradMem_32_LBM_GCC.append(max(arr[32:])-min(arr[32:]))
	time_32_LBM_GCC.append(count_32_LBM_GCC)
	count_32_LBM_GCC += 1

file.close()

plt.figure(0) 
plt.plot(time_4_GCC_LBM,maxMem_4_GCC_LBM)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('4_Core_Mem_GCC_LBM.png')

plt.figure(1) 
plt.plot(time_4_LBM_GCC,maxMem_4_LBM_GCC)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('4_Core_Mem_LBM_GCC.png')

plt.figure(2) 
plt.plot(time_4_GCC_LBM,maxCore_4_GCC_LBM)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('4_Core_Core_GCC_LBM.png')

plt.figure(3) 
plt.plot(time_4_LBM_GCC,maxCore_4_LBM_GCC)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('4_Core_Core_LBM_GCC.png')

plt.figure(4) 
plt.plot(time_4_GCC_LBM,gradMem_4_GCC_LBM)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('4_Core_Grad_GCC_LBM.png')

plt.figure(5) 
plt.plot(time_4_LBM_GCC,gradMem_4_LBM_GCC)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('4_Core_Grad_LBM_GCC.png')

plt.figure(6) 
plt.plot(time_16_GCC_LBM,maxMem_16_GCC_LBM)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('16_Core_Mem_GCC_LBM.png')

plt.figure(7) 
plt.plot(time_16_LBM_GCC,maxMem_16_LBM_GCC)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('16_Core_Mem_LBM_GCC.png')

plt.figure(8) 
plt.plot(time_16_GCC_LBM,maxCore_16_GCC_LBM)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('16_Core_Core_GCC_LBM.png')

plt.figure(9) 
plt.plot(time_16_LBM_GCC,maxCore_16_LBM_GCC)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('16_Core_Core_LBM_GCC.png')

plt.figure(10) 
plt.plot(time_16_GCC_LBM,gradMem_16_GCC_LBM)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('16_Core_Grad_GCC_LBM.png')

plt.close('all')

plt.figure(11) 
plt.plot(time_16_LBM_GCC,gradMem_16_LBM_GCC)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('16_Core_Grad_LBM_GCC.png')

plt.figure(12) 
plt.plot(time_32_GCC_LBM,maxMem_32_GCC_LBM)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('32_Core_Mem_GCC_LBM.png')

plt.figure(13) 
plt.plot(time_32_LBM_GCC,maxMem_32_LBM_GCC)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('32_Core_Mem_LBM_GCC.png')

plt.figure(14) 
plt.plot(time_32_GCC_LBM,maxCore_32_GCC_LBM)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('32_Core_Core_GCC_LBM.png')

plt.figure(15) 
plt.plot(time_32_LBM_GCC,maxCore_32_LBM_GCC)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('32_Core_Core_LBM_GCC.png')

plt.figure(16) 
plt.plot(time_32_GCC_LBM,gradMem_32_GCC_LBM)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('32_Core_Grad_GCC_LBM.png')

plt.figure(17) 
plt.plot(time_32_LBM_GCC,gradMem_32_LBM_GCC)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('32_Core_Grad_LBM_GCC.png')

plt.figure(18) 
plt.plot(time_4_GCC_LBM,maxMem_4_GCC_LBM,label = "GCC_LBM")
plt.plot(time_4_LBM_GCC,maxMem_4_LBM_GCC,label = "LBM_GCC")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('4_Core.png')

plt.figure(19) 
plt.plot(time_16_GCC_LBM,maxMem_16_GCC_LBM,label = "GCC_LBM")
plt.plot(time_16_LBM_GCC,maxMem_16_LBM_GCC,label = "LBM_GCC")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('16_Core.png')

plt.figure(20) 
plt.plot(time_32_GCC_LBM,maxMem_32_GCC_LBM,label = "GCC_LBM")
plt.plot(time_32_LBM_GCC,maxMem_32_LBM_GCC,label = "LBM_GCC")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('32_Core.png')

plt.close('all')


plt.figure(21) 
plt.plot(time_4_GCC_LBM,gradMem_4_GCC_LBM,label = "GCC_LBM")
plt.plot(time_4_LBM_GCC,gradMem_4_LBM_GCC,label = "LBM_GCC")
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.legend()
plt.title('Temperature Gradient vs Time')
plt.savefig('4_Core_Grad.png')

# plt.figure(3) 
# plt.plot(time_16,maxMem_16)
# plt.ylabel('Max Mem Temperature (in C)')
# plt.xlabel('Time (in ms)')
# plt.grid()
# plt.title('Max Mem Temperature vs Time')
# plt.savefig('16_Core_Mem.png')

# plt.figure(4) 
# plt.plot(time_16,maxCore_16)
# plt.ylabel('Max Core Temperature (in C)')
# plt.xlabel('Time (in ms)')
# plt.grid()
# plt.title('Max Core Temperature vs Time')
# plt.savefig('16_Core_Core.png')

# plt.figure(5) 
# plt.plot(time_16,maxMem_16,label = "Max Mem Temp")
# plt.plot(time_16,maxCore_16,label = "Max Core Temp")
# plt.ylabel('Max Core-Mem Temperature (in C)')
# plt.xlabel('Time (in ms)')
# plt.title('Max Core-Mem Temperature vs Time')
# plt.grid()
# plt.legend()
# plt.savefig('16_Core.png')

# plt.figure(6) 
# plt.plot(time_32,maxMem_32)
# plt.ylabel('Max Mem Temperature (in C)')
# plt.xlabel('Time (in ms)')
# plt.grid()
# plt.title('Max Mem Temperature vs Time')
# plt.savefig('32_Core_Mem.png')

# plt.figure(7) 
# plt.plot(time_32,maxCore_32)
# plt.ylabel('Max Core Temperature (in C)')
# plt.xlabel('Time (in ms)')
# plt.grid()
# plt.title('Max Core Temperature vs Time')
# plt.savefig('32_Core_Core.png')

# plt.figure(8) 
# plt.plot(time_32,maxMem_32,label = "Max Mem Temp")
# plt.plot(time_32,maxCore_32,label = "Max Core Temp")
# plt.ylabel('Max Core-Mem Temperature (in C)')
# plt.xlabel('Time (in ms)')
# plt.title('Max Core-Mem Temperature vs Time')
# plt.grid()
# plt.legend()
# plt.savefig('32_Core.png')

# plt.figure(9) 
# plt.plot(time_4,maxMem_4,label = "4_Core")
# plt.plot(time_16,maxMem_16,label = "16_Core")
# plt.plot(time_32,maxMem_32,label = "32_Core")
# plt.ylabel('Max Mem Temperature (in C)')
# plt.xlabel('Time (in ms)')
# plt.title('Max Mem Temperature vs Time')
# plt.grid()
# plt.legend()
# plt.savefig('Mem.png')

# plt.figure(10) 
# plt.plot(time_4,maxCore_4,label = "4_Core")
# plt.plot(time_16,maxCore_16,label = "16_Core")
# plt.plot(time_32,maxCore_32,label = "32_Core")
# plt.ylabel('Max Core Temperature (in C)')
# plt.xlabel('Time (in ms)')
# plt.title('Max Core Temperature vs Time')
# plt.grid()
# plt.legend()
# plt.savefig('Core.png')

# plt.figure(12) 
# plt.plot(time_16,gradMem_16)
# plt.ylabel('Temperature Gradient in C)')
# plt.xlabel('Time (in ms)')
# plt.grid()
# plt.title('Temperature Gradient vs Time')
# plt.savefig('16_Core_Grad.png')

# plt.figure(13) 
# plt.plot(time_32,gradMem_32)
# plt.ylabel('Temperature Gradient (in C)')
# plt.xlabel('Time (in ms)')
# plt.grid()
# plt.title('Temperature Gradient vs Time')
# plt.savefig('32_Core_Grad.png')
