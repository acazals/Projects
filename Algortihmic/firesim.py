#!/usr/bin/python

from PIL import Image
from numpy import asarray
import numpy as np
#import random
import argparse
import sys
import random
import os
import re
import matplotlib.pyplot as plt
import statistics
from scipy import stats


# RGB colors
rgb_alive = [86, 130, 3]
rgb_notree = [88, 41, 0]
rgb_burning = [255,0,0]
rgb_burned = [128,128,128]

# labels used for trees
alive = 0
burning = 1
burned = 2
notree = 3

# Convert an image into an RGB matrix, with 2 colors: one for trees, one for the
# remaining pixels
def get_rgb_matrix(filename):
  img = Image.open(filename)

  t = asarray(img)
  n = len(t)
  m = len(t[0])
  I = np.zeros((n,m,3), dtype="uint8") # creates a  matrix n x m with triples of zeroes

  # for each pixel, if g dominates: creates a green cell; red otherwise
  for i in range (n):
  	for j in range(m):
	   if (t[i][j][1]>t[i][j][0] and t[i][j][1]>t[i][j][2]):
	     	I[i][j] = rgb_alive
	   else :
	   	 I[i][j] = rgb_notree
  return I


# get the offsets (-1, 0, +1) of the neighbors of the cell (i,j) in matrix M
# NB: topology==4 or 8, that is 4 or 8 neighbors
# NB: a list of pairs (a,b) is returned
def get_neighbors_offsets(M,i,j, topology):
  L = []
  n = len (M)
  m = len (M[0])
  # (-1,0,1): offset with repect to i; likewise for j
  for a in range(-1,2):
    for b in range(-1,2):
      # select the four neighbors above/below/left/right; remove center  + corners
      if 0<=i+a<=n-1 and 0<=j+b<=m-1:
        if topology == 4:
          if not ((a==0 and b==0) or (a== -1 and b==-1) or (a==-1 and b==1) or (a==1 and b==-1) or (a==1 and b==1)):
            L.append((a, b))
        # anto: a toi de jour
        elif topology == 8:
         if not (a==0 and b==0):
           L.append((a, b))
        else:
          sys.exit("Connectivity must be 4 or 8")
  return(L)

# if voxel (i,j) is not burning: return empty list
def alive_neighbors_offsets_of_burning_voxel(M,i,j, topology):
  if M[i][j][0] != burning:
    return []

  L = get_neighbors_offsets(M, i,j, topology) # neighbor: pair of indices [i,j]
  P=[]
  for k in range(len(L)):
    # coords of the neighbors
    a=L[k][0]; 	b=L[k][1]
    if M[i+a][j+b][0] == alive:
      P.append(L[k])
  return P

