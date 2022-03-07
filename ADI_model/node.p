*simple pd model for transmission line simulations
.subckt node p n phyp phyn 0 params: lpodl=80u cnode=15p rnode=10k
lpodl p n {lpodl}
cpodl p n {cnode}
ctxp  p phyp 220n
ctxn  phyn n 220n
rnodep phyp 0 {rnode/2}
rnoden 0 phyn {rnode/2}
.ends node
