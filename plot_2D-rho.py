import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import h5py


con1 = 'Particles'

for i in range(1,2):#(rank, 21, size):
    i = i*5    
    t = float(i)*1./10.


    R = h5py.File('./snapshot_%03d.hdf5'% i)

    pos = R['PartType0']['Coordinates']
    x = np.transpose(pos)[0]
    y = np.transpose(pos)[1]

#    rho1 = R['PartType0']['MagneticField']
    rho = R['PartType0']['Density']
    h = R['PartType0']['SmoothingLength'] 

    x = np.array(x)
    y = np.array(y)
    rho = np.array(rho)
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
    
    print('t=%1.6f rho_max=%1.6lf rho_min=%1.6lf' %(t, max(rho), min(rho)))

    fig, ax = plt.subplots(figsize=(3,3))
    #fig, ax = plt.subplots()
    ax.set_aspect('equal')

    ax.set_xlim(0.,1.)
    ax.set_ylim(0.,1.)
    ax.set_xticks([])
    ax.set_yticks([])


    print(ax.get_xlim()[-1] - ax.get_xlim()[0], fig.dpi)

    s_const = ax.get_window_extent().width / (ax.get_xlim()[-1] - ax.get_xlim()[0])  * 72. / fig.dpi 

    s = []
    for j in range(len(rho)):
        s_r = (0.5 * h[j] * s_const) ** 2
        #s_r = 3
        s.append(int(np.ceil(s_r)))
    s = np.array(s)

    print('s_min:%ld, s_max:%ld' %(min(s), max(s)))

    for j in range(max(s), min(s)-1, -1):
        if j in s:
            select_s = (s==j)

            xp = x[select_s]
            yp = y[select_s]
            rp = rho[select_s]

            img = ax.scatter(xp, yp, c=rp, cmap='jet', s=j, vmin=0.1, vmax=0.5, marker='o')

#    ax.set_xlabel(r'$x$')
#    ax.set_ylabel(r'$y$')

    position=fig.add_axes([0.163, 0.9, 0.7, 0.03])    
    cbar = fig.colorbar(img, cax=position, orientation='horizontal')
    ax2 = cbar.ax
    ax2.tick_params(which='major', direction='in', labelsize=8)
    ax2.xaxis.set_ticks(np.arange(0.1,0.51,0.1))
    ax2.xaxis.set_ticks_position('top')
    ax2.set_title(r'$\rho, t=%1.1f$'%t, fontsize=18, position=(0.5,3.3))


    fig.savefig('./rho'+'_%1.4f.png' %t, bbox_inches='tight',dpi=fig.dpi)#,pad_inches=0.0)
    plt.close()

    
