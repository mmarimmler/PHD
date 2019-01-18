import numpy as np
from matplotlib import pyplot as plt
from helpers import cusplot as cplt
from helpers import numerics as num
from functools import partial



def s_kick_sept(x_sept,x_add,x_init,kick,perm,init,l_kick,l_sept,sept_type='DC'):
    '''function that calculates the propagation distance in a kicker + septum beam line.
    Calculated lengths correspond to the deflected arms.'''
    # offset: inital + orbit in kicker
    x_init = x_init + l_kick*kick/2
    
    # dist. from kicker end to sept. begin.
    s1 = (x_sept-x_init)/np.sin(kick+init)
    
    # dist. from septum end to x_add separation
    o_sept = l_sept*perm/2 # orbit offset in septum
    d_k_sept = l_sept*kick # drift in septum from kick angle 
    
    s2 = (x_add-o_sept-d_k_sept)/np.sin(kick+perm+init)
    
    if sept_type == 'OFS':
        # dist from septum end to x_add separaion (Opposite Field Septum)
        s2 = (x_add-2*o_sept-d_k_sept)/np.sin(kick+2*perm+init)
        # 2*o_sept AND 2*perm because beam manipulation in two field regions
     
    s = s1+s2+l_sept
    
    return s,s1,s2


def quad_defl(k,l,kick,l_kick,l1,l2):
    
    sep = kick*l1+l_kick*kick/2
    Thet = k*l*sep+kick
    
    sep2 = Thet*l2+l*Thet/2+sep
    
    return sep2


def plot_comb_kick_sept(x_sept,x_add,x_init,init,l_kick,l_sept,sept_type,start_kick,step_kick,list_perm,max_prop,**kwargs):

    s_kick_sept_fix = lambda perm,kick: s_kick_sept(x_sept,x_add,x_init,kick,perm,init,l_kick,l_sept,sept_type)
    d = num.iterate(s_kick_sept_fix,list_perm,start_kick,step_kick,max_prop)

    if 'figsize' in kwargs.keys():
        _,ax = plt.subplots(1,2,figsize=kwargs['figsize'])
    else:
        _,ax = plt.subplots(1,2)

    ax[0].plot(*zip(*sorted(d.items())))
    ax[0].set_ylabel('kick_angle [rad]')
    ax[0].set_xlabel('perm_angle [rad]')

    last_ele = list(d.values())[-1]
    ax[0].text(0.5,0.02, r'$\Theta_k = {}$ rad'.format(last_ele))

    # add B-field information
    if 'brho' in kwargs.keys():
        calc_magn_sept = partial(calc_magn, l=l_sept, brho=kwargs['brho'])
        calc_magn_kick = partial(calc_magn, l=l_kick, brho=kwargs['brho'])

        cplt.add_axis(ax[0],'x',calc_magn_sept,'B [T]')
        cplt.add_axis(ax[0],'y',calc_magn_kick,'B [T]')

    fst_arm = [(kick,s_kick_sept_fix(perm,kick)[1]) for perm,kick in zip(list(d.keys()),list(d.values()))]
    snd_arm = [(kick,s_kick_sept_fix(perm,kick)[2]) for perm,kick in zip(list(d.keys()),list(d.values()))]    

    ax[1].scatter(*zip(*fst_arm))
    ax[1].scatter(*zip(*snd_arm))
    ax[1].set_ylabel('length [m]')
    ax[1].set_xlabel('kick_angle [rad]')
    ax[1].legend(['kick-sept','sept-max_prop'])

    data = (d,fst_arm,snd_arm)

    return ax,data



def calc_magn(ang,l,brho):
    '''function that calculates magnetic field'''    
    B = ang*brho/l
    
    return round(B,3)