#!/usr/bin/env python

import sys, os, math, collections, sniper_lib, sniper_stats, sniper_config, getopt

def gen_floorplan(floorplan, interposer, format = 'svg', core_dim=[], mem_dim=[], outputobj = sys.stdout):
  print("gen_floorplan")
  file = open(floorplan, mode = 'r')
  lines = file.readlines()
  file.close()
  corex = int(core_dim[0])
  corey = int(core_dim[1])
  corez = int(core_dim[2])
  memx = int(mem_dim[0])
  memy = int(mem_dim[1])
  memz = int(mem_dim[2])

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
'''%(origin_x,origin_y,interposer_width,interposer_height)
  print >> outputobj, '''\
<g id="floorplan" style="stroke: none; fill: red;">
  <rect x="%d" y="%d" width="%d" height="%d" style="fill:rgb(0,255,153)" />
  '''%(origin_x,origin_y,interposer_width,interposer_height)
  #core
  i=corey-1
  j=0
  while (i>-1):
    j=0
    while (j<corex):
      print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[i*corex+j][2],arr[i*corex+j][3],arr[i*corex+j][2]+arr[i*corex+j][0],arr[i*corex+j][3])
      print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[i*corex+j][2],arr[i*corex+j][3],arr[i*corex+j][2],arr[i*corex+j][3]+arr[i*corex+j][1])
      print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[i*corex+j][2]+arr[i*corex+j][0],arr[i*corex+j][3],arr[i*corex+j][2]+arr[i*corex+j][0],arr[i*corex+j][3]+arr[i*corex+j][1])
      print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[i*corex+j][2],arr[i*corex+j][3]+arr[i*corex+j][1],arr[i*corex+j][2]+arr[i*corex+j][0],arr[i*corex+j][3]+arr[i*corex+j][1])
      print >> outputobj,'''<text x="%d" y="%d" fill="black" text_anchor="start" style="font-size:570" > C%d_%d </text>'''%(arr[i*corex+j][2]+100,arr[i*corex+j][3]+2000,corey-1-i,j)
      j=j+1
    i=i-1
  #mem
  start_mem = corex*corey
  i=memy-1
  j=0
  while (i>-1):
    j=0
    while (j<memx):
      print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_mem+i*memx+j][2],arr[start_mem+i*memx+j][3],arr[start_mem+i*memx+j][2]+arr[start_mem+i*memx+j][0],arr[start_mem+i*memx+j][3])
      print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_mem+i*memx+j][2],arr[start_mem+i*memx+j][3],arr[start_mem+i*memx+j][2],arr[start_mem+i*memx+j][3]+arr[start_mem+i*memx+j][1])
      print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_mem+i*memx+j][2]+arr[start_mem+i*memx+j][0],arr[start_mem+i*memx+j][3],arr[start_mem+i*memx+j][2]+arr[start_mem+i*memx+j][0],arr[start_mem+i*memx+j][3]+arr[start_mem+i*memx+j][1])
      print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_mem+i*memx+j][2],arr[start_mem+i*memx+j][3]+arr[start_mem+i*memx+j][1],arr[start_mem+i*memx+j][2]+arr[start_mem+i*memx+j][0],arr[start_mem+i*memx+j][3]+arr[start_mem+i*memx+j][1])
      print >> outputobj,'''<text x="%d" y="%d" fill="black" text_anchor="start" style="font-size:570" > LC%d_%d </text>'''%(arr[start_mem+i*memx+j][2]+100,arr[start_mem+i*memx+j][3]+500,memy-1-i,j)
      j=j+1
    i=i-1
  start_air = start_mem + memx*memy
	#X1
  print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_air][2],arr[start_air][3],arr[start_air][2]+arr[start_air][0],arr[start_air][3])
  print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_air][2],arr[start_air][3],arr[start_air][2],arr[start_air][3]+arr[start_air][1])
  print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_air][2]+arr[start_air][0],arr[start_air][3],arr[start_air][2]+arr[start_air][0],arr[start_air][3]+arr[start_air][1])
  print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_air][2],arr[start_air][3]+arr[start_air][1],arr[start_air][2]+arr[start_air][0],arr[start_air][3]+arr[start_air][1])
  print >> outputobj,'''<text x="%d" y="%d" fill="black" text_anchor="start" style="font-size:570" > X%d </text>'''%(arr[start_air][2]+100,arr[start_air][3]+570,1)
  #X2
  print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_air+1][2],arr[start_air+1][3],arr[start_air+1][2]+arr[start_air+1][0],arr[start_air+1][3])
  print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_air+1][2],arr[start_air+1][3],arr[start_air+1][2],arr[start_air+1][3]+arr[start_air+1][1])
  print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_air+1][2]+arr[start_air+1][0],arr[start_air+1][3],arr[start_air+1][2]+arr[start_air+1][0],arr[start_air+1][3]+arr[start_air+1][1])
  print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_air+1][2],arr[start_air+1][3]+arr[start_air+1][1],arr[start_air+1][2]+arr[start_air+1][0],arr[start_air+1][3]+arr[start_air+1][1])
  print >> outputobj,'''<text x="%d" y="%d" fill="black" text_anchor="start" style="font-size:570" > X%d </text>'''%(arr[start_air+1][2]+100,arr[start_air+1][3]+570,2)
  #X3
  print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_air+2][2],arr[start_air+2][3],arr[start_air+2][2]+arr[start_air+2][0],arr[start_air+2][3])
  print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_air+2][2],arr[start_air+2][3],arr[start_air+2][2],arr[start_air+2][3]+arr[start_air+2][1])
  print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_air+2][2]+arr[start_air+2][0],arr[start_air+2][3],arr[start_air+2][2]+arr[start_air+2][0],arr[start_air+2][3]+arr[start_air+2][1])
  print >> outputobj,'''<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:blue;stroke-width:30" />'''%(arr[start_air+2][2],arr[start_air+2][3]+arr[start_air+2][1],arr[start_air+2][2]+arr[start_air+2][0],arr[start_air+2][3]+arr[start_air+2][1])
  print >> outputobj,'''<text x="%d" y="%d" fill="black" text_anchor="start" style="font-size:570" > X%d </text>'''%(arr[start_air+2][2]+100,arr[start_air+2][3]+2000,3)
        
  print >> outputobj,'''</g>
</svg>
'''

  

if __name__ == '__main__':
  floorplan = '.'
  interposer = '.'
  core_dim = []
  mem_dim = []
  outputfilename = None
  formatdefaultoutputfile = {'svg': 'floorplan.svg', 'text': 'floorplan.txt'}
  validformats = ('svg', 'text')
  format = 'svg'

  # def usage():
  #   print 'Usage: %s [-h|--help (help)] [-c|--core (core)] [-m|--mem (mem)] [-d <floorplan (.)>]  [-o|--output (output filename/"-" for stdout)]  [-f|--format (options: %s)]' % (sys.argv[0], validformats)

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:c:m:o:f:i:", [ "help","core", "mem", "output=", "format=" ])
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
    output = open(outputfilename, 'w')
  gen_floorplan(floorplan, interposer, format = format, core_dim=core_dim, mem_dim=mem_dim, outputobj = output)
  print("End of Code")