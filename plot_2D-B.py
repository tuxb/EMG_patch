import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import h5py

con1 = 'Particles'

for i in range(0,1):#(rank, 21, size):
    i = i*10
    t = float(i)*1.#/10.


    R = h5py.File('./snapshot_%03d.hdf5'% i)

    pos = R['PartType0']['Coordinates']
    x = np.transpose(pos)[0]
    y = np.transpose(pos)[1]

    MF = R['PartType0']['MagneticField']
    rho1 = np.transpose(MF)[0]
    rho2 = np.transpose(MF)[1]
    h = R['PartType0']['SmoothingLength'] 

    x = np.array(x)
    y = np.array(y)
    rho1 = np.array(rho1)
    rho2 = np.array(rho2)
    rho = (rho1*rho1 + rho2*rho2)/2
    rho = rho*1.e+6
    h = np.array(h)


    sort_rho = np.argsort(rho)
    x = x[sort_rho]
    y = y[sort_rho]
    rho = rho[sort_rho]
    h = h[sort_rho]

    # shift
    
    #x += 0.5
    #y += 0.5
    #x[x>1.0] -= 1.0
    #y[y>1.0] -= 1.0
    
    print('t=%1.6f rho_max=%2.16lf rho_min=%2.16lf' %(t, max(rho), min(rho)))

    fig, ax = plt.subplots(figsize=(3,3))
    ax.set_aspect('equal')

    ax.set_xlim(0.,1.)
    ax.set_ylim(0.,1.)
    ax.set_xticks([])
    ax.set_yticks([])

    img = ax.scatter(x, y, c=rho, cmap='jet', s=0.1, vmin=0.0, vmax=1., marker='o')

#    ax.set_xlabel(r'$x$')
#    ax.set_ylabel(r'$y$')

    position=fig.add_axes([0.15, 0.9, 0.7, 0.03])    
    cbar = fig.colorbar(img, cax=position, orientation='horizontal')
    ax2 = cbar.ax
    ax2.tick_params(which='major',direction='in',labelsize=8)
    ax2.xaxis.set_ticks(np.arange(0.0,1.1,0.2))
    ax2.xaxis.set_ticks_position('top')
    ax.set_title(r'$B^{2}/2, t=%1.1f$'%t, fontsize=18, position=(0.5,1.15))


    fig.savefig('./BFLD'+'_%1.4f.png' %t, bbox_inches='tight',dpi=fig.dpi)#,pad_inches=0.0)
    plt.close()

    
