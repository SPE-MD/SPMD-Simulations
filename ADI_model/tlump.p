*one segment for a lumped transmission line model

*Copyright 2021 <Analog Devices>
*Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
*The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


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
