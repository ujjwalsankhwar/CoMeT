#!/usr/bin/env python

from distutils import core
import sys, os, math, collections, sniper_lib, sniper_stats, sniper_config, getopt

def gen_floorplan(floorplan, interposer, format = 'svg', core_dim=[], mem_dim=[], outputobj = sys.stdout):
  print("gen_floorplan")
  core_layer_thikness = 500#variable (10x)
  mem_layer_thikness = 500#variable (10x)
  tim_layer_thikness = 200#variable (10x)
  cos60 = 0.7071#0.866025#0.5
  sin60 = -0.7071#-0.5#0.866025
  cosz = 1
  cosZ = 0.7071#0.866025
  file = open(floorplan, mode = 'r')
  lines = file.readlines()
  file.close()
  corex = int(core_dim[0])
  corey = int(core_dim[1])
  corez = int(core_dim[2])
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
  file = open(interposer, mode = 'r')
  lines = file.readlines()
  file.close()
  flag = False
  interposer_height = 0
  interposer_width = 0
  origin_x = 0
  origin_y = 0
  for line in lines:
    if (flag):
      line = line.split('\t')
      temp_line = []
      interposer_width = int(float(line[1])*1000000)
      interposer_height = int(float(line[2])*1000000)
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
'''%(origin_x,origin_y,2*interposer_width,3*interposer_height)
  print >> outputobj, '''\
