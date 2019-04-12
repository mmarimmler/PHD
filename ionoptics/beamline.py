import numpy as np
from matplotlib import pyplot as plt
import scipy.optimize as sco
from functools import partial


# ion optical elements

def qf(L,k,t=False):
    
    c = np.cos(np.sqrt(k)*L)
    s = np.sin(np.sqrt(k)*L)
    
    ch = np.cosh(np.sqrt(k)*L)
    sh = np.sinh(np.sqrt(k)*L)
    
    M11 = c
    M12 = s/np.sqrt(k)
    M21 = -np.sqrt(k)*s
    M22 = c
    
    M33 = ch
    M34 = sh/np.sqrt(k)
    M43 = np.sqrt(k)*sh
    M44 = ch
    
    if t:
        M11 = 1
        M12 = 0
        M21 = -k*L
        M22 = 1
        
        M33 = 1
        M34 = 0
        M43 = k*L
        M44 = 1
    
    
    
    M = np.array([[M11,M12,0,0],[M21,M22,0,0],[0,0,M33,M34],[0,0,M43,M44]])
    
    return M

def qdf(L,k,t=False):
    
    ch = np.cosh(np.sqrt(k)*L)
    sh = np.sinh(np.sqrt(k)*L)
    
    c = np.cos(np.sqrt(k)*L)
    s = np.sin(np.sqrt(k)*L)
    
    M11 = ch
    M12 = sh/np.sqrt(k)
    M21 = np.sqrt(k)*sh
    M22 = ch
    
    M33 = c
    M34 = s/np.sqrt(k)
    M43 = -np.sqrt(k)*s
    M44 = c
    
    if t:
        M11 = 1
        M12 = 0
        M21 = k*L
        M22 = 1
        
        M33 = 1
        M34 = 0
        M43 = -k*L
        M44 = 1
    
    
    
    M = np.array([[M11,M12,0,0],[M21,M22,0,0],[0,0,M33,M34],[0,0,M43,M44]])
    
    return M

def drift(L):
    
    M11 = 1
    M12 = L
    M21 = 0
    M22 = 1
    
    M33 = 1
    M34 = L
    M43 = 0
    M44 = 1
    
    M = np.array([[M11,M12,0,0],[M21,M22,0,0],[0,0,M33,M34],[0,0,M43,M44]])
    
    return M



def dipole(L,L_max,alpha,beta_s=0,beta_e=0):
    '''@ param L: scalar, length of path in dipole
       @ param alpha: scalar, bending angle in rad
       @ param beta: face angle in rad, 0 for SBEND (default), alpha/2 for RBEND, (larger, outer arc smaller)'''

    rho_0 = L_max/alpha

    alpha = L/rho_0   

    E11 = 1
    E12 = 0
    E21 = np.tan(beta_s)/rho_0
    E22 = 1
    
    E33 = 1
    E34 = 0
    E43 = -np.tan(beta_s)/rho_0 #TODO: just approx.
    E44 = 1
    
    E_s = np.array([[E11,E12,0,0],[E21,E22,0,0],[0,0,E33,E34],[0,0,E43,E44]])

    E11 = 1
    E12 = 0
    E21 = np.tan(beta_e)/rho_0
    E22 = 1
    
    E33 = 1
    E34 = 0
    E43 = -np.tan(beta_e)/rho_0 #TODO: just approx.
    E44 = 1
    
    E_e = np.array([[E11,E12,0,0],[E21,E22,0,0],[0,0,E33,E34],[0,0,E43,E44]])



    M11 = np.cos(alpha)
    M12 = rho_0*np.sin(alpha)
    M21 = -np.sin(alpha)/rho_0
    M22 = np.cos(alpha)
    
    M33 = 1
    M34 = L
    M43 = 0
    M44 = 1

    M = np.array([[M11,M12,0,0],[M21,M22,0,0],[0,0,M33,M34],[0,0,M43,M44]])

    M = bl([E_s,M,E_e])
    #TODO: this gives the right result at the end but however
    # is wrong for plotting since all elements plotted have edge
    # focusing effects which only occur at the beg/end. 

    #M = bl([E,M])
    #if L == L_max:
    #   M = bl([E,M,E]) #does not work properly because last point is omitted 


    
    return M    

# transport matrix of beamline
    
def bl(matrices):
    '''@ param matrices: list starting with first transport matrix'''
    for index in range(len(matrices)):
        try:
            matrices[index+1] = np.matmul(matrices[index+1],matrices[index])
        except: pass
    
    return matrices[-1]

# main planes of thick lens

def zplanes(matrix):

    z1x = (matrix[1][1]-1)/matrix[1][0]
    z2x = (matrix[0][0]-1)/matrix[1][0]
    
    z1y = (matrix[3][3]-1)/matrix[3][2]
    z2y = (matrix[2][2]-1)/matrix[3][2]
    
    return (z1x,z2x),(z1y,z2y)

# thin lens representation matrix of thick lens

def thin(matrix):
    
    zx,zy = zplanes(matrix)
    
    Z1x = drift(-zx[0])
    Z2x = drift(-zx[1])
    
    Z1y = drift(-zy[0])
    Z2y = drift(-zy[1])
    
    thinx = bl([Z1x,matrix,Z2x])
    thiny = bl([Z1y,matrix,Z2y])
    
    return thinx,thiny

