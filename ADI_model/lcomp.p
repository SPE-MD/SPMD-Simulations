*compensating inductor model from coilcraft
.subckt coilcraft8085LS a b 
;ra a a1 25m ;misplaced resistance... this belongs somewhere else in the t-connectors
xlcomp a b lcomp params: l=76.2n k1=15e-6 k2=6.53e-1 c=2.08p r1=2010 r2=76.2m
.ends coilcraft8085LS

.subckt lcomp a b l=76.2n k1=15e-6 k2=6.53e-1 c=2.08p r1=2010 r2=92.8m
r2 a a1 {r2}
grv1 a1 lx a1 lx  laplace={1/(k1*sqrt(s/(2*pi)))}
grv2 a1 b  a1 b  laplace={1/(k2*sqrt(s/(2*pi)))}
l1 lx b {l}
c1 a1 cx {c}
r1 cx b {r1}
.ends lcomp