## NB: neighbors presented as tuples (i,j) not lists [i,j], to make them hashable in sets
#i################################################################################
class Fire_simulation:

  # create the forest matrix M; set the simulation parameters
  def __init__(self, options):
    self.options = options

    self.num_trees_total = 0
    self.wind = [0, 0] # wind: default is no wind

    self.ofname_prefix = "" # prefix used for the output files
    self.dfname_stats = "" # filename to dump stats
    self.dfname_pict = ""  # filename to dump images

    self.p_hat_estimation = [] #list of pairs of integers to estimate p: see below

  # prepares self.M_forest, and counts the total number of trees
  def get_forest_matrix(self, rgb_matrix):
    self.num_trees_total = 0
    n = len(rgb_matrix)
    m = len(rgb_matrix[0])
    #self.M_forest = np.zeros((n, m, 2), dtype="uint8")
    self.M_forest = np.zeros((n, m, 2), dtype="int16")

    for i in range(n):
      for j in range (m):
        keep_tree = True
        a = random.randint(0,100) # percentage
        if a < 100*self.options.trim_proba:
          keep_tree = False

        if rgb_matrix[i][j][0] == rgb_alive[0] and keep_tree:
          self.M_forest[i][j] = [alive,0]
          self.num_trees_total += 1
        else:
          self.M_forest[i][j] = [notree, 0]

    print("Image n m size num-trees:", n, m, n*m, self.num_trees_total)

  # collect all simulation files from the current directory
  # stats
  # Format for a stats file is:
  #id proba iteration burning_trees burned_trees burned_trees_total burned_trees_total_perc
  # run-id 0.35 1 1 4  0
  def stats_burning(self):
    cmd = "ls  %s/*-stats.txt" % self.options.odir
    files = os.popen(cmd).readlines()
    results = []
    proba_to_fraction = dict()
    for afile in files:

      lines = open(afile.rstrip()).readlines()
      if len(lines)==1: # header only found: nothing has been dumped
        continue

      # from line, retrieve run id + proba + fraction of burned trees
      last_line = lines[-1].rstrip()
      aux = re.split(r"\s+", last_line) # split the last line using blanks: we expect 5 numbers
      simul_id = int(aux[0])
      proba = float(aux[1])
      fraction = float(aux[-1])

      if proba in proba_to_fraction:
        proba_to_fraction[ proba ].append(fraction)
      else:
        proba_to_fraction[ proba ] = [fraction]

    # for each proba value: pick the median fraction
    for proba in proba_to_fraction.keys():
      m = statistics.median( proba_to_fraction[proba] )
      results.append([proba, m])

    xs = [r[0] for r in results]
    ys = [r[1] for r in results]
    plt.plot(xs, ys,  '--bo')
    plt.xlabel('Probabilite')
    plt.ylabel('% arbres brules')

    dfname = "%s/%s-burned-trees-topo%s-trim%.2f-res.png" % \
      (self.options.odir, self.ofname_prefix, self.options.topo, self.options.trim_proba)
    plt.savefig(dfname)
    plt.clf()
    # plt.show()

    cmd = "cp %s ~/attach/tipe" % dfname
    os.system(cmd)

  def stats_p_hat(self):
    proba_to_fraction = dict()

    xs = []; ys = []; zs = []
    lines = open(self.dfname_phat).readlines()
    for line in lines:
      aux = re.split(r"\s+", line.rstrip())
      proba = float(aux[0])
      phat = float(aux[1])
      if proba in proba_to_fraction:
        proba_to_fraction[ proba ].append(phat)
      else:
        proba_to_fraction[ proba ] = [phat]

    tmp = []
    for proba in proba_to_fraction.keys():
      tmp.append( (proba, statistics.median(proba_to_fraction[proba])) )
    ord =  sorted(tmp)
    for t in ord:
      xs.append(t[0])
      ys.append(t[1])
      zs.append(t[0])

    # linear regression
    ls = []
    slope, intercept, r_value, p_value, std_err = stats.linregress(xs, ys)
    print("slope and r-squared:", slope, r_value**2)
    for x in xs:
      ls.append(intercept +slope*x)

    # plot: simulation
    plt.plot(xs, ys,  '--bo', color='r', label='Simuation')  # Simulation
    # plot: linear regression
    plt.plot(xs, ls, color='r',   label='Regression lineaire')
    # plot: y=x for reference
    plt.plot(xs, zs, color='g',   label='y=x')

    plt.xlabel('Proba')
    plt.ylabel('Estimation')

    plt.legend()
    dfname = "%s/%s-ML-estimation-topo%s-trim%.2f-res.png" % \
      (self.options.odir, self.ofname_prefix, self.options.topo, self.options.trim_proba)
    plt.savefig(dfname)
    plt.clf()
    # plt.show()

    cmd = "cp %s ~/attach/tipe" % dfname
    os.system(cmd)

  # return a pair (number of burned trees, new matrix)
  def one_iteration(self, iteration):
    Mp1 = self.M_forest # M plus one: forest at the nex iteration
    n=len(self.M_forest); m=len(self.M_forest[0])

    burned_trees = 0
    burning_trees = 0

    # now compute for this iteration: #new_burning #candidate
    candidates = set()
    burning_new = set()

    for i in range(n):
        for j in range (m):
            if self.M_forest[i,j,0] == burning:
              neighbors_offsets = alive_neighbors_offsets_of_burning_voxel(self.M_forest, i, j, self.options.topo)

              # tree is burning, but was not lit during this iteration
              if self.M_forest[i,j,1] != iteration:
                for x in neighbors_offsets:
                    a = x[0]; b = x[1]

                    candidates.add( (i+a, j+b) )

                    # fire transmission prob is the sum of the default proba + contribution of the wind;
                    # the latter is the dot product between offset vector and the wind vector
                    # if sucess: the neighbor will burn too
                    r = random.randint(1,100)
                    if r <= (self.options.p*100+ 10*(a*self.wind[0]+b*self.wind[1])):
                        burning_new.add( (i+a,j+b) )
                        Mp1[i+a,j+b]=[burning, iteration]
                        self.M_rgb[i+a,j+b]=rgb_burning
                        burning_trees += 1

              # tree burned during self.burning_time steps: dead
              if iteration-self.M_forest[i,j,1] >= self.options.burning_time:
                Mp1[i][j][0] = burned
                self.M_rgb[i][j] = rgb_burned
                burned_trees += 1

    # update the forest data structure for the  next iteration
    #msg = "iteration - burning trees - burned trees: %s %s %s" % (iteration, burning_trees, burned_trees)
    #print(msg)

    for i in range(n):
        for j in range (m):
            self.M_forest[i,j]=Mp1[i,j]

    # record the information to estimate p_hat
    if burning_trees != len(burning_new):
      sys.exit("problem")
    self.p_hat_estimation.append( [len(burning_new), len(candidates) ] )
    return (burning_trees, burned_trees, Mp1)


