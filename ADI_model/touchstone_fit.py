from typing import List

from abc import ABC, abstractproperty
import os

import skrf as rf

vectorfit_cache = {}


class FittedTouchstone(ABC):
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
                vf.vector_fit(n_poles_real=0, n_poles_cmplx=poles)
                error = vf.get_rms_error()
                if error < fitting_error:
                    print(f"Fitting Error RMS", error)
                    break
                poles += 2

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