# calculate s-dependent matrix elements

def Mplot(blist,llist):
    '''calculate s-dependent matrix elements of given beam line with specified lenghts.
    @param blist: list of functions of ion optical elements (careful: elements with multiple input params: partial)
    @param llist: list of lenghts of ion optical elements
    @return: 
        s: propagation
        first tuple: horizontal transport matrix elements
        second tuple: horizontal transport matrix elements
        
    '''
    M11, M12, M21, M22, M33, M34, M43, M44 = ([] for i in range(8))
    
    dec = max([str(i)[::-1].find('.') for i in llist])
    step = 10**-dec
    
    M_static = [ele(length) for ele,length in zip(blist,llist)]
    M_dyn = lambda x: [ele(x) for ele in blist]
    # save static elements in list and multiply current l-dependent matrix with it
    for i,l in enumerate(llist):
        dist = np.arange(0,l,step)
        for d in dist:
            stat = M_static[:i]
            dyn = [M_dyn(d)[i]]
            stat.extend(dyn)
            
            M_temp = bl(stat)

            M11.append(M_temp[0][0])
            M12.append(M_temp[0][1])
            M21.append(M_temp[1][0])
            M22.append(M_temp[1][1])
            
            M33.append(M_temp[2][2])
            M34.append(M_temp[2][3])
            M43.append(M_temp[3][2])
            M44.append(M_temp[3][3])
            
            
            
    s = np.arange(0,round(sum(llist),dec),step)
        
    return s,(M11,M12,M21,M22),(M33,M34,M43,M44)

# optimize quadrupole triplet settings (strength)

def opt_quad_mult(elements,lengths,image='P-to-P',S=True,prec=1e-3,iters=100,**kwargs):
    '''calculate quadrupole strengths for arbitrary sequence of beam line elements 
       for point-to-point or point-to-parallel imaging
       @param elements: list of functions, (drift, qdf, etc.)
       @param lengths: list of floats, lengths (caution: analyzation steps ~ digits of lengths
       @param image: string, P-to-P or P-to-Par
       @param S: bool, symmetric configuration
       @param prec: float, tolerance for termination
       @param iters: int, max. no. of iterations
       @param **kwargs: e.g. k_init: list, start values for k
       @return: list, optimized values for k'''

    no_qs = len([x for x in elements if (x == qdf or x == qf)])

    def residual(k):

        if 'k_fix' in kwargs.keys():
            for pos in kwargs['k_fix'].keys():
                k[pos] = kwargs['k_fix'][pos]

        p_elements = eles_to_peles(elements,k,S)
                


        if image == 'P-to-P':
            res = (Mplot(p_elements,lengths)[1][1][-1])**2 + (Mplot(p_elements,lengths)[2][1][-1])**2
        elif image == 'P-to-Par':
            res = (Mplot(p_elements,lengths)[1][0][-1])**2 + (Mplot(p_elements,lengths)[2][0][-1])**2


        return res

    if 'k_init' in kwargs.keys():
        k_init = kwargs['k_init']
    else:
        if S:
            k_init = [2]*round(no_qs/2)
        else:
            k_init = [2]*no_qs

    opt = sco.minimize(residual,k_init,tol=prec,options={'maxiter':iters})
    
    if opt.success == False:
        print(opt.status)


    
    return opt.x

def plot_M_vs_s(blist,llist,**kwargs):

    if 'figsize' in kwargs.keys():
        fig, ax = plt.subplots(1,2, figsize=kwargs['figsize'])
    else:
        fig, ax = plt.subplots(1,2) 


    ax[0].plot(Mplot(blist,llist)[0],Mplot(blist,llist)[1][0])
    ax[0].plot(Mplot(blist,llist)[0],Mplot(blist,llist)[2][0])

    ax[1].plot(Mplot(blist,llist)[0],Mplot(blist,llist)[1][1])
    ax[1].plot(Mplot(blist,llist)[0],Mplot(blist,llist)[2][1])

    ax[0].legend(['M11','M33'])
    ax[1].legend(['M12','M34'])

    ax[0].set_xlabel('s [m]')
    ax[1].set_xlabel('s [m]')

    return ax

def eles_to_peles(elements,k,S):
    '''convert list of elements to list with partials and fixed ks, considers symmetry
       @param elements: list of functions (w/o partials)
       @param k: list of quadrupole strengths t.b. assigned
       @param S: bool, symmetry. length of k needs to be adapted
       @return: list of functions, k assigned, w/ partials'''

    no_qs = len([x for x in elements if (x == qdf or x == qf)])

    p_elements = []
    j = 0
    q = 0
    for i,x in enumerate(elements):
        if x == qdf or x == qf:

            p_elements.append(partial(x,k = k[j]))

            if S:
                if q+1 > no_qs/2:
                    j-=1
                elif q+1 == no_qs/2:
                    pass
                else:
                    j+=1
            else:
                j+=1

            q+=1

        else:
            p_elements.append(elements[i])  

    return p_elements



    
        

