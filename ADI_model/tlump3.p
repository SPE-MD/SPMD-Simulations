*one 10cm segment for a lumped transmission line model
.subckt tlump t1p t1n t2p t2n rtn
rx t1p rtn 1e9
g1 t1p a t1p a laplace=1/(1.134268e-5*((abs(s)/(2*pi))^0.5))
l1 a t2p {1*20.6435n}
c1 t2p rtn {1*2.25026p}
r1 t1n rtn 1e-6
r2 t2n rtn 1e-6
.ends tlump
