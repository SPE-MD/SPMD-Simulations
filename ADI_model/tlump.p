*one segment for a lumped transmission line model
.subckt tlump t1p t1n t2p t2n rtn
c1 t1p t1n {clump/4}
l1p t1p t2p {llump/2} rser={rser}
l2p t1n t2n {llump/2} rser={rser}
c2 t2p t2n {clump/4}
cp1 t1p rtn {clump/2}
cn1 t1n rtn {clump/2}
cp2 t2p rtn {clump/2}
cn2 t2n rtn {clump/2}
r1 t1p t1n {rg/2}
r2 t2p t2n {rg/2}

*r2a t2p rtn 2e7
*r1b t1p rtn 2e7
.ends tlump
