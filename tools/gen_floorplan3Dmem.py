#!/usr/bin/env python

from distutils import core
import sys, os, math, collections, sniper_lib, sniper_stats, sniper_config, getopt

def floorplan_3D_mem(floorplan, tim_mem, format = 'svg', mem_dim=[], outputobj = sys.stdout):
  print("floorplan_3D_mem")
  mem_layer_thikness = 500#variable (10x)
  tim_layer_thikness = 200#variable (10x)
  cos60 = 0.7071#0.866025#0.5
  sin60 = -0.7071#-0.5#0.866025
  cosz = 1
  cosZ = 0.7071#0.866025
  file = open(floorplan, mode = 'r')
  lines = file.readlines()
  file.close()
  memx = int(mem_dim[0])
  memy = int(mem_dim[1])
  memz = int(mem_dim[2])
  #print("memz = ",memz)
  arr = []
  # flag = False
  flag = False
  for line in lines:
    if (flag):
      line = line.split('\t')
      temp_line = []
      temp_line.append(int(float(line[1])*1000000))
      temp_line.append(int(float(line[2])*1000000))
      temp_line.append(int(float(line[3])*1000000))
      temp_line.append(int(float(line[4])*1000000))
      arr.append(temp_line)
      #print(temp_line)
    else:
      flag = True
  
  #dimensions of floorplan
  file = open(tim_mem, mode = 'r')
  lines = file.readlines()
  file.close()
  flag = False
  tim_height = 0
  tim_width = 0
  origin_x = 0
  origin_y = 0
  for line in lines:
    if (flag):
      line = line.split('\t')
      temp_line = []
      tim_width = int(float(line[1])*1000000)
      tim_height = int(float(line[2])*1000000)
      origin_x = int(float(line[3])*1000000)
      origin_y = int(float(line[4])*1000000)
    else:
      flag = True
  
  # total_core_height = corey * arr[0][1]
  # total_core_width = corex * arr[0][0]
  # total_mem_height = memy * arr[corex*corey*corez][1]
  # total_mem_width = memx * arr[corex*corey*corez][0]
  # dist_core_mem = arr[-1][0]



  print >> outputobj, '''\
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
'''
  print >> outputobj, '''\
<svg xmlns="http://www.w3.org/2000/svg">
<svg width="900px" height="500px"
    viewBox="%d %d %d %d">
'''%(origin_x,origin_y,2*tim_width,3*tim_height)
  print >> outputobj, '''\
<g id="floorplan" style="stroke: none; fill: red;">
  <rect x="%d" y="%d" width="%d" height="%d" style="fill:rgb(0,255,153)" />
  '''%(origin_x,origin_y,2*tim_width,3*tim_height)

  end_mem = memx*memy#*memz
  #X1
  k=0
  while (k<memz):
    x1 = arr[end_mem+0][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
    y1 = arr[end_mem+0][3] + -(mem_layer_thikness+tim_layer_thikness)*k
    x2 = x1 + arr[end_mem+0][0]
    y2 = y1
    x3 = x1
    y3 = y1 + arr[end_mem+0][1]
    x4 = x2
    y4 = y3
    mem_x1 = x1*cos60 + y1*sin60
    mem_y1 = (-x1*sin60 + y1*cos60)*cosZ
    mem_x2 = x2*cos60 + y2*sin60
    mem_y2 = (-x2*sin60 + y2*cos60)*cosZ
    mem_x3 = x3*cos60 + y3*sin60
    mem_y3 = (-x3*sin60 + y3*cos60)*cosZ
    mem_x4 = x4*cos60 + y4*sin60
    mem_y4 = (-x4*sin60 + y4*cos60)*cosZ

    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x1,mem_y1,mem_x3,mem_y3,mem_x4,mem_y4,mem_x2,mem_y2)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x3,mem_y3,mem_x3,mem_y3+mem_layer_thikness,mem_x4,mem_y4+mem_layer_thikness,mem_x4,mem_y4)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x4,mem_y4,mem_x4,mem_y4+mem_layer_thikness,mem_x2,mem_y2+mem_layer_thikness,mem_x2,mem_y2)
    k+=1
  #X3
  k=0
  while (k<memz):
    x1 = arr[end_mem+2][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
    y1 = arr[end_mem+2][3]-(mem_layer_thikness+tim_layer_thikness)*k
    x2 = x1 + arr[end_mem+2][0]
    y2 = y1
    x3 = x1
    y3 = y1 + arr[end_mem+2][1]
    x4 = x2
    y4 = y3
    mem_x1 = x1*cos60 + y1*sin60
    mem_y1 = (-x1*sin60 + y1*cos60)*cosZ
    mem_x2 = x2*cos60 + y2*sin60
    mem_y2 = (-x2*sin60 + y2*cos60)*cosZ
    mem_x3 = x3*cos60 + y3*sin60
    mem_y3 = (-x3*sin60 + y3*cos60)*cosZ
    mem_x4 = x4*cos60 + y4*sin60
    mem_y4 = (-x4*sin60 + y4*cos60)*cosZ

    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x1,mem_y1,mem_x3,mem_y3,mem_x4,mem_y4,mem_x2,mem_y2)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x3,mem_y3,mem_x3,mem_y3+mem_layer_thikness,mem_x4,mem_y4+mem_layer_thikness,mem_x4,mem_y4)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x4,mem_y4,mem_x4,mem_y4+mem_layer_thikness,mem_x2,mem_y2+mem_layer_thikness,mem_x2,mem_y2)
    k+=1
  #mem
  start_mem = 0#corex*corey#*corez
  mem_size = memx*memy#*memz
  nth_mem = 0

  i=memy-1
  j=0
  k=0
  while (k<memz):
