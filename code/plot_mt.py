import os.path as op

from matplotlib import pyplot as plt

from pyrocko.model import load_one_event
from pyrocko import plot
from pyrocko.plot import beachball


results_path = '../../../demonstrator/Norcia_2016'
report_path = 'grond/report/Norcia_20161030_064018/Norcia_20161030_064018_fast_mt/event.solution.best.yaml'

gcmt = load_one_event('../../../data/events/Norcia_20161030_064018/event.txt')
ev100 = load_one_event(op.join(results_path, report_path))
ev200 = load_one_event(op.join(results_path, '200km', report_path))
ev300 = load_one_event(op.join(results_path, '300km', report_path))

events = dict(
    gcmt=gcmt,
    km100=ev100,
    km200=ev200,
    km300=ev300)

# events = dict(
#     km100=ev100,
#     km200=ev200)


for label, ev in events.items():
    fig = plt.figure(figsize=(2., 2.))
    fig.subplots_adjust(left=0., right=1., bottom=0., top=1.)
    axes = fig.add_subplot(1, 1, 1)
    axes.set_xlim(0., 2.)
    axes.set_ylim(0., 2.)
    axes.set_axis_off()

    beachball.plot_beachball_mpl(
        ev.moment_tensor,
        axes,
        beachball_type='dc',
        size=1.95,
        size_units='data',
        position=(1, 1),
        color_t=plot.mpl_color('scarletred2'),
        linewidth=1.0)

    plt.savefig('../figures/results/mt_{}.png'.format(label))

    plt.close()
