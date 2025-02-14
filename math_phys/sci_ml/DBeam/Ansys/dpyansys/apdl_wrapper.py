from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

log = []

ALL = all = 'ALL'
FULL = full = 'FULL'
LIVE = live = 'LIVE'
S = s = 's'


def finish():
    mapdl.finish()
    log.append('finish')


def solu():
    mapdl.solu()
    log.append('/solu')


def post1():
    mapdl.post1()
    log.append('/post1')


def post26():
    mapdl.post26()
    log.append('/post26')


def prep7():
    mapdl.prep7()
    log.append('/prep7')


def title(param):
    mapdl.title(param)
    log.append(f'/title, {param}')


def et(*params):
    mapdl.et(*params)
    log.append(f'et, ' + ', '.join([str(param) for param in params]))


def blc4(*params):
    rect = mapdl.blc4(*params)
    log.append(f'blc4, ' + ', '.join([str(param) for param in params]))
    return rect


def cyl4(*params):
    mapdl.cyl4(*params)
    log.append(f'cyl4, ' + ', '.join([str(param) for param in params]))


def vext(*params, **params_dict):
    mapdl.vext(*params, **params_dict)
    log.append(f'vext, ' + ', '.join([str(param) for param in params]))


def asba(*params):
    mapdl.asba(*params)
    log.append(f'asba, ' + ', '.join([str(param) for param in params]))


def vsweep(*params):
    mapdl.vsweep(*params)
    log.append(f'vsweep, ' + ', '.join([str(param) for param in params]))


def esize(*params):
    mapdl.esize(*params)
    log.append(f'esize, ' + ', '.join([str(param) for param in params]))


def nropt(*params):
    mapdl.nropt(*params)
    log.append(f'nropt, ' + ', '.join([str(param) for param in params]))


def ekill(*params):
    mapdl.ekill(*params)
    log.append(f'ekill, ' + ', '.join([str(param) for param in params]))


def esel(*params):
    mapdl.esel(*params)
    log.append(f'esel, ' + ', '.join([str(param) for param in params]))


def eplot(*params):
    mapdl.eplot(*params)
    log.append(f'eplot, ' + ', '.join([str(param) for param in params]))


def save_log(filename):
    with open(filename, 'wt', encoding='utf-8') as f:
        for line in log:
            f.write(line + '\n')