#############################################
    i=memy-1
    j=0
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    mem_x1 = 0
    mem_x2 = 0
    mem_x3 = 0
    mem_x4 = 0
    mem_y1 = 0
    mem_y2 = 0
    mem_y3 = 0
    mem_y4 = 0
    #i==0 and j==0
    i=0
    j=0
    x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
    y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
    
    mem_x1 = x1*cos60 + y1*sin60
    mem_y1 = (-x1*sin60 + y1*cos60)*cosZ

    i=0
    j=memx-1
    x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
    y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
    mem_x2 =  x2*cos60 + y2*sin60
    mem_y2 = (-x2*sin60 + y2*cos60)*cosZ

    i=memy-1
    j=0
    x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
    y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
    mem_x3 = x1*cos60 + y1*sin60
    mem_y3 = (-x1*sin60 + y1*cos60)*cosZ

    i=memy-1
    j=memx-1
    x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
    y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
    if (i==memy-1 and j==memx-1):
      mem_x4 = x2*cos60 + y2*sin60
      mem_y4 = (-x2*sin60 + y2*cos60)*cosZ
    #3D effect thickness applied
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(255,155,100);stroke:purple;stroke-width:1" />'''%(mem_x1,mem_y1,mem_x3,mem_y3,mem_x4,mem_y4,mem_x2,mem_y2)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(255,155,100);stroke:purple;stroke-width:1" />'''%(mem_x3,mem_y3,mem_x3,mem_y3+mem_layer_thikness,mem_x4,mem_y4+mem_layer_thikness,mem_x4,mem_y4)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(255,155,100);stroke:purple;stroke-width:1" />'''%(mem_x4,mem_y4,mem_x4,mem_y4+mem_layer_thikness,mem_x2,mem_y2+mem_layer_thikness,mem_x2,mem_y2)
    
    
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(mem_x3,mem_y3,mem_x3,mem_y3+mem_layer_thikness)
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(mem_x4,mem_y4,mem_x4,mem_y4+mem_layer_thikness)
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(mem_x2,mem_y2,mem_x2,mem_y2+mem_layer_thikness)
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(mem_x3,mem_y3+mem_layer_thikness,mem_x4,mem_y4+mem_layer_thikness)
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(mem_x4,mem_y4+mem_layer_thikness,mem_x2,mem_y2+mem_layer_thikness)
    

  ###################################
    i=memy-1
    j=0
    while (i>-1):
      j=0
      while (j<memx):
        x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
        x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
        print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
        x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
        x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
        print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
        x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
        x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
        print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
        x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
        x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
        print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
        j=j+1
      i=i-1
    k=k+1
  
  #X2
  k=0
  while (k<memz):
    x1 = arr[end_mem+1][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
    y1 = arr[end_mem+1][3]-(mem_layer_thikness+tim_layer_thikness)*k
    x2 = x1 + arr[end_mem+1][0]
    y2 = y1
    x3 = x1
    y3 = y1 + arr[end_mem+1][1]
    x4 = x2
    y4 = y3
    mem_x1 = x1*cos60 + y1*sin60
    mem_y1 = (-x1*sin60 + y1*cos60)*cosZ
    mem_x2 = x2*cos60 + y2*sin60
    mem_y2 = (-x2*sin60 + y2*cos60)*cosZ
    mem_x3 = x3*cos60 + y3*sin60
    mem_y3 = (-x3*sin60 + y3*cos60)*cosZ
    mem_x4 = x4*cos60 + y4*sin60
    mem_y4 = (-x4*sin60 + y4*cos60)*cosZ

    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x1,mem_y1,mem_x3,mem_y3,mem_x4,mem_y4,mem_x2,mem_y2)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x3,mem_y3,mem_x3,mem_y3+mem_layer_thikness,mem_x4,mem_y4+mem_layer_thikness,mem_x4,mem_y4)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x4,mem_y4,mem_x4,mem_y4+mem_layer_thikness,mem_x2,mem_y2+mem_layer_thikness,mem_x2,mem_y2)
    k+=1
  print >> outputobj,'''</g>
</svg>
'''

  
def floorplan_3D_core(floorplan, tim_mem, format = 'svg', mem_dim=[], outputobj = sys.stdout):
  print("floorplan_3D_core")
  mem_layer_thikness = 500#variable (10x)
  tim_layer_thikness = 200#variable (10x)
  cos60 = 0.7071#0.866025#0.5
  sin60 = -0.7071#-0.5#0.866025
  cosz = 1
  cosZ = 0.7071#0.866025
  file = open(floorplan, mode = 'r')
  lines = file.readlines()
  file.close()
  memx = int(mem_dim[0])
  memy = int(mem_dim[1])
  memz = int(mem_dim[2])
  #print("memz = ",memz)
  arr = []
  # flag = False
  flag = False
  for line in lines:
    if (flag):
      line = line.split('\t')
      temp_line = []
      temp_line.append(int(float(line[1])*1000000))
      temp_line.append(int(float(line[2])*1000000))
      temp_line.append(int(float(line[3])*1000000))
      temp_line.append(int(float(line[4])*1000000))
      arr.append(temp_line)
      #print(temp_line)
    else:
      flag = True
  # arr.append([0,0,0,0])
  #dimensions of floorplan
  file = open(tim_mem, mode = 'r')
  lines = file.readlines()
  file.close()
  flag = False
  tim_height = 0
  tim_width = 0
  origin_x = 0
  origin_y = 0
  for line in lines:
    if (flag):
      line = line.split('\t')
      temp_line = []
      tim_width = int(float(line[1])*1000000)
      tim_height = int(float(line[2])*1000000)
      origin_x = int(float(line[3])*1000000)
      origin_y = int(float(line[4])*1000000)
    else:
      flag = True
  
  # total_core_height = corey * arr[0][1]
  # total_core_width = corex * arr[0][0]
  # total_mem_height = memy * arr[corex*corey*corez][1]
  # total_mem_width = memx * arr[corex*corey*corez][0]
  # dist_core_mem = arr[-1][0]



  print >> outputobj, '''\
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
'''
  print >> outputobj, '''\
<svg xmlns="http://www.w3.org/2000/svg">
<svg width="900px" height="500px"
    viewBox="%d %d %d %d">
'''%(origin_x,origin_y,2*tim_width,3*tim_height)
  print >> outputobj, '''\
<g id="floorplan" style="stroke: none; fill: red;">
  <rect x="%d" y="%d" width="%d" height="%d" style="fill:rgb(0,255,153)" />
  '''%(origin_x,origin_y,2*tim_width,3*tim_height)

  end_mem = memx*memy#*memz
  
  
  #mem
  start_mem = 0#corex*corey#*corez
  mem_size = memx*memy#*memz
  nth_mem = 0

  i=memy-1
  j=0
  k=0
  while (k<memz):
