#Copyright 2022 Rosenberger Hochfreqenztechnik GmbH & Co. KG
#Author: Franz Forstmayr
# 
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from typing import List

from abc import ABC, abstractproperty
import os

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

        spice_file = f"fitted_{instance_name}_{fittedModelName}_{str(hash(key))}.sp"
        vf.write_spice_subcircuit_s(spice_file, self.instance_name)
        self.inner_circuit = open(spice_file).read()

        if cached:
            os.remove(spice_file)

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
