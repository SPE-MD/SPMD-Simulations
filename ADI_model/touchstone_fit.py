#Copyright 2022 Rosenberger Hochfreqenztechnik GmbH & Co. KG
#Author: Franz Forstmayr
# 
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from typing import List

from abc import ABC, abstractproperty
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

import skrf as rf

vectorfit_cache = {}


class TouchstoneFit(ABC):
    n_ports = 0

    def __init__(
        self,
        touchstone_file: str,
        fittedModelName: str,
        fitting_error: float,
        instance_name: str = "",
        port_order: List[int] = None,
        max_poles: int = 30,
    ):

        self.instance_name = instance_name
        self.port_order = port_order if port_order else list(range(self.n_ports))

        netw = rf.Network(touchstone_file)
        assert (
            netw.nports == self.n_ports
        ), f"{self.__class__.__name__} needs exactly {self.n_ports} ports, got: {netw.nports}"
        assert (
            len(self.port_order) == self.n_ports
        ), f"port_order has to be of length {self.n_ports} or None"

        key = (touchstone_file, fittedModelName, fitting_error)

        if instance_name:
            self.instance_name = instance_name
        else:
            self.instance_name = f"fitted_{str(hash(key))}"

        cached = False
        if key not in vectorfit_cache.keys():
            vf = rf.VectorFitting(netw)

            poles = 4
            while True:
                print(f"Fit with {poles} poles")
                if poles > max_poles:
                    raise RuntimeError("Unable to fit network ")
                vf.vector_fit(n_poles_real=1, n_poles_cmplx=poles)
                error = vf.get_rms_error()
                if error < fitting_error:
                    print(f"Fitting Error RMS", error)
                    break
                poles += 1

            vectorfit_cache[key] = vf
        else:
            cached = True
            vf = vectorfit_cache[key]

        self.spice_file = Path("tmp_vectorfit") / f"fitted_{instance_name}_{fittedModelName}_{str(hash(key))}.sp"
        self.spice_file.parent.mkdir(exist_ok=True)

        vf.write_spice_subcircuit_s(self.spice_file, self.instance_name)
        self.inner_circuit = open(self.spice_file).read()

        if cached:
            os.remove(self.spice_file)
        else:
            self.create_plots(netw, vf)

    def plot_both_traces(self, orig: rf.Network, fitted: rf.Network, tpl, ax):
        fitted.plot_s_db(tpl[0], tpl[1], ax=ax)
        orig.plot_s_db(tpl[0], tpl[1], ax=ax, linestyle='dashed')


    def create_plots(self, original: rf.Network, fitted: rf.VectorFitting):
        
        fitted_s = np.zeros((len(original), 6,6), dtype=complex)

        for i in range(6):
            for j in range(6):
                fitted_s[:,i,j] = fitted.get_model_response(i,j, freqs=original.f)

        fitted_netw = rf.Network(frequency=original.frequency, s=fitted_s, name="fitted")

        with plt.style.context(os.path.join(rf.data.pwd, "skrf.mplstyle")):
            fig, axes = plt.subplots(2, 2)
            fig.set_size_inches(12, 8)
            
            axes[0,0].set_title("Return Loss Trunk")
            axes[0,1].set_title("Return Loss Node")
            for i in range(6):
                current_ax = axes[0,0] if i < 4 else axes[0, 1]
                self.plot_both_traces(original, fitted_netw, (i, i), current_ax)

            axes[1,0].set_title("Insertion Loss Trunk - Node")
            for t0, t1 in [(1,5), (2,6), (3,5), (4,6)]:
                self.plot_both_traces(original, fitted_netw, (t0-1, t1-1), axes[1,0])

            axes[1,1].set_title("Insertion Loss Trunk - Trunk")
            for t0, t1 in [(3,1), (4,2)]:
                self.plot_both_traces(original, fitted_netw, (t0-1, t1-1), axes[1,1])

            fig.tight_layout()
            file = self.spice_file.with_suffix('.png')
            fig.savefig(file)



    @abstractproperty
    def port_names(self) -> List[str]:
        pass

    def __str__(self) -> str:
        s = [
            "**********************",
            "* Fitted Touchstone",
            "* name        %s" % self.instance_name,
            "**********************",
        ]
        return "\n".join(s)

    def subcircuit(self) -> str:
        return self.inner_circuit

    def instance(self) -> str:
        port_tpl = list(zip(self.port_order, self.port_names))

        port_tpl.sort()
        ports = [e[1] for e in port_tpl]

        """Generate the instance call for this cable segment"""
        return "x%s %sp %sn %sp %sn %sp %sn %s" % (
            self.instance_name,
            *ports,
            self.instance_name,
        )