#############################################
    i=memy-1
    j=0
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    mem_x1 = 0
    mem_x2 = 0
    mem_x3 = 0
    mem_x4 = 0
    mem_y1 = 0
    mem_y2 = 0
    mem_y3 = 0
    mem_y4 = 0
    #i==0 and j==0
    i=0
    j=0
    x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
    y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
    
    mem_x1 = x1*cos60 + y1*sin60
    mem_y1 = (-x1*sin60 + y1*cos60)*cosZ

    i=0
    j=memx-1
    x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
    y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
    mem_x2 =  x2*cos60 + y2*sin60
    mem_y2 = (-x2*sin60 + y2*cos60)*cosZ

    i=memy-1
    j=0
    x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
    y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
    mem_x3 = x1*cos60 + y1*sin60
    mem_y3 = (-x1*sin60 + y1*cos60)*cosZ

    i=memy-1
    j=memx-1
    x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
    y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
    if (i==memy-1 and j==memx-1):
      mem_x4 = x2*cos60 + y2*sin60
      mem_y4 = (-x2*sin60 + y2*cos60)*cosZ
    #3D effect thickness applied
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(255,155,100);stroke:purple;stroke-width:1" />'''%(mem_x1,mem_y1,mem_x3,mem_y3,mem_x4,mem_y4,mem_x2,mem_y2)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(255,155,100);stroke:purple;stroke-width:1" />'''%(mem_x3,mem_y3,mem_x3,mem_y3+mem_layer_thikness,mem_x4,mem_y4+mem_layer_thikness,mem_x4,mem_y4)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(255,155,100);stroke:purple;stroke-width:1" />'''%(mem_x4,mem_y4,mem_x4,mem_y4+mem_layer_thikness,mem_x2,mem_y2+mem_layer_thikness,mem_x2,mem_y2)
    
    
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(mem_x3,mem_y3,mem_x3,mem_y3+mem_layer_thikness)
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(mem_x4,mem_y4,mem_x4,mem_y4+mem_layer_thikness)
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(mem_x2,mem_y2,mem_x2,mem_y2+mem_layer_thikness)
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(mem_x3,mem_y3+mem_layer_thikness,mem_x4,mem_y4+mem_layer_thikness)
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(mem_x4,mem_y4+mem_layer_thikness,mem_x2,mem_y2+mem_layer_thikness)
    

  ###################################
    i=memy-1
    j=0
    while (i>-1):
      j=0
      while (j<memx):
        x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
        x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
        print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
        x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
        x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
        print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
        x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
        x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
        print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
        x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
        x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
        y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
        print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
        j=j+1
      i=i-1
      x1 = arr[end_mem+0][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k
      y1 = arr[end_mem+0][3] + -(mem_layer_thikness+tim_layer_thikness)*k
      x2 = x1 + arr[end_mem+0][0]
      y2 = y1
      x3 = x1
      y3 = y1 + arr[end_mem+0][1]
      x4 = x2
      y4 = y3
      mem_x1 = x1*cos60 + y1*sin60
      mem_y1 = (-x1*sin60 + y1*cos60)*cosZ
      mem_x2 = x2*cos60 + y2*sin60
      mem_y2 = (-x2*sin60 + y2*cos60)*cosZ
      mem_x3 = x3*cos60 + y3*sin60
      mem_y3 = (-x3*sin60 + y3*cos60)*cosZ
      mem_x4 = x4*cos60 + y4*sin60
      mem_y4 = (-x4*sin60 + y4*cos60)*cosZ

      print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x1,mem_y1,mem_x3,mem_y3,mem_x4,mem_y4,mem_x2,mem_y2)
      print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x3,mem_y3,mem_x3,mem_y3+mem_layer_thikness,mem_x4,mem_y4+mem_layer_thikness,mem_x4,mem_y4)
      print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x4,mem_y4,mem_x4,mem_y4+mem_layer_thikness,mem_x2,mem_y2+mem_layer_thikness,mem_x2,mem_y2)
      
    k=k+1
  #X4
  length_air_over_core = 10000
  length_air_over_core = tim_width - arr[end_mem+0][0]
  k=memz
  while (k<8):
    x1 = arr[end_mem+0][2]+tim_width-(mem_layer_thikness+tim_layer_thikness)*k-length_air_over_core
    y1 = arr[end_mem+0][3] + -(mem_layer_thikness+tim_layer_thikness)*k
    x2 = x1 + arr[end_mem+0][0]+length_air_over_core
    y2 = y1
    x3 = x1
    y3 = y1 + arr[end_mem+0][1]
    x4 = x2
    y4 = y3
    mem_x1 = x1*cos60 + y1*sin60
    mem_y1 = (-x1*sin60 + y1*cos60)*cosZ
    mem_x2 = x2*cos60 + y2*sin60
    mem_y2 = (-x2*sin60 + y2*cos60)*cosZ
    mem_x3 = x3*cos60 + y3*sin60
    mem_y3 = (-x3*sin60 + y3*cos60)*cosZ
    mem_x4 = x4*cos60 + y4*sin60
    mem_y4 = (-x4*sin60 + y4*cos60)*cosZ

    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x1,mem_y1,mem_x3,mem_y3,mem_x4,mem_y4,mem_x2,mem_y2)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x3,mem_y3,mem_x3,mem_y3+mem_layer_thikness,mem_x4,mem_y4+mem_layer_thikness,mem_x4,mem_y4)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(155,155,100);stroke:purple;stroke-width:1" />'''%(mem_x4,mem_y4,mem_x4,mem_y4+mem_layer_thikness,mem_x2,mem_y2+mem_layer_thikness,mem_x2,mem_y2)
    k+=1
  
  print >> outputobj,'''</g>
</svg>
'''


