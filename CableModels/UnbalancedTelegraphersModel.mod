.param Kft=0.328                                    ; 1 Kft = 1000 feet
.param Lcon=10n                                 ; convergence inductance
+ C=15.72e-9                                    ; the value of capacitance at dc
+ Gdc=0.5n                                      ; the value of conductance at dc
+ Rdc=52.50                                     ; the value of resistance at dc
+ Ldc=0.1868e-3                                 ; the value of inductance at dc
+ Linf=0.133e-3                                 ; inductance at infinite frequency
+ Ldel=(Ldc-Linf)                               ; inductance parameter
+ Zinf=(Linf/C)**0.5                            ; characteristic impedance at infinite frequency
+ Yinf=1/Zinf                                   ; characteristic conductance at infinite frequency
+ F2=5e6                                        ; the highest frequency in Hz
+ W2=6.28318*F2                                 ; the highest frequency in rad/sec
+ G1=23u                                        ; the value of conductance at F1
+ G2=36u                                        ; the value of conductance at F2
+ Rac=304.62                                    ; the value of resistance at F2
+ F1=3e6                                        ; the second highest frequency in Hz
+ A=1.6                                         ; inductance parameter
+ k=Log(G2/G1)/Log(F2/F1)/2                     ; conductance parameter
+ WL=6.28318*161000                             ; inductance parameter
+ WR=W2*(Rdc**2)/(((Rac**4)-(Rdc**4))**0.5)     ; resistance parameter
.subckt single_mode_xline L1 R1
G1 N1 0 N1 0 Laplace=(((((Gdc+G2*(-(s/w2)^2)^k)+s*C)/((Rdc*(1-(s/wR)^2)^0.25)+s*(Linf+Ldel/(1+A*((-(s/wL)^2)^0.5)-(s/wL)^2)^0.25)))^0.5))-Yinf
G2 0 N1 N2 0 1
G3 0 L1 N2 0 1
V1 L1 N1 0 Rser=0
H1 N4 0 V1 1
G4 N6 0 N6 0 Laplace=(((((Gdc+G2*(-(s/w2)^2)^k)+s*C)/((Rdc*(1-(s/wR)^2)^0.25)+s*(Linf+Ldel/(1+A*((-(s/wL)^2)^0.5)-(s/wL)^2)^0.25)))^0.5))-Yinf
G5 0 N6 N5 0 1
G6 0 R1 N5 0 1
V2 R1 N6 0 Rser=0
H2 N3 0 V2 1
R1 N6 0 {Zinf}
R2 N1 0 {Zinf}
G7 0 N2 N3 0 Laplace= Exp(-Kft*( (((Rdc*(1-(s/wR)^2)^.25)+s*(Linf+Ldel/(1+A*((-(s/wL)^2)^.5)-(s/wL)^2)^.25))*(Gdc+G2*(-(s/w2)^2)^k+s*C))^.5))/(s*Lcon+1)
L1 N5 0 {Lcon} Rser=1
G8 0 N5 N4 0 Laplace= Exp(-Kft*( (((Rdc*(1-(s/wR)^2)^.25)+s*(Linf+Ldel/(1+A*((-(s/wL)^2)^.5)-(s/wL)^2)^.25))*(Gdc+G2*(-(s/w2)^2)^k+s*C))^.5))/(s*Lcon+1)
L2 N2 0 {Lcon} Rser=1
.ends single_mode_xline
