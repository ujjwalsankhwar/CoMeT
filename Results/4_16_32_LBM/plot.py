import matplotlib.pyplot as plt

file = open("4_Core.trace", "r")

time_4 = []
maxCore_4 = []
maxMem_4 = []
gradMem_4 = []
count_4 = 0

for line in file:
	if count_4 == 0:
		count_4 += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_4.append(max(arr[0:4]))
	maxMem_4.append(max(arr[4:]))
	gradMem_4.append(max(arr[4:20])-min(arr[4:20]))
	time_4.append(count_4)
	count_4 += 1

file.close()

file = open("16_Core.trace", "r")

time_16 = []
maxCore_16 = []
maxMem_16 = []
gradMem_16 = []
count_16 = 0

for line in file:
	if count_16 == 0:
		count_16 += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_16.append(max(arr[0:16]))
	maxMem_16.append(max(arr[16:]))
	gradMem_16.append(max(arr[16:32])-min(arr[16:32]))
	time_16.append(count_16)
	count_16 += 1

file.close()

file = open("32_Core.trace", "r")

time_32 = []
maxCore_32 = []
maxMem_32 = []
gradMem_32 = []
count_32 = 0

for line in file:
	if count_32 == 0:
		count_32 += 1
		continue
	arr = [float(i) for i in line.split( )]
	maxCore_32.append(max(arr[0:32]))
	maxMem_32.append(max(arr[32:]))
	gradMem_32.append(max(arr[32:48])-min(arr[32:48]))
	time_32.append(count_32)
	count_32 += 1

file.close()

plt.figure(0) 
plt.plot(time_4,maxMem_4)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('4_Core_Mem.png')

plt.figure(1) 
plt.plot(time_4,maxCore_4)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('4_Core_Core.png')

plt.figure(2) 
plt.plot(time_4,maxMem_4,label = "Max Mem Temp")
plt.plot(time_4,maxCore_4,label = "Max Core Temp")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core-Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('4_Core.png')

plt.figure(3) 
plt.plot(time_16,maxMem_16)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('16_Core_Mem.png')

plt.figure(4) 
plt.plot(time_16,maxCore_16)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('16_Core_Core.png')

plt.figure(5) 
plt.plot(time_16,maxMem_16,label = "Max Mem Temp")
plt.plot(time_16,maxCore_16,label = "Max Core Temp")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core-Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('16_Core.png')

plt.figure(6) 
plt.plot(time_32,maxMem_32)
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Mem Temperature vs Time')
plt.savefig('32_Core_Mem.png')

plt.figure(7) 
plt.plot(time_32,maxCore_32)
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Max Core Temperature vs Time')
plt.savefig('32_Core_Core.png')

plt.figure(8) 
plt.plot(time_32,maxMem_32,label = "Max Mem Temp")
plt.plot(time_32,maxCore_32,label = "Max Core Temp")
plt.ylabel('Max Core-Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core-Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('32_Core.png')

plt.figure(9) 
plt.plot(time_4,maxMem_4,label = "4_Core")
plt.plot(time_16,maxMem_16,label = "16_Core")
plt.plot(time_32,maxMem_32,label = "32_Core")
plt.ylabel('Max Mem Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Mem Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('Mem.png')

plt.figure(10) 
plt.plot(time_4,maxCore_4,label = "4_Core")
plt.plot(time_16,maxCore_16,label = "16_Core")
plt.plot(time_32,maxCore_32,label = "32_Core")
plt.ylabel('Max Core Temperature (in C)')
plt.xlabel('Time (in ms)')
plt.title('Max Core Temperature vs Time')
plt.grid()
plt.legend()
plt.savefig('Core.png')

plt.figure(11) 
plt.plot(time_4,gradMem_4)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('4_Core_Grad.png')

plt.figure(12) 
plt.plot(time_16,gradMem_16)
plt.ylabel('Temperature Gradient in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('16_Core_Grad.png')

plt.figure(13) 
plt.plot(time_32,gradMem_32)
plt.ylabel('Temperature Gradient (in C)')
plt.xlabel('Time (in ms)')
plt.grid()
plt.title('Temperature Gradient vs Time')
plt.savefig('32_Core_Grad.png')