if __name__ == '__main__':
  print("main")
  floorplan = '.'
  interposer = '.'
  tim_mem = '.'
  tim_core = '.'
  core_dim = []
  mem_dim = []
  core_flag = False
  mem_flag = False
  outputfilename = None
  outputfolder = ''
  formatdefaultoutputfile = {'svg': 'floorplan.svg', 'text': 'floorplan.txt'}
  validformats = ('svg', 'text')
  format = 'svg'
  
  # def usage():
  #   print 'Usage: %s [-h|--help (help)] [-c|--core (core)] [-m|--mem (mem)] [-d <floorplan (.)>]  [-o|--output (output filename/"-" for stdout)]  [-f|--format (options: %s)]' % (sys.argv[0], validformats)

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:c:m:o:f:i:t:z:", [ "help","core", "mem", "output=", "format=" ])
  except getopt.GetoptError, e:
    print e
    #usage()
    sys.exit()
  for o, a in opts:
    if o == '-h' or o == '--help':
      #usage()
      sys.exit()
    elif o == '-d':
      floorplan = a
    elif o == '-i':
      interposer = a
    elif o == '-t':
      tim_mem = a
    # elif 0 == '-tc':
    #     tim_core = a
    elif o == '-o' or o == '--output':
      outputfilename = a
    elif o == '-z':
      outputfolder = a
    elif o == '-c':
      dim = a.split(',')
      core_dim = [int(xyz) for xyz in dim]
      core_flag = True
    elif o == '-m':
      dim = a.split(',')
      mem_dim = [int(xyz) for xyz in dim]
      mem_flag = True
    else:
      #usage()
      sys.exit()
  
  if outputfilename == None:
    outputfilename = formatdefaultoutputfile[format]

  if outputfilename == '-':
    output = sys.stdout
  else:
    output = open(outputfolder+outputfilename, 'w')
  print("start")
  if (mem_flag):
    floorplan_3D_mem(floorplan, tim_mem, format = format, mem_dim=mem_dim, outputobj = output)
  elif (core_flag):
    floorplan_3D_core(floorplan, tim_mem, format = format, mem_dim=core_dim, outputobj = output)
  print("End of Code")

#core with air
#$ python gen_floorplan3Dmem.py -d 3Dmem_air_4core/cores_1.flp -t 3Dmem_air_4core/core_tim.flp -c 2,2,1 -o view_core.svg -z ~/CoMeT/tools/3Dmem_air_4core/

#mem with air
#$ python gen_floorplan3Dmem.py -d ../3Dmem_16core_air/mem_ctrl.flp -t ../3Dmem_16core_air/mem_tim.flp -m 4,4,8 -o view_mem.svg -z ../3Dmem_16core_air/