#n= taille du carré, p= probabilité de transmission, d-nombre de départs de feu, t=nombre de tours durant lesquels brulent les arbres, q = percolation de la forêt, vent=[x,y] intensité du vent selon x et y. x positif vent de haut en bas, y positif vent de gauche à droite
  def simulation(self):
    n=len(self.M_forest); m=len(self.M_forest[0])
    msg = "Running iteration on matrix of size %s and %s for %s voxels" % (n,m,n*m)
    print(msg)

    c = n//2; d = m//2
    self.M_forest[c,d] = [burning,0]
    self.M_forest[c+1, d] = [burning,0]
    self.M_forest[c, d+1] = [burning,0]
    self.M_forest[c+1, d+1] = [burning,0]

    iteration=1
    burned_trees_total = 0

    f=open(self.dfname_stats, "w") # open file to append a line
    f.write("#proba iteration burning_trees burned_trees burned_trees_total burned_trees_total_perc\n")
    f.close()

    while True:
      (burning_trees, burned_trees, Mp1) = self.one_iteration(iteration)
      # print("Iter burning_trees, burned_trees", iteration, burning_trees, burned_trees)
      burned_trees_total += burned_trees

      burned_perc = 100.0*burned_trees_total / self.num_trees_total
      if burning_trees == 0:
        break

      # store image1
      # output_filename = "forestM-windx%s-windy%s-iteration%s.png" % (self.wind[0], self.wind[1], iteration)
      # X = Image.fromarray(Mp1)
      # X.save(output_filename)

      if self.options.picts:
        X = Image.fromarray(self.M_rgb)
        self.dfname_pict       = "%.2f-iteration%s-pict.png" % (self.options.p, iteration)
        X.save(self.dfname_pict)

      # update statistics
      f=open(self.dfname_stats, "a") # open file to append a line
      line = "%d %.2f %s %s %s %2.f" % \
        (self.options.id, self.options.p, iteration, burning_trees, burned_trees, burned_perc)
      print("Simul-id / proba  / iteration / burning trees / burned trees:", line)
      f.write(line + "\n")
      f.close()

      iteration = iteration+1

    # when done: store the last pict in any case
    X = Image.fromarray(self.M_rgb)
    X.save(self.dfname_pict_final)

    # at least 2 iterations needed
    if  iteration == 1:
      return

    # estimation of the proba from the trees reached / starting to burn at each iteration
    nn = 0; mm = 0
    for k in range(0, len(self.p_hat_estimation)):
      nn += self.p_hat_estimation[k][0] # new burning
      mm += self.p_hat_estimation[k][1] # candidates
    p_hat = float(nn)/mm
    print("Estimation: ", p_hat)

    f=open(self.dfname_phat, "a") # open file to append a line
    line = "%.2f %.2f" % (self.options.p, p_hat)
    f.write(line + "\n")
    f.close()

  def run(self):
    (dd, ff) = os.path.split(self.options.fname)
    self.ofname_prefix      = re.sub(r"\\.\w{3}","",ff);    # name of the file containing the image

    # output directory: exists, or create
    if self.options.odir:
      if not os.path.exists(self.options.odir):
        sys.exit("You passed a directory which does not exist")
    else:
      # prepare the prefix of output filenames
      self.options.odir = "%s-topo%s-windx%s-windy%s-trim%.2f" % \
        (self.ofname_prefix, self.options.topo,  self.wind[0], self.wind[1], self.options.trim_proba)

      # run mode only: if self.options.odir pre-exists, remove and re-create
      if self.options.mode == "run" and os.path.exists(self.options.odir):
        cmd = "rm -rf %s" % self.options.odir; print(cmd); os.system(cmd)
      cmd = "mkdir %s"  % self.options.odir; print(cmd); os.system(cmd)

    self.dfname_stats      = "%s/proba%.2f-id%s-stats.txt" % (self.options.odir, self.options.p,  self.options.id)
    self.dfname_pict_final = "%s/proba%.2f-id%s-pict.png"  % (self.options.odir, self.options.p, self.options.id)
    self.dfname_phat       = "%s/p-hat.txt" % self.options.odir


    # run the simulation
    if self.options.mode == "run":
      # directory into which results are stored
      self.M_rgb = get_rgb_matrix(self.options.fname)
      self.get_forest_matrix(self.M_rgb)
      self.simulation()
    # run the stats
    elif self.options.mode == "stats":
      self.stats_burning()
      self.stats_p_hat()
    else:
      print("Provide the option run for the simulation, and stats for the statistics")


#i################################################################################
# Options of the simulation in the command line of the shell
parser = argparse.ArgumentParser(description='My parser')

parser.add_argument("-f", "--fname", dest="fname", default="data/foret-ciel-small.jpg", help="Image filename")
parser.add_argument("--trim", dest="trim_proba", type=float, default=0.0, help="Trim proba. If 0 (default), no trimming takes place")

parser.add_argument("-p", "--proba", dest="p", default=0.3,type=float, help="Fire propagation probability")
parser.add_argument("-b", "--burning_time", dest="burning_time", default=3,type=int, help="Burning time")
parser.add_argument("-t", "--topo", dest="topo", default=4,type=int, help="Connectivity of a pixel: 4 or 8 neighbors")

parser.add_argument("--odir", dest="odir", help="Output directory name for the results")
parser.add_argument("-i", "--id", dest="id", type=int, default=0, help="Simulation id when running repeats")
parser.add_argument("--pict", action="store_true", default=False, dest="picts", help="Store pictures at every iteration")

parser.add_argument("-m", dest="mode", help="Mode: run or stats")

options = parser.parse_args()

# The simulation
fire   = Fire_simulation(options) # create the instance of the simulation
fire.run()     # run the simulation
