*one segment for a lumped transmission line model

*Copyright 2021 <Analog Devices>
*Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
*The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


.subckt tlump t1p t1n t2p t2n rtn params: lseg=20.6435n cseg=2.25026p rskin=1.134268e-5 rser=9.4m rg=1e9
c1  t1p t1n {cseg/4}
l1p ap  t2p {lseg/2} rser={rser/2}
l2p an  t2n {lseg/2} rser={rser/2}
c2  t2p t2n {cseg/4}
cp1 t1p rtn {cseg/2}
cn1 t1n rtn {cseg/2}
cp2 t2p rtn {cseg/2}
cn2 t2n rtn {cseg/2}
g1p t1p ap t1p ap laplace={2/(rskin*((abs(s)/(2*pi))^0.5))}
g1n t1n an t1n an laplace={2/(rskin*((abs(s)/(2*pi))^0.5))}
r1 t1p t1n {4*rg}
r2 t2p t2n {4*rg}
r3 t1p rtn {2*rg}
r4 rtn t1n {2*rg}
r5 t2p rtn {2*rg}
r6 rtn t2n {2*rg}
*r2a t2p rtn 2e7
*r1b t1p rtn 2e7
.ends tlump