<g id="floorplan" style="stroke: none; fill: red;">
  <rect x="%d" y="%d" width="%d" height="%d" style="fill:rgb(0,255,153)" />
  '''%(origin_x,origin_y,2*interposer_width,3*interposer_height)
  #core
  k=0
  while (k<corez):
    i=corey-1
    j=0
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    core_x1 = 0
    core_x2 = 0
    core_x3 = 0
    core_x4 = 0
    core_y1 = 0
    core_y2 = 0
    core_y3 = 0
    core_y4 = 0
    #i==0 and j==0
    i=0
    j=0
    x1 = arr[i*corex+j][2]+interposer_width-(core_layer_thikness+tim_layer_thikness)*k
    y1 = (arr[i*corex+j][3])-(core_layer_thikness+tim_layer_thikness)*k
    core_x1 = x1*cos60 + y1*sin60
    core_y1 = (-x1*sin60 + y1*cos60)*cosZ

    i=0
    j=corex-1
    x2 = arr[i*corex+j][2]+arr[i*corex+j][0]+interposer_width-(core_layer_thikness+tim_layer_thikness)*k
    y2 = (arr[i*corex+j][3])-(core_layer_thikness+tim_layer_thikness)*k
    core_x2 =  x2*cos60 + y2*sin60
    core_y2 = (-x2*sin60 + y2*cos60)*cosZ

    i=corey-1
    j=0
    x1 = arr[i*corex+j][2]+interposer_width-(core_layer_thikness+tim_layer_thikness)*k
    y1 = (arr[i*corex+j][3]+arr[i*corex+j][1])-(core_layer_thikness+tim_layer_thikness)*k
    core_x3 = x1*cos60 + y1*sin60
    core_y3 = (-x1*sin60 + y1*cos60)*cosZ

    i=corey-1
    j=corex-1
    x2 = arr[i*corex+j][2]+arr[i*corex+j][0]+interposer_width-(core_layer_thikness+tim_layer_thikness)*k
    y2 = (arr[i*corex+j][3]+arr[i*corex+j][1])-(core_layer_thikness+tim_layer_thikness)*k
    if (i==corey-1 and j==corex-1):
      core_x4 = x2*cos60 + y2*sin60
      core_y4 = (-x2*sin60 + y2*cos60)*cosZ
    #3D effect thickness applied
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(255,255,0);stroke:purple;stroke-width:1" />'''%(core_x1,core_y1,core_x3,core_y3,core_x4,core_y4,core_x2,core_y2)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(255,255,0);stroke:purple;stroke-width:1" />'''%(core_x3,core_y3,core_x3,core_y3+core_layer_thikness,core_x4,core_y4+core_layer_thikness,core_x4,core_y4)
    print >> outputobj,'''<polygon points="%d,%d %d,%d %d,%d %d,%d" style="fill:rgb(255,255,0);stroke:purple;stroke-width:1" />'''%(core_x4,core_y4,core_x4,core_y4+core_layer_thikness,core_x2,core_y2+core_layer_thikness,core_x2,core_y2)
    
    
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(core_x3,core_y3,core_x3,core_y3+core_layer_thikness)
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(core_x4,core_y4,core_x4,core_y4+core_layer_thikness)
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(core_x2,core_y2,core_x2,core_y2+core_layer_thikness)
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(core_x3,core_y3+core_layer_thikness,core_x4,core_y4+core_layer_thikness)
    print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(core_x4,core_y4+core_layer_thikness,core_x2,core_y2+core_layer_thikness)
    

    i=corey-1
    j=0
    while (i>-1):
      j=0
      while (j<corex):
        #print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[i*corex+j][2],arr[i*corex+j][3],arr[i*corex+j][2]+arr[i*corex+j][0],arr[i*corex+j][3])
        x1 = arr[i*corex+j][2]+interposer_width-(core_layer_thikness+tim_layer_thikness)*k
        y1 = (arr[i*corex+j][3])-(core_layer_thikness+tim_layer_thikness)*k
        x2 = arr[i*corex+j][2]+arr[i*corex+j][0]+interposer_width-(core_layer_thikness+tim_layer_thikness)*k
        y2 = (arr[i*corex+j][3])-(core_layer_thikness+tim_layer_thikness)*k
        print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
        x1 = arr[i*corex+j][2]+interposer_width-(core_layer_thikness+tim_layer_thikness)*k
        y1 = (arr[i*corex+j][3])-(core_layer_thikness+tim_layer_thikness)*k
        x2 = arr[i*corex+j][2]+interposer_width-(core_layer_thikness+tim_layer_thikness)*k
        y2 = (arr[i*corex+j][3]+arr[i*corex+j][1])-(core_layer_thikness+tim_layer_thikness)*k
        print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
        x1 = arr[i*corex+j][2]+arr[i*corex+j][0]+interposer_width-(core_layer_thikness+tim_layer_thikness)*k
        y1 = (arr[i*corex+j][3])-(core_layer_thikness+tim_layer_thikness)*k
        x2 = arr[i*corex+j][2]+arr[i*corex+j][0]+interposer_width-(core_layer_thikness+tim_layer_thikness)*k
        y2 = (arr[i*corex+j][3]+arr[i*corex+j][1])-(core_layer_thikness+tim_layer_thikness)*k
        print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
        x1 = arr[i*corex+j][2]+interposer_width-(core_layer_thikness+tim_layer_thikness)*k
        y1 = (arr[i*corex+j][3]+arr[i*corex+j][1])-(core_layer_thikness+tim_layer_thikness)*k
        x2 = arr[i*corex+j][2]+arr[i*corex+j][0]+interposer_width-(core_layer_thikness+tim_layer_thikness)*k
        y2 = (arr[i*corex+j][3]+arr[i*corex+j][1])-(core_layer_thikness+tim_layer_thikness)*k

        print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
        #print >> outputobj,'''<text x="%d" y="%d" fill="black" text_anchor="start" style="font-size:570" > C%d_%d </text>'''%(arr[i*corex+j][2]+100,arr[i*corex+j][3]+2000,corey-1-i,j)
        j=j+1
      i=i-1
    k=k+1

  #mem
  start_mem = corex*corey#*corez
  mem_size = memx*memy#*memz
  nth_mem = 0
  while (nth_mem<4):
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
      x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+interposer_width-(mem_layer_thikness+tim_layer_thikness)*k
      y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
      
      mem_x1 = x1*cos60 + y1*sin60
      mem_y1 = (-x1*sin60 + y1*cos60)*cosZ

      i=0
      j=memx-1
      x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+interposer_width-(mem_layer_thikness+tim_layer_thikness)*k
      y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
      mem_x2 =  x2*cos60 + y2*sin60
      mem_y2 = (-x2*sin60 + y2*cos60)*cosZ

      i=memy-1
      j=0
      x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+interposer_width-(mem_layer_thikness+tim_layer_thikness)*k
      y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
      mem_x3 = x1*cos60 + y1*sin60
      mem_y3 = (-x1*sin60 + y1*cos60)*cosZ

      i=memy-1
      j=memx-1
      x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+interposer_width-(mem_layer_thikness+tim_layer_thikness)*k
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
          x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+interposer_width-(mem_layer_thikness+tim_layer_thikness)*k
          y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
          x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+interposer_width-(mem_layer_thikness+tim_layer_thikness)*k
          y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
          print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
          x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+interposer_width-(mem_layer_thikness+tim_layer_thikness)*k
          y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
          x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+interposer_width-(mem_layer_thikness+tim_layer_thikness)*k
          y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
          print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
          x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+interposer_width-(mem_layer_thikness+tim_layer_thikness)*k
          y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3])-(mem_layer_thikness+tim_layer_thikness)*k
          x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+interposer_width-(mem_layer_thikness+tim_layer_thikness)*k
          y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
          print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
          x1 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+interposer_width-(mem_layer_thikness+tim_layer_thikness)*k
          y1 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
          x2 = arr[start_mem+nth_mem*mem_size+i*memx+j][2]+arr[start_mem+nth_mem*mem_size+i*memx+j][0]+interposer_width-(mem_layer_thikness+tim_layer_thikness)*k
          y2 = (arr[start_mem+nth_mem*mem_size+i*memx+j][3]+arr[start_mem+nth_mem*mem_size+i*memx+j][1])-(mem_layer_thikness+tim_layer_thikness)*k
          print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(x1*cos60 + y1*sin60, (-x1*sin60 + y1*cos60)*cosZ, x2*cos60 + y2*sin60, (-x2*sin60 + y2*cos60)*cosZ)
          j=j+1
        i=i-1
      k=k+1
    nth_mem = nth_mem+1
  print >> outputobj,'''</g>
</svg>
'''


  

