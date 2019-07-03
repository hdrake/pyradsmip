#!/usr/bin/env python
# coding: utf-8

# # Create moist adiabatic atmosphere w/ isothermal stratosphere

# In[1]:


import numpy as np

# climlab
import climlab
from attrdict import AttrDict

# pyrads
import sys
sys.path.append("../")
import pyradsmip
from pyradsmip import pyrads
from scipy.integrate import trapz,simps,cumtrapz


# # PyRADS

# In[6]:


class Dummy:
    pass

params = Dummy()

params.Rv = pyrads.phys.H2O.R # moist component
params.cpv = pyrads.phys.H2O.cp
params.Lvap = pyrads.phys.H2O.L_vaporization_TriplePoint
params.satvap_T0 = pyrads.phys.H2O.TriplePointT
params.satvap_e0 = pyrads.phys.H2O.TriplePointP
params.esat = lambda T: pyrads.Thermodynamics.get_satvps(T,params.satvap_T0,params.satvap_e0,params.Rv,params.Lvap)

params.R = pyrads.phys.air.R  # dry component
params.cp = pyrads.phys.air.cp
params.ps_dry = 1e5           # surface pressure of dry component

params.R_CO2 = pyrads.phys.CO2.R

params.g = 9.8             # surface gravity
params.cosThetaBar = 3./5. # average zenith angle used in 2stream eqns
params.RH = 0.5             # relative humidity

nlev = 60
Tstrat = 160.      # stratospheric temperature

## PyRADS setup
dwavenr = 0.01
wavenr_min = 0.1   # [cm^-1]
wavenr_max = 3500. #


# In[65]:


CO2_vec = np.array([75.,150.,300.,300.*2,300.*4,300.*8,300.*16])
Ts_vec = np.arange(275.,330.,2.5)
CO2_grid, Ts_grid = np.meshgrid(CO2_vec,Ts_vec)

OLR_PyRADS = np.zeros_like(CO2_grid)
OLR_RRTMG = np.zeros_like(CO2_grid)

j=0
for Ts in Ts_vec:
    i=0
    for CO2 in CO2_vec:
        ## PyRADS
        # recreate grid with proper surface temp
        g = pyrads.SetupGrids.make_grid(Ts, Tstrat, nlev, wavenr_min, wavenr_max, dwavenr, params, RH=params.RH)
        # compute optical thickness:
        g.tau = pyrads.OpticalThickness.compute_tau_H2ON2_CO2dilute(g.p, g.T, g.q, CO2*1.e-6, g, params, RH=params.RH )
        # compute Planck functions etc:
        T_2D = np.transpose(np.tile( g.T, (g.Nn,1) )) # shape=(g.p,g.n)
        g.B_surf = np.pi* pyrads.Planck.Planck_n( g.n, Ts ) # shape=(g.n)
        g.B = np.pi* pyrads.Planck.Planck_n( g.wave, T_2D ) # shape=(g.p,g.n)
        # compute OLR etc:
        olr_spec = pyrads.Get_Fluxes.Fplus_alternative(0,g) # (spectrally resolved=irradiance)
        olr = simps(olr_spec,g.n)
        OLR_PyRADS[j,i] = olr
        print(round(olr,2),end=", ")
        
        ## RRTMG
        #  Couple water vapor to radiation
        ## climlab setup
        # create surface and atmosperic domains
        sfc, atm = climlab.domain.single_column(lev=g.p/100.)

        # create atmosheric state
        state = AttrDict()

        # assign surface temperature and vertical temperature profiles
        Ts_ = climlab.Field(np.array([Ts]), domain=sfc)
        state['Ts'] = Ts_

        Tatm = climlab.Field(g.T, domain=atm)
        state['Tatm'] = Tatm

        #  Parent model process
        rcm = climlab.TimeDependentProcess(state=state)
        rad = climlab.radiation.RRTMG(state=state, specific_humidity=g.q, albedo=0.3, ozone_file=None)
        rad.subprocess['LW'].absorber_vmr = {'CO2':CO2*1.e-6,
                                             'CH4':0.,
                                             'N2O':0.,
                                             'O2':0.,
                                             'CFC11':0.,
                                             'CFC12':0.,
                                             'CFC22':0.,
                                             'CCL4':0.,
                                             'O3':0.
                                            }
        # add radiation process and compute diagnostics
        rcm.add_subprocess('Radiation', rad)
        rcm.compute();
        olr = rcm.OLR[0]
        OLR_RRTMG[j,i] = olr
        print(olr,end="\n")
        
        i+=1
    j+=1
    
np.savez("../data/processed/OLR.npz",
         OLR_RRTMG=OLR_RRTMG,
         OLR_PyRADS=OLR_PyRADS,
         Ts_vec=Ts_vec,
         CO2_vec=CO2_vec
        )

