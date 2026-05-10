#!/usr/bin/env python3
# coding=utf-8
#
# Copyright (C) 2015 ~suv <suv-sf@users.sf.net>
# Copyright (C) 2010 Alvin Penner
# Copyright (C) 2006 Georg Wiora
# Copyright (C) 2006 Nathan Hurst
# Copyright (C) 2005 Aaron Spike, aaron@ekips.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
This extension module can measure arbitrary path and object length
It adds text to the selected path containing the length in a given unit.
Area and Center of Mass calculated using Green's Theorem:
http://mathworld.wolfram.com/GreensTheorem.html
"""

import inkex

#from gettext import gettext as _

from lib import dynalab,csvReader


from inkex.bezier import csparea, cspcofm
#from inkex.localization import inkex_gettext as _
from inkex.paths.interfaces import LengthSettings


class MeasureLength(dynalab.Ext):
    """Measure the length of selected paths"""

    def add_arguments(self, pars):
        # pars.add_argument(
        #     "--type", dest="mtype", default="length", help="Type of measurement"
        # )

        pars.add_argument(
            "--materials", dest="materials", type=int, default=1, help="Type of materials"
        )
        
        pars.add_argument(
            "--presetFormat", default="default", help="Preset text layout"
        )
        pars.add_argument(
            "--startOffset", default="custom", help="Text Offset along Path"
        )
        pars.add_argument(
            "--startOffsetCustom", type=int, default=50, help="Text Offset along Path"
        )
        pars.add_argument("--anchor", default="start", help="Text Anchor")
        pars.add_argument("--position", default="start", help="Text Position")
        pars.add_argument("--angle", type=float, default=0, help="Angle")
        pars.add_argument(
            "-f",
            "--fontsize",
            type=int,
            default=12,
            help="Size of length label text in px",
        )
        pars.add_argument(
            "-o",
            "--offset",
            type=float,
            default=-6,
            help="The distance above the curve",
        )
        pars.add_argument(
            "-u", "--unit", default="mm", help="The unit of the measurement"
        )
        pars.add_argument(
            "-p",
            "--precision",
            type=int,
            default=2,
            help="Number of significant digits after decimal point",
        )
        pars.add_argument(
            "-s",
            "--scale",
            type=float,
            default=1.0,
            help="Scale Factor (Drawing:Real Length)",
        )

    def effect(self):
        fill_mode_color = self.config["laser_mode_fill_color"]
        
        estimedTime = 0
        estimedTimeCut = 0
        tailleArea,tailleCut = 0,0
        # get number of digits
        prec = int(self.options.precision)
        scale = self.svg.viewport_to_unit(
            "1" + self.svg.document_unit
        )  # convert to document units
        self.options.offset *= scale
        factor = self.svg.unit_to_viewport(1, self.options.unit)

        paths = []

        for elem in self.svg.selection.values():

            elem_copy = elem.copy()

            if isinstance(elem, inkex.TextElement):
                text_copy = elem.copy()
                path = text_copy.to_path_element()
                paths.append(path)
        
            elif isinstance(elem_copy, inkex.PathElement):
                paths.append(elem_copy)

            else:
                paths.append(elem_copy.to_path_element())

        if not paths:
            raise inkex.AbortExtension(_("Please select at least one object."))
        
        for node in paths:            
            path: inkex.Path = node.path.transform(node.composed_transform())
            if node.style.get("stroke")!=fill_mode_color: #Element de type decoupe
                settings = LengthSettings(error=1e-8)
                stotal = sum(
                    command.length(settings=settings)
                    for command in path.proxy_iterator()
                    if command.letter not in "mM"
                )
                val = round(stotal * factor * self.options.scale, prec)
                tailleCut += val
                #self.group = node.getparent().add(TextElement())
            elif node.style.get("stroke")==fill_mode_color: #Element de type gravure remplissage
                csp = path.to_superpath()
                stotal = abs(csparea(csp) * factor * self.options.scale)
                val = round(stotal * factor * self.options.scale, prec)
                tailleArea += val
            else:
                continue
        # if (self.options.unit == "cm") == True:
        #     tailleArea = tailleArea*100
        #     tailleCut = tailleCut*100
            
        values = csvReader.readAreaCSV(self.options.materials)
        estimedTime = tailleArea * values
        values = csvReader.readLengthCSV(self.options.materials)
        estimedTimeCut = tailleCut * values

        #Calcul de l'intervalle
        interval = csvReader.formater_intervalle(estimedTime);
        intervalCut = csvReader.formater_intervalle(estimedTimeCut);

        self.message(
            _(
                """
                La forme va prendre environ {interval} à être gravé
                La forme va prendre environ {intervalCut} à être coupé
                """
            ).format(interval=interval,intervalCut=intervalCut)
        )
        # self.message(
        #     _(
        #         """
        #         {taille} {estimedTime} {estimedTimeH} {unitH}
        #         """
        #     ).format(taille=taille,estimedTime=estimedTime,estimedTimeH=estimedTimeH,unitH=unitH)
        # )
        
   
if __name__ == "__main__":
    MeasureLength().run()