if __name__ == '__main__':
  floorplan = '.'
  interposer = '.'
  core_dim = []
  mem_dim = []
  outputfilename = None
  outputfolder = ''
  formatdefaultoutputfile = {'svg': 'floorplan.svg', 'text': 'floorplan.txt'}
  validformats = ('svg', 'text')
  format = 'svg'

  # def usage():
  #   print 'Usage: %s [-h|--help (help)] [-c|--core (core)] [-m|--mem (mem)] [-d <floorplan (.)>]  [-o|--output (output filename/"-" for stdout)]  [-f|--format (options: %s)]' % (sys.argv[0], validformats)

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:c:m:o:f:i:z:", [ "help","core", "mem", "output=", "format=" ])
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
    elif o == '-o' or o == '--output':
      outputfilename = a
    elif o == '-z':
      outputfolder = a
    # elif o == '-f' or o == '--format':
    #   if a not in validformats:
    #     print >> sys.stderr, '%s is not a valid format' % a
    #     #usage()
    #     sys.exit()
    #   format = a
    elif o == '-c':
      dim = a.split(',')
      core_dim = [int(xyz) for xyz in dim]
    elif o == '-m':
      dim = a.split(',')
      mem_dim = [int(xyz) for xyz in dim]
    else:
      #usage()
      sys.exit()

  if outputfilename == None:
    outputfilename = formatdefaultoutputfile[format]

  if outputfilename == '-':
    output = sys.stdout
  else:
    output = open(outputfolder+outputfilename, 'w')
  gen_floorplan(floorplan, interposer, format = format, core_dim=core_dim, mem_dim=mem_dim, outputobj = output)
  print("End of Code")

#core with mem 3D
#$ python gen_floorplan3D.py -d ../2_5D_4_DRAM/core_and_mem_ctrl.flp -i ../2_5D_4_DRAM/interposer.flp -c 4,4,2 -m 2,2,8 -o view_core_mem.svg -z ../2_5D_4_DRAM/
