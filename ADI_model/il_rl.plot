file="zcable.nopodl.30p.csv"
file="zcable.nopodl.15p.csv"
file="zcable.30p.csv"
#file="zcable.15p.csv"
file="zcable.csv"
set datafile separator ","
set multiplot layout 2,1
#set xrange [0:40e6]
set xrange [0:40e6]
set format x "%.0s%c"
set title "Return Loss (S11)"
set yrange [-50:0]
rl_1(x) = 14
rl_2(x) = 14 - 10 * log10(x / 10e6)
rl(x) = x < 0.3e6 ? NaN : x < 10e6 ? rl_1(x) : x < 40e6 ? rl_2(x) : NaN
plot file u 1:4 w l notitle, -1*rl(x) t "RL Limit"

set title "Insertion Loss (S21)"
set yrange [-10:0]
il_1(x) = 1.0 + (1.6 * (x -  1e6)  / 9e6)
il_2(x) = 2.6 + (2.3 * (x - 10e6) / 23e6)
il_3(x) = 4.9 + (2.3 * (x - 33e6) / 33e6)
il(x) = x < 0.3e6 ? NaN : x < 10e6 ? il_1(x) : x < 33e6 ? il_2(x) : x < 40e6 ? il_3(x) : NaN
plot file u 1:5 w l notitle, -1.1*il(x) t "1.1 * IL Limit"
unset multiplot
