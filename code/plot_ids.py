import os.path as op

import numpy as num

from pyrocko.plot import gmtpy

from ewrica.sources import load_sources
from ewrica.plot.ids import RuptureMap

results_path = '../../../demonstrator/Norcia_2016'
report_path = 'ids/Norcia_20161030_064018_ids_regular_nodalplane{}/results/idssource.yaml'

sources100 = [load_sources(
    filename=op.join(results_path, report_path.format(i + 1))) for i in range(2)]

sources200 = [
    load_sources(
        filename=op.join(results_path, '200km', report_path.format(i + 1)))
    for i in range(2)]

sources300 = [
    load_sources(
        filename=op.join(results_path, '300km', report_path.format(i + 1)))
    for i in range(2)]

sources100 = [src for lst in sources100 for src in lst]
sources200 = [src for lst in sources200 for src in lst]
sources300 = [src for lst in sources300 for src in lst]


def extract_source(sources):
    misfits = num.array([src.misfit_log.misfit_all[-1] for src in sources])
    idx = num.argmin(misfits)

    print(idx)

    return sources[idx]


sources = dict(
    km100=extract_source(sources100),
    km200=extract_source(sources200),
    km300=extract_source(sources300))

# sources = dict(
#     km100=source100,
#     km200=source200)

for label, source in sources.items():
    print(label, source.magnitude)
    m = RuptureMap(
        lat=42.8,
        lon=13.3,
        height=15,
        width=15.,
        radius=50e3,
        show_cities=False,
        source=source)

    m.draw_dislocation(clim=(0., 1.))
    m.draw_top_edge(W='3p,{}'.format(gmtpy.color('skyblue1')))
    m.draw_nucleation_point()
    # m.draw_time_contour()

    m.save('../figures/results/ids_{}.png'.format(label))
