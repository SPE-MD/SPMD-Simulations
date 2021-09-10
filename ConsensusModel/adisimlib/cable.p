*lumped transmission line model with 20 segments per meter at 51 meters
*and a 51.000000 meter long cable
.include tlump2.p
.include node.p
**********************
* name    trunk1
* length  2.6842105263157894
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk1 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk1
**********************
* name    trunk2
* length  2.6842105263157894
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk2 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk2
**********************
* name    trunk3
* length  2.6842105263157894
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk3 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk3
**********************
* name    trunk4
* length  2.6842105263157894
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk4 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk4
**********************
* name    trunk5
* length  2.6842105263157894
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk5 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk5
**********************
* name    trunk6
* length  2.6842105263157894
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk6 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk6
**********************
* name    trunk7
* length  2.684210526315791
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk7 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk7
**********************
* name    trunk8
* length  2.6842105263157876
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk8 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk8
**********************
* name    trunk9
* length  2.6842105263157876
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk9 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk9
**********************
* name    trunk10
* length  2.684210526315791
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk10 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk10
**********************
* name    trunk11
* length  2.684210526315791
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk11 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk11
**********************
* name    trunk12
* length  2.6842105263157876
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk12 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk12
**********************
* name    trunk13
* length  2.6842105263157876
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk13 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk13
**********************
* name    trunk14
* length  2.6842105263157947
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk14 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk14
**********************
* name    trunk15
* length  2.6842105263157876
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk15 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk15
**********************
* name    trunk16
* length  2.6842105263157876
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk16 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk16
**********************
* name    trunk17
* length  2.6842105263157876
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk17 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk17
**********************
* name    trunk18
* length  2.6842105263157876
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk18 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk18
**********************
* name    trunk19
* length  2.6842105263157947
* gage    18
* seg_max 0.05
* nsegs   53.684211
* whole   53.000000
* part    0.684211
**********************
.subckt trunk19 0000p 0000n endp endn rtn
rendp endp 0054p 1u
rendn 0054n endn 1u
xseg0000 0000p 0000n 0001p 0001n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0001 0001p 0001n 0002p 0002n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0002 0002p 0002n 0003p 0003n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0003 0003p 0003n 0004p 0004n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0004 0004p 0004n 0005p 0005n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0005 0005p 0005n 0006p 0006n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0006 0006p 0006n 0007p 0007n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0007 0007p 0007n 0008p 0008n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0008 0008p 0008n 0009p 0009n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0009 0009p 0009n 0010p 0010n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0010 0010p 0010n 0011p 0011n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0011 0011p 0011n 0012p 0012n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0012 0012p 0012n 0013p 0013n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0013 0013p 0013n 0014p 0014n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0014 0014p 0014n 0015p 0015n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0015 0015p 0015n 0016p 0016n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0016 0016p 0016n 0017p 0017n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0017 0017p 0017n 0018p 0018n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0018 0018p 0018n 0019p 0019n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0019 0019p 0019n 0020p 0020n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0020 0020p 0020n 0021p 0021n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0021 0021p 0021n 0022p 0022n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0022 0022p 0022n 0023p 0023n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0023 0023p 0023n 0024p 0024n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0024 0024p 0024n 0025p 0025n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0025 0025p 0025n 0026p 0026n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0026 0026p 0026n 0027p 0027n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0027 0027p 0027n 0028p 0028n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0028 0028p 0028n 0029p 0029n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0029 0029p 0029n 0030p 0030n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0030 0030p 0030n 0031p 0031n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0031 0031p 0031n 0032p 0032n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0032 0032p 0032n 0033p 0033n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0033 0033p 0033n 0034p 0034n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0034 0034p 0034n 0035p 0035n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0035 0035p 0035n 0036p 0036n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0036 0036p 0036n 0037p 0037n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0037 0037p 0037n 0038p 0038n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0038 0038p 0038n 0039p 0039n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0039 0039p 0039n 0040p 0040n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0040 0040p 0040n 0041p 0041n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0041 0041p 0041n 0042p 0042n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0042 0042p 0042n 0043p 0043n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0043 0043p 0043n 0044p 0044n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0044 0044p 0044n 0045p 0045n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0045 0045p 0045n 0046p 0046n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0046 0046p 0046n 0047p 0047n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0047 0047p 0047n 0048p 0048n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0048 0048p 0048n 0049p 0049n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0049 0049p 0049n 0050p 0050n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0050 0050p 0050n 0051p 0051n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0051 0051p 0051n 0052p 0052n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0052 0052p 0052n 0053p 0053n rtn tlump params: lseg={2.06435e-08} rskin={1.13427e-05} cseg={2.25026e-12} rser={0.0094}
xseg0053 0053p 0053n 0054p 0054n rtn tlump params: lseg={1.41245e-08} rskin={7.76078e-06} cseg={1.53965e-12} rser={0.00643158}
.ends trunk19
**********************
* number      1
* name        node1
* port        t1
* drop_name   drop1
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop1
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop1 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop1
**********************
* number      2
* name        node2
* port        t2
* drop_name   drop2
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop2
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop2 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop2
**********************
* number      3
* name        node3
* port        t3
* drop_name   drop3
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop3
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop3 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop3
**********************
* number      4
* name        node4
* port        t4
* drop_name   drop4
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop4
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop4 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop4
**********************
* number      5
* name        node5
* port        t5
* drop_name   drop5
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop5
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop5 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop5
**********************
* number      6
* name        node6
* port        t6
* drop_name   drop6
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop6
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop6 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop6
**********************
* number      7
* name        node7
* port        t7
* drop_name   drop7
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop7
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop7 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop7
**********************
* number      8
* name        node8
* port        t8
* drop_name   drop8
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop8
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop8 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop8
**********************
* number      9
* name        node9
* port        t9
* drop_name   drop9
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop9
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop9 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop9
**********************
* number      10
* name        node10
* port        t10
* drop_name   drop10
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop10
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop10 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop10
**********************
* number      11
* name        node11
* port        t11
* drop_name   drop11
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop11
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop11 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop11
**********************
* number      12
* name        node12
* port        t12
* drop_name   drop12
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop12
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop12 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop12
**********************
* number      13
* name        node13
* port        t13
* drop_name   drop13
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop13
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop13 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop13
**********************
* number      14
* name        node14
* port        t14
* drop_name   drop14
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop14
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop14 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop14
**********************
* number      15
* name        node15
* port        t15
* drop_name   drop15
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop15
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop15 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop15
**********************
* number      16
* name        node16
* port        t16
* drop_name   drop16
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop16
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop16 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop16
**********************
* number      17
* name        node17
* port        t17
* drop_name   drop17
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop17
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop17 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop17
**********************
* number      18
* name        node18
* port        t18
* drop_name   drop18
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop18
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop18 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop18
**********************
* number      19
* name        node19
* port        t19
* drop_name   drop19
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop19
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop19 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop19
**********************
* number      20
* name        node20
* port        t20
* drop_name   drop20
* drop_length 0.000000
* drop_gage   18
* spice_model node
**********************
**********************
* name    drop20
* length  0.0
* gage    18
* seg_max 0.05
* nsegs   0.000000
* whole   0.000000
* part    0.000000
**********************
.subckt drop20 0000p 0000n endp endn rtn
rendp endp 0000p 1u
rendn 0000n endn 1u
.ends drop20
**********************
* name    start_term
* rterm   100
* ccouple 2.2e-07
**********************
.subckt start_term p n sp sn rtn
ccp p sp 2.2e-07
ccn sn n 2.2e-07
rp sp rtn 50
rn rtn sn 50
.ends start_term
**********************
* name    end_term
* rterm   100
* ccouple 2.2e-07
**********************
.subckt end_term p n sp sn rtn
ccp p sp 2.2e-07
ccn sn n 2.2e-07
rp sp rtn 50
rn rtn sn 50
.ends end_term
** MAIN NETWORK DESCRIPTION **
xtrunk1 t1p t1n t2p t2n rtn trunk1
xtrunk2 t2p t2n t3p t3n rtn trunk2
xtrunk3 t3p t3n t4p t4n rtn trunk3
xtrunk4 t4p t4n t5p t5n rtn trunk4
xtrunk5 t5p t5n t6p t6n rtn trunk5
xtrunk6 t6p t6n t7p t7n rtn trunk6
xtrunk7 t7p t7n t8p t8n rtn trunk7
xtrunk8 t8p t8n t9p t9n rtn trunk8
xtrunk9 t9p t9n t10p t10n rtn trunk9
xtrunk10 t10p t10n t11p t11n rtn trunk10
xtrunk11 t11p t11n t12p t12n rtn trunk11
xtrunk12 t12p t12n t13p t13n rtn trunk12
xtrunk13 t13p t13n t14p t14n rtn trunk13
xtrunk14 t14p t14n t15p t15n rtn trunk14
xtrunk15 t15p t15n t16p t16n rtn trunk15
xtrunk16 t16p t16n t17p t17n rtn trunk16
xtrunk17 t17p t17n t18p t18n rtn trunk17
xtrunk18 t18p t18n t19p t19n rtn trunk18
xtrunk19 t19p t19n t20p t20n rtn trunk19
xdrop1 t1p t1n node_1_mdi_p node_1_mdi_n rtn drop1
xnode1 node_1_mdi_p node_1_mdi_n phy_1_p phy_1_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop2 t2p t2n node_2_mdi_p node_2_mdi_n rtn drop2
xnode2 node_2_mdi_p node_2_mdi_n phy_2_p phy_2_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop3 t3p t3n node_3_mdi_p node_3_mdi_n rtn drop3
xnode3 node_3_mdi_p node_3_mdi_n phy_3_p phy_3_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop4 t4p t4n node_4_mdi_p node_4_mdi_n rtn drop4
xnode4 node_4_mdi_p node_4_mdi_n phy_4_p phy_4_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop5 t5p t5n node_5_mdi_p node_5_mdi_n rtn drop5
xnode5 node_5_mdi_p node_5_mdi_n phy_5_p phy_5_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop6 t6p t6n node_6_mdi_p node_6_mdi_n rtn drop6
xnode6 node_6_mdi_p node_6_mdi_n phy_6_p phy_6_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop7 t7p t7n node_7_mdi_p node_7_mdi_n rtn drop7
xnode7 node_7_mdi_p node_7_mdi_n phy_7_p phy_7_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop8 t8p t8n node_8_mdi_p node_8_mdi_n rtn drop8
xnode8 node_8_mdi_p node_8_mdi_n phy_8_p phy_8_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop9 t9p t9n node_9_mdi_p node_9_mdi_n rtn drop9
xnode9 node_9_mdi_p node_9_mdi_n phy_9_p phy_9_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop10 t10p t10n node_10_mdi_p node_10_mdi_n rtn drop10
xnode10 node_10_mdi_p node_10_mdi_n phy_10_p phy_10_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop11 t11p t11n node_11_mdi_p node_11_mdi_n rtn drop11
xnode11 node_11_mdi_p node_11_mdi_n phy_11_p phy_11_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop12 t12p t12n node_12_mdi_p node_12_mdi_n rtn drop12
xnode12 node_12_mdi_p node_12_mdi_n phy_12_p phy_12_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop13 t13p t13n node_13_mdi_p node_13_mdi_n rtn drop13
xnode13 node_13_mdi_p node_13_mdi_n phy_13_p phy_13_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop14 t14p t14n node_14_mdi_p node_14_mdi_n rtn drop14
xnode14 node_14_mdi_p node_14_mdi_n phy_14_p phy_14_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop15 t15p t15n node_15_mdi_p node_15_mdi_n rtn drop15
xnode15 node_15_mdi_p node_15_mdi_n phy_15_p phy_15_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop16 t16p t16n node_16_mdi_p node_16_mdi_n rtn drop16
xnode16 node_16_mdi_p node_16_mdi_n phy_16_p phy_16_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop17 t17p t17n node_17_mdi_p node_17_mdi_n rtn drop17
xnode17 node_17_mdi_p node_17_mdi_n phy_17_p phy_17_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop18 t18p t18n node_18_mdi_p node_18_mdi_n rtn drop18
xnode18 node_18_mdi_p node_18_mdi_n phy_18_p phy_18_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop19 t19p t19n node_19_mdi_p node_19_mdi_n rtn drop19
xnode19 node_19_mdi_p node_19_mdi_n phy_19_p phy_19_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xdrop20 t20p t20n node_20_mdi_p node_20_mdi_n rtn drop20
xnode20 node_20_mdi_p node_20_mdi_n phy_20_p phy_20_n rtn node params: cnode=1.5e-11 lpodl=8e-05 rnode=10000
xstart_term t1p t1n startp startn rtn start_term
xend_term t20p t20n endp endn rtn end_term
