#!/usr/bin/python


from scipy.integrate import odeint
from pylab import *
from random import *

#constantes
g = 9.8
#acceleration de la pesanteur
f = 0.0001 #taux de combustion
p = 1.225 #masse volumique de l’air
T0 = 300 #Temperature ambiante
Cp = 1400 #capacite thermique massique du papier
s = 5.67*10**(-8) #constante de steffan boltzmann
e = 0.9 #[U+FFFD]missivit[U+FFFD]
h = 5 #coefficient de transfert thermique
T0=300 #Temperature ambiante
Tig = 600 #Temperature d’ignition du gazon
v_f = 1 #vitesse de propagation de l’incendie
L=[200, 600, 1000, 1300, 1800, 2200] #masses volumiques
Cp = [10,100,200,500,1000,2000] #capacites thermiques massiques
M = [[0.1*i+0.05,0,0] for i in range(1000)]
PP1, PP2 = [], []
mtot=0

class Wind:
    @staticmethod
    def wind(y):
        #profile du vent quadratique

        yref=10
        wxref=12
        k=0.28 #puissance empirique

        return wxref*((y/yref)**k)

    @staticmethod
    def get_wind(p0_1):
        wyref=0
        return [Wind.wind(p0_1), wyref]

class Brandon:
  def __init__(self):
    #masse initiale
    self.m0 = expovariate(1000)
    #altitude initiale
    z0 = expovariate(0.1)
    #Composition
    C0 = randrange(6)
    r = L[C0]
    Cp = L[C0]
    #Forme
    self.F0 = randrange(0,2)

    #position initiale
    # no y coord: points travel in the xz plane perpendicular to the firefront
    p0=[0,z0]
    self.pos_x = [p0[0]]
    self.pos_z = [p0[1]]

   # vitesse initiale selon x et y
    v0 = [2,0]
    self.vx=[v0[0]]
    self.vz=[v0[1]]

    #masse du brandon
    self.K1 = f*(4*pi*r)**(1/3)*(3**(-1/3))
    self.K2 = f*self.m0**(2/3)*(r*pi/100)**(1/3)

    #surface du brandon
    self.A0 = (pi/5*((100*self.m0)/(pi*r))**(2/3))*(1-self.F0)+ 4*pi*(((3*self.m0)/(4*pi*r))**(2/3))**2 # xfc

  def get_F0(self):
      return self.F0

  def get_pos_latest_x(self):
      return self.pos_x[-1]
  def get_pos_latest_z(self):
      return self.pos_z[-1]
  def get_velocity_latest_x(self):
      return self.vx[-1]
  def get_velocity_latest_z(self):
      return self.vz[-1]


  def append_position(self, ax, az):
      self.pos_x.append(ax)
      self.pos_z.append(az)

    # append velocities to the vector of velocities
  def append_velocities(self, avx, avz):
      self.vx.append( avx)
      self.vz.append( avz)


  def get_initial_position(self):
      return [self.pos_x[0], self.pos_z[0]]

  def m(self, t):
      mm = (self.m0-self.K2*t)*(1-self.F0) + (self.m0**(1/3) - self.K1*t)**(1/3)*self.F0
      #if math.isnan(mm):
      #    print(self.m0, self.K2*t, self.F0, mm)
      return mm

    #derivee de la masse
  def dm(self, t):
      return -self.K2*(1-self.F0)-self.K1*self.F0*3*(self.m0**(1/3)-self.K1*t)**2

  def A(self, t):
      return self.A0*(self.m(t)/self.m0)*(1-self.F0)+self.F0*self.A0*(self.m(t)/self.m0)**(2/3)


#i################################################################################
tatt = 0 # xfc; temps atterissage
for l in range(100):

    # creationbrandon
    bra = Brandon()

    w = Wind.get_wind( bra.get_initial_position()[1] )

    #coefficient de trainee
    Cd = 0.49*bra.get_F0()+0.82*(1-bra.get_F0())

    #Resolution de l’equation differentielle du mouvement
    def fx(x,y,t):
        # return 1/m(t)*(-dm(t)*x-(0.5*p*Cd*A(t)*((x-w[0]+v_f)**2+(y-w[1])**2)**0.5
        # nn = ()**0.5
        nn = (x-w[0]+v_f)**2+(y-w[1])**2
        if nn<0:
            print(nn); sys.exit(0)
        return 1/bra.m(t) * (-bra.dm(t)*x - (0.5*p*Cd*bra.A(t) * math.sqrt(nn) * (x-w[0]+v_f) ) )

    def fy(x,y,t):
        # return 1/m(t)*(-dm(t)*y-m(t)*g-(0.5*p*Cd*A(t)*((x-w[0]+v_f)**2+(y-w[1])**
        nn = (x-w[0]+v_f)**2+(y-w[1])**2
        if nn<0:
            print(nn); sys.exit(0)
        tmp = 1/bra.m(t) * (-bra.dm(t)*y -(0.5*p*Cd*bra.A(t)* math.sqrt(nn) * (y-w[1]+v_f) -bra.m(t)*g ))
        return tmp


    for i in range(0,1000):
        t=linspace(0.1*i,0.1*(i+1),100) # 100 steps in [n,n+1], n=0..999
        vxi = bra.get_velocity_latest_x()
        vzi = bra.get_velocity_latest_z()

        for j in range(1,len(t)):
            # make sure thr brandon has not melted !
            if bra.m(t[j]) <= 0.00001 :
                 print("Small mass, exiting")
                 break

            # update velocities
            a=(t[j]-t[j-1])*(fx(vxi,vzi,t[j]))+vxi
            b=(t[j]-t[j-1])*(fy(vxi,vzi,t[j]))+vzi
            bra.append_velocities(a, b)

            c = bra.get_pos_latest_x() + a*(t[j]-t[j-1]) + 0.5*fx(vxi,vzi,t[j])*((t[j]-t[j-1])**2)
            d = bra.get_pos_latest_z() + b*(t[j]-t[j-1]) + 0.5*fy(vxi,vzi,t[j])*((t[j]-t[j-1])**2)
            if d<0:
                tt=t[j]
                break
            bra.append_position(c, d)
            vxi=a
            vzi=b

        if bra.m(t[j]) <= 0.00001 :
            print("Small mass, exiting")
            break

        if d<0:
            tatt=t[j]
            break
        w[0] = Wind.wind( bra.get_velocity_latest_z() )
        Bb= [tatt, bra.get_pos_latest_x() ] #temps et position d’atterrissage
