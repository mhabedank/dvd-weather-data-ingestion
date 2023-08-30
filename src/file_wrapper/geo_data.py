import os
import json
from enum import StrEnum
from shapely.geometry import shape, Point
import numpy as np


class FederalStates(StrEnum):
    BADEN_WUERTTEMBERH = "Baden-Württemberg"
    BAYERN = "Bayern"
    BERLIN = "Berlin"
    BRANDENBURG = "Brandenburg"
    BREMEN = "Bremen"
    HAMBURG = "Hamburg"
    HESSEN = "Hessen"
    MECKLENBURG_VORPOMMERN = "Mecklenburg-Vorpommern"
    NIEDERSACHSEN = "Niedersachsen"
    NORDRHEIN_WESTFALEN = "Nordrhein-Westfalen"
    RHEINLAND_PFALZ = "Rheinland-Pfalz"
    SAARLAND = "Saarland"
    SACHSEN_ANHALT = "Sachsen-Anhalt"
    SACHSEN = "Sachsen"
    SCHLESWIG_HOLSTEIN = "Schleswig-Holstein"
    THUERINGEN = "Thüringen"


class AdministrativeBoundaries:
    def __init__(self, path: os.PathLike):
        with open(path) as f:
            self.data = json.load(f)

        self.get_state_by_point = np.vectorize(self._get_state_by_point)

    def _get_state_by_point(self, lon, lat):
        point = Point(lon, lat)
        for feature in self.data["features"]:
            pol_type = shape(feature["geometry"])
            if pol_type.contains(point):
                return feature["properties"]["name"]
        return None
