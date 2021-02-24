from enum import Enum

from ..vlo.lut import LUT

ClassID = Enum("ClassID", {x:x for x in LUT["VLO"]["CLASS"]["IDR"].keys()})
