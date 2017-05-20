r"""
Find :math:`u` such that:

.. math::
    \int_{\Omega} s \pdiff{u}{t}
    + \int_{\Omega} D \nabla s \cdot \nabla u
    =   \int_{\Gamma s\nabla u}
    \;, \quad \forall s \;.

View the results using::

  python postproc.py square_tri2.*.vtk -b --wireframe
"""
from __future__ import absolute_import
from sfepy import data_dir

filename_mesh = data_dir + '/meshes/2d/square_tri2.mesh'

regions = {
    'Omega' : 'all', # or 'cells of group 6'
    'Gamma_Left' : ('vertices in (x < -0.99999)', 'facet'),
    'Gamma_Right' : ('vertices in (x > 0.99999)', 'facet'),
    'Gamma_Bottom' : ('vertices in (y < -0.99999)', 'facet'),
    'Gamma_Top' : ('vertices in (y > 0.99999)', 'facet'),
}

fields = {
    'concentration' : ('real', 1, 'Omega', 1),
}

variables = {
    'u' : ('unknown field', 'concentration', 0, 100),
    's' : ('test field',    'concentration', 'u'),
}


ebcs = {
    'u1' : ('Gamma_Top', {'u.all' : 10.0}),
    'u2' : ('Gamma_Bottom', {'u.all' : 0.0}),
}

# Units: D: 0.0001 m^2 / day, v: [0.1, 0] m / day -> time in days.
materials = {
    'm' : ({'D' : 1, }, ),
    'flux' : ({'left' : -5, 'right': 5}, ),
}


ics = {
    'ic' : ('Omega', {'u.0' : 5.}),
}

integrals = {
    'i' : 2,
}

equations = {
    'advection-diffusion' :
     """
     dw_volume_dot.i.Omega( s, du/dt ) +
     dw_laplace.i.Omega(m.D, s, u) =
     dw_surface_integrate.i.Gamma_Right(flux.right, s) +
     dw_surface_integrate.i.Gamma_Left(flux.left, s)
     """
}

t0 = 0.
t1 = 0.3
n_step = 50

solver_0 = {
    'name' : 'ls',
    'kind' : 'ls.scipy_direct',
    'presolve' : True,
}

solver_1 = {
    'name' : 'newton',
    'kind' : 'nls.newton',

    'i_max'      : 1,
    'eps_a'      : 1e-10,
    'eps_r'      : 1.0,
    'macheps'   : 1e-16,
    'lin_red'    : 1e-2, # Linear system error < (eps_a * lin_red).
    'ls_red'     : 0.1,
    'ls_red_warp' : 0.001,
    'ls_on'      : 1.1,
    'ls_min'     : 1e-5,
    'check'     : 0,
    'delta'     : 1e-6,
    'is_linear' : True,
}

solver_2 = {
    'name' : 'ts',
    'kind' : 'ts.simple',

    't0'    : t0,
    't1'    : t1,
    'dt'    : None,
    'n_step' : n_step, # has precedence over dt!
}

options = {
    'nls' : 'newton',
    'ls' : 'ls',
    'ts' : 'ts',
    'save_steps' : -1,
}
