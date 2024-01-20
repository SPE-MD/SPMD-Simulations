*simple pd model for transmission line simulations
.subckt node p n phyp phyn 0 params: lpodl=80u cnode=15p rnode=10k ccouple=220n
lpodl p n {lpodl}
cnode p n {cnode}
ctxp  p phyp {ccouple}
ctxn  phyn n {ccouple}
rnodep phyp 0 {rnode/2}
rnoden 0 phyn {rnode/2}
.ends node
