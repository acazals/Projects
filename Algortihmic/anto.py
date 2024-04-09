
# transforms the image into a matrix
def image (nom):
  im=Image.open(nom)
  T=array(im)
  n=len(T)
  m=len(T[0])
  H =zeros((n,m,3), dtype="uint8")
  for i in range (n):
  	for j in range(m):
	   if (T[i][j][1]>T[i][j][0] and T[i][j][1]>T[i][j][2]):
	     	H[i][j]=[86, 130, 3]
	   else :
	   	 H[i][j]=[88, 41, 0]
  return (H)



def foret (T):
  n=len (T)
  m=len (T[0])
  M=zeros((n, m, 2), dtype="uint8")
  for i in range(n):
  	for j in range (m):
	   if T[i][j][0]==86:
	      M[i][j]=[0,-1]
	   else:
	      M[i][j]-[3, -1]
  return (M)



def foret_elague (T,d):
  n=len (T)
  m=len (T[0])
  M=zeros((n,m,2), dtype="uint8")
  d=d*100
  for i in range(n):
  	for j in range (m):
	    a=randint(0,100)
	    if T[i][j][0]==86 and a>d:
	       M[i][j]=[0,-1]
	    else:
	       M[i][j]=[3, -1]
  return(M)

def depart(M):
  n=len(M)
  m=len(M[0])
  a=randint(0,n-1)
  b=randint(0,m-1)
  M[a][b]=[1,0]


def voisins (M,i,j):
  L=[]
  n=len (M)
  m=len (M[0])
  for a in range(-1,2):
  	for b in range(-1,2):
	     if 0<=i+a<n and 0<=j+b<m and not ((a==0 and b==0) or (a== -1 and b==-1) or (a==1 and b==-1) or (a==1 and b==1)):
	       L.append((i+a, j+b))
  return(L)




def nb_voisins_feu (M,i,j):
  C=0
  L=voisins(M,i,j)
  P=[]
  for k in range(len(L)):
    f=L[k][0]
    g=L[k][1]
    if M[f][g][0]==1:
      c+=1
      P.append(L[k])
  return (c,P)





















def evolution (nom, p, t, vent, y):

#n= taille du carré, p= probabilité de transmission, d-nombre de départs de feu, t=nombre de tours durant lesquels brulent les arbres, q = percolation de la forêt, vent=[x,y] intensité du vent selon x et y. x positif vent de haut en bas, y positif vent de gauche à droite

  T=image (nom)
  M=foret (T)
  V=foret (T)
  n=len (M)
  m=len (M[0])
  h=0 #nombre d'arbres brûlés
  M[n//2][m//2]=[1,0]
  M[n//2-1][m//2]=[1,0]
  M[n//2-1] [m//2+1]=[1,0]
  M[n//2] [m//2+1]=[1,0]
  k=1
  change=True
  while change==True:
    change=False
    for i in range (n):
      for j in range (m):

        S=nb_voisins_feu (M,i,j)
        P=S[1]
	      #if M[i][j][0]==0 and len(P)>0:
        if ((M[i][j][0]==0) and (len(P)>0)):
	        for x in P:
	          r=randint (1,100)
	          a=i-x[0]
	          if a!=0:
	            a=a/abs(a)
	            b=j-x[1]
	          if b!=0:
	            b=b/abs (b)
	          if r<=(p*100+ (a*vent [0] *10)+(b*vent [1]*10)):
	            V[i][j]=[1,k]
	            T[i][j]=(255,0,0)
	            change=True
        if M[i][j][1]<=k-t and M[i][j][0]==1:
          #quand un arbre a brulé pendant t étapes, il s'éteint
	        V[i][j][0]=2
	        T[i][j]=(128,128,128)
	        h+=1
	        change=True
    for i in range(n):
      for j in range (m):
        M[i][j]=V[i][j]
  X-Image.fromarray(T)
  if k==1:
    X.save(r'images'+str(y)+'\img'+str(k)+', p='+str(p)+', vent ='+str(vent)+', t='+str(t)+'.png')
  else :
    X.save(r'images'+str(y)+'\img'+ str(k)+'.png')
    k=k+1
  f=open("Résultats "+str(y), "a")
  f.write("nombre d'arbres brûlés="+str(h)+", str(k) "+" tours"+", proportion de forêt brulée="+str(int((n*m)*10000)/100)+"%")
  f.close()
  return("Terminé"+str(y))
