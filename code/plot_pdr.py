import os.path as op

from pyrocko.gf import PseudoDynamicRupture, get_engine
from pyrocko.plot import dynamic_rupture, gmtpy

from ewrica.io import grond as grondio

engine = get_engine()
store = engine.get_store('ak135_500km_1Hz')

results_path = '../../../demonstrator/Norcia_2016'
report_path = 'grond/runs_fastmodel_syn/Norcia_20161030_064018_fast_pdr.grun'


source100, _ = grondio.get_best_source_and_misfit(
    op.join(results_path, report_path))

source200, _ = grondio.get_best_source_and_misfit(
    op.join(results_path, '200km', report_path))

source300, _ = grondio.get_best_source_and_misfit(
    op.join(results_path, '300km', report_path))

sources = dict(
    km100=source100,
    km200=source200,
    km300=source300)

# sources = dict(
#     km100=source100,
#     km200=source200)


def draw_outline(m, **kwargs):
    '''
    Indicate rupture outline on map.
    '''

    outline = m.source.outline(cs='latlondepth')

    kwargs = kwargs or {}
    kwargs['W'] = kwargs.get(
        'W', '%gp,%s' % (m._fontsize / 10., gmtpy.color('aluminium5')))

    m.gmt.psxy(
        in_columns=[outline[:, 1], outline[:, 0]],
        *m.jxyr,
        **kwargs)

for label, source in sources.items():
    source.discretize_patches(store)

    m = dynamic_rupture.RuptureMap(
        lat=42.8,
        lon=13.3,
        height=15,
        width=15.,
        radius=50e3,
        show_cities=False,
        source=source)

    m.draw_dislocation(clim=(0., 2.))
    m.draw_top_edge(W='3p,{}'.format(gmtpy.color('skyblue1')))
    m.draw_nucleation_point()
    m.draw_time_contour(store)

    m.save('../figures/results/pdr_{}.png'.format(label))
