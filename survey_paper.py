import os
import pyfits
import numpy as np
import glob
import shutil

import matplotlib.pyplot as plt

USE_PLOT_GUI=False

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

from pyraf import iraf
from iraf import iraf

import threedhst
import threedhst.eazyPy as eazy
import threedhst.catIO as catIO
import unicorn

import re

noNewLine = '\x1b[1A\x1b[1M'

root = None

def throughput():
    os.chdir('/research/HST/GRISM/3DHST/ANALYSIS/SURVEY_PAPER')
    
    xg141, yg141 = np.loadtxt('g141.dat', unpack=True)
    xf140, yf140 = np.loadtxt('f140w.dat', unpack=True)
    xf814, yf814 = np.loadtxt('f814w.dat', unpack=True)
    xg800l, yg800l = np.loadtxt('g800l.dat', unpack=True)

    fig = unicorn.catalogs.plot_init(square=True, xs=8, aspect=1./3, left=0.12)
    
    plt.plot(xg141, yg141, color='black', linewidth=2, alpha=0.5)
    plt.fill(xg141, yg141, color='red', linewidth=2, alpha=0.1)
    plt.plot(xf140, yf140, color='black', linewidth=2, alpha=0.7)
    
    plt.plot(xg800l, yg800l, color='black', linewidth=2, alpha=0.5)
    plt.fill(xg800l, yg800l, color='blue', linewidth=2, alpha=0.1)
    plt.plot(xf814, yf814, color='black', linewidth=2, alpha=0.7)
    
    

    em_lines = [3727, 4861, 5007, 6563.]
    offset = np.array([0,-0.05,0,0])
    offset = 0.25+np.array([-0.15,-0.1,0.02,-0.1])

    em_names = ['[OII]',r'H$\beta$','[OIII]',r'H$\alpha$']
    
    dlam = 25
    zi = 1
    
    show_spectra = False
    colors=['blue','green','red']    
    if show_spectra:
      for zi in [1,2,3]:
        sedx, sedy = np.loadtxt('templates/EAZY_v1.0_lines/eazy_v1.0_sed4_nolines.dat', unpack=True)
        sedy *= 1.*sedy.max()
        dl = dlam/(1+zi)
        for em_line in em_lines:
            em_gauss = 1./np.sqrt(2*np.pi*dl**2)*np.exp(-1*(sedx-em_line)**2/2/dl**2)
            sedy += em_gauss/em_gauss.max()*0.6

        plt.plot(sedx*(1+zi), sedy*0.4+0.5, color=colors[zi-1], alpha=0.7, linewidth=2)
        plt.text(5500.,1.18-zi*0.13,r'$z=%d$' %(zi), color=colors[zi-1], fontsize=11)
        
      for i in range(4):
        plt.text(em_lines[i]*(1+1), 1+offset[i], em_names[i], horizontalalignment='center', fontsize=10)
    
    show_continuous = True
    if show_continuous:
        em_lines = [3727, 5007, 6563.]
        zgrid = np.arange(1000)/1000.*4
        for line in em_lines:
            plt.plot(line*(1+zgrid), zgrid/4.*0.8+0.5, linewidth=2, alpha=0.5, color='black')
        for zi in [0,1,2,3]:
            plt.plot([0.1,2.e4],np.array([zi,zi])/4.*0.8+0.5, linestyle='--', color='black', alpha=0.2)
            
    
    plt.text(5800, 0.08,'G800L',rotation=33., color='black', alpha=0.7)
    plt.text(5800, 0.08,'G800L',rotation=33., color='blue', alpha=0.4)

    plt.text(7100, 0.03,'F814W',rotation=80., color='black', alpha=0.9)

    plt.text(1.115e4, 0.17,'G141',rotation=15., color='black', alpha=0.7)
    plt.text(1.115e4, 0.17,'G141',rotation=15., color='red', alpha=0.4)

    plt.text(1.21e4, 0.03,'F140W',rotation=88., color='black', alpha=0.9)

    
    plt.xlim(4500, 1.79e4)
    plt.ylim(0,1.4)
    plt.xlabel(r'$\lambda$')
    plt.ylabel('throughput')
    
    fig.savefig('throughput.pdf')
    
def orbit_structure():
    """
    Show the POSTARG offsets in WFC3 / ACS
    """
    
    os.chdir('/research/HST/GRISM/3DHST/ANALYSIS/SURVEY_PAPER')
    
    fig = unicorn.catalogs.plot_init(square=True, xs=5, aspect=1, left=0.12)
    ax = fig.add_subplot(111)
    
    a11 = 0.1355
    b10 = 0.1211 # arcsec / pix, from instrument HB
    
    #dxs = np.array([0,-20,-13,7]) + np.int(np.round(xsh[0]))*0
    #dys = np.array([0,-7,-20,-13]) + np.int(np.round(ysh[0]))*0
    
    xpostarg = np.array([0, 1.355, 0.881, -0.474])
    ypostarg = np.array([0, 0.424, 1.212, 0.788])
    
    xoff = xpostarg/a11
    yoff = ypostarg/b10
        
    ax.plot(xoff, yoff, marker='o', markersize=10, color='red', alpha=0.8, zorder=10)
    
    if 1 == 1:
        for i in range(4):
            ax.text(xoff[i], yoff[i]+0.5, 'F140W + G141', horizontalalignment='center', backgroundcolor='white', zorder=20)
            
    ax.set_xlabel(r'$x$ offset [pix]')
    ax.set_ylabel(r'$y$ offset [pix]')

    scale = 4
    x0 = -2.9
    y0 = -5.5
    
    ax.fill(np.array([0,1,1,0])*scale+x0, np.array([0,0,1,1])*scale+y0, color='white', zorder=10)
    ax.fill(np.array([0,1,1,0])*scale+x0, np.array([0,0,1,1])*scale+y0, color='black', alpha=0.1, zorder=11)
    ax.plot(np.array([0.5,0.5])*scale+x0, np.array([0,1])*scale+y0, color='black', alpha=0.2, zorder=12)
    ax.plot(np.array([0,1])*scale+x0, np.array([0.5,0.5])*scale+y0, color='black', alpha=0.2, zorder=12)
    
    ax.plot(np.abs(xoff-np.cast[int](xoff))*scale+x0, np.abs(yoff-np.cast[int](yoff))*scale+y0, marker='o', markersize=10, color='red', alpha=0.8, zorder=13)
    ax.text(x0+scale/2., y0-1, 'WFC3 Primary', horizontalalignment='center')
    
    #plt.xlim(-5,11)
    #plt.ylim(-5,11)
    
    #### ACS:
    # XPOS = x*a11 + y*a10
    # YPOS = x*b11 + y*b10
    # 
    #       a10    a11      b10     b11
    # WFC: 0.0000   0.0494  0.0494  0.0040
    a10, a11, b10, b11 =  0.0000,0.0494,0.0494,0.0040
    #xoff = np.cumsum(xpostarg)
    #yoff = np.cumsum(ypostarg)

    acsang = 45.
    acsang = 92.16- -45.123
    xpos_acs, ypos_acs = threedhst.utils.xyrot(xpostarg, ypostarg, acsang)
    xpix_acs = xpos_acs / a11
    ypix_acs = (ypos_acs-xpix_acs*b11)/b10

    x0 = 5.5
    #y0 = -4.5
    
    ax.fill(np.array([0,1,1,0])*scale+x0, np.array([0,0,1,1])*scale+y0, color='white', zorder=10)
    ax.fill(np.array([0,1,1,0])*scale+x0, np.array([0,0,1,1])*scale+y0, color='black', alpha=0.1, zorder=11)
    ax.plot(np.array([0.5,0.5])*scale+x0, np.array([0,1])*scale+y0, color='black', alpha=0.2, zorder=12)
    ax.plot(np.array([0,1])*scale+x0, np.array([0.5,0.5])*scale+y0, color='black', alpha=0.2, zorder=12)

    ax.plot(np.abs(xpix_acs-np.cast[int](xpix_acs))*scale+x0, np.abs(ypix_acs-np.cast[int](ypix_acs))*scale+y0, marker='o', markersize=10, color='blue', alpha=0.8, zorder=13)
    #ax.plot(np.array([0,0.5,1,0.5])*scale+x0, np.array([0,0.5,0.5,1])*scale+y0, marker='o', marker='None', color='blue', linestyle='--', alpha=0.6, zorder=13)
    ax.plot(np.array([0,0.5,0.5,1])*scale+x0, np.array([0,1,0.5,0.5])*scale+y0, marker='o', marker='None', color='blue', linestyle='--', alpha=0.6, zorder=13)
    
    ax.text(x0+scale/2., y0-1, 'ACS Parallel', horizontalalignment='center')
    
    #plt.grid(alpha=0.5, zorder=1, markevery=5)
    
    from matplotlib.ticker import MultipleLocator, FormatStrFormatter

    ax.set_xlim(-5.9,12.5)
    #ax.set_ylim(-5.9,12.5)
    ax.set_ylim(-6.9,11.5)

    majorLocator   = MultipleLocator(5)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator   = MultipleLocator(1)

    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_minor_locator(minorLocator)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.xaxis.grid(alpha=0.5, zorder=1, which='major')
    ax.xaxis.grid(alpha=0.2, zorder=1, which='minor')

    ax.yaxis.set_major_locator(majorLocator)
    ax.yaxis.set_minor_locator(minorLocator)
    ax.yaxis.set_major_formatter(majorFormatter)
    ax.yaxis.grid(alpha=0.5, zorder=1, which='major')
    ax.yaxis.grid(alpha=0.2, zorder=1, which='minor')
        
    fig.savefig('dither_box.pdf')
    
def exptimes():
    """
    Extract the range of exposure times from the formatted Phase-II files
    """
    os.system('grep F814W 12???.pro   |grep " S " > f814w.exptime')
    os.system('grep G800L 12???.pro   |grep " S " > g800l.exptime')
    os.system('grep F140W *.pro |grep MULTIAC |grep NSAMP > f140w.exptime')
    os.system('grep G141 *.pro |grep MULTIAC |grep NSAMP > g141.exptime')
    
    ### G141
    fp = open('g141.exptime')
    lines = fp.readlines()
    fp.close()
    nsamp = []
    object = []
    for line in lines:
        nsamp.append(line.split('NSAMP=')[1][0:2])
        object.append(line.split()[1])
        
    expsamp = np.zeros(17)
    expsamp[12] = 1002.94
    expsamp[13] = 1102.94
    expsamp[14] = 1202.94
    expsamp[15] = 1302.94
    expsamp[16] = 1402.94
    
    nsamp = np.cast[int](nsamp)
    nsamp+=1 ### this seems to be the case for all actual observations !!
    objects = object[::4]
    NOBJ = len(nsamp)/4
    texp = np.zeros(NOBJ)
    for i in range(NOBJ):
        texp[i] = np.sum(expsamp[nsamp[i*4:(i+1)*4]])
        print objects[i], texp[i]
        
    print 'G141:  %.1f - %.1f' %(texp.min(), texp.max())
    
def spectral_features():
    wmin, wmax = 1.1e4, 1.65e4
    
    print '%-8s  %.1f -- %.1f' %('Halpha', wmin/6563.-1, wmax/6563.-1)
    print '%-8s  %.1f -- %.1f' %('OIII', wmin/5007.-1, wmax/5007.-1)
    print '%-8s  %.1f -- %.1f' %('OII', wmin/3727.-1, wmax/3727.-1)
    print '%-8s  %.1f -- %.1f' %('4000', wmin/4000.-1, wmax/4000.-1)

    wmin, wmax = 0.55e4, 1.0e4
    print '\n\nACS\n\n'
    print '%-8s  %.1f -- %.1f' %('Halpha', wmin/6563.-1, wmax/6563.-1)
    print '%-8s  %.1f -- %.1f' %('OIII', wmin/5007.-1, wmax/5007.-1)
    print '%-8s  %.1f -- %.1f' %('OII', wmin/3727.-1, wmax/3727.-1)
    print '%-8s  %.1f -- %.1f' %('4000', wmin/4000.-1, wmax/4000.-1)

def aXe_model():
    import copy
    import scipy.ndimage as nd
    
    os.chdir('/research/HST/GRISM/3DHST/ANALYSIS/SURVEY_PAPER')
    
    dir = pyfits.open('/research/HST/GRISM/3DHST/GOODS-S/PREP_FLT/UDF-F140W_drz.fits')
    gri = pyfits.open('/research/HST/GRISM/3DHST/GOODS-S/PREP_FLT/UDF-G141_drz.fits.gz')
    mod = pyfits.open('/research/HST/GRISM/3DHST/GOODS-S/PREP_FLT/UDF-FC-G141CONT_drz.fits.gz')

    #### rotate all the images so that dispersion axis is along X
    angle = gri[1].header['PA_APER']#+180
    direct = nd.rotate(dir[1].data, angle, reshape=False)
    grism = nd.rotate(gri[1].data, angle, reshape=False)
    model = nd.rotate(mod[1].data, angle, reshape=False)
    
    
    xc, yc = 1877, 2175
    NX, NY = 1270, 365
    aspect = 3.*NY/NX
    
    xc, yc = 1731, 977
    NX, NY = 882, 467
    
    aspect = 1.*NY/NX
    
    plt.gray()
    
    plt.rcParams['lines.linewidth'] = 2
    
    fig = unicorn.catalogs.plot_init(square=True, xs=8, aspect=aspect, left=0.12)
    
    fig.subplots_adjust(wspace=0.0,hspace=0.0,left=0.01,
                        bottom=0.015,right=0.99,top=0.985)
    
    fs1 = 15 ### Font size of label
    xlab, ylab = 0.04*NX/3., NY-0.02*NY
    
    ax = fig.add_subplot(221)
    ax.imshow(0-direct[yc-NY/2:yc+NY/2, xc-NX/2:xc+NX/2], vmin=-0.2, vmax=0.02, interpolation='nearest')
    ax.set_yticklabels([]); ax.set_xticklabels([])
    xtick = ax.set_xticks([0,NX]); ytick = ax.set_yticks([0,NY])
    ax.text(xlab, ylab, 'a) Direct F140W', fontsize=fs1, backgroundcolor='white', verticalalignment='top')

    #ax.text(xlab, ylab, r'$%d\times\ $$%d^{\prime\prime}$' %(NX*0.06, NY*0.06), fontsize=18, backgroundcolor='white', verticalalignment='top')
    
    ax = fig.add_subplot(222)
    ax.imshow(0-grism[yc-NY/2:yc+NY/2, xc-NX/2:xc+NX/2], vmin=-0.04, vmax=0.004, interpolation='nearest')
    ax.set_yticklabels([]); ax.set_xticklabels([])
    xtick = ax.set_xticks([0,NX]); ytick = ax.set_yticks([0,NY])
    ax.text(xlab, ylab, 'b) Grism G141', fontsize=fs1, backgroundcolor='white', verticalalignment='top')

    ax = fig.add_subplot(223)
    diff = grism-model
        
    ### Flag em lines and 0th order
    dy0 = 20
    
    emx, emy = [223, 272, 487, 754, 520, 850, 565, 558, 51, 834, 345, 495], [122, 189, 83, 240, 148, 124, 336, 418, 338, 225, 197, 268]
    ax.plot(np.array(emx)+(xc-1731), np.array(emy)-dy0+(yc-977), marker='o', markersize=5, linestyle='None', color='green', alpha=0.9)
    
    zx, zy = [301, 393, 648], [183, 321, 446]
    ax.plot(np.array(zx)+(xc-1731), np.array(zy)-dy0+(yc-977), marker='o', markersize=5, linestyle='None', color='red', alpha=0.9)

    ax.text(0.04*NX/3., 0.02*NY, 'Em.', fontsize=fs1*0.8, backgroundcolor='white', verticalalignment='bottom', color='green')
    ax.text(0.3*NX/3., 0.02*NY, r'0th', fontsize=fs1*0.8, backgroundcolor='white', verticalalignment='bottom', color='red')
    
    ax.imshow(0-diff[yc-NY/2:yc+NY/2, xc-NX/2:xc+NX/2], vmin=-0.02, vmax=0.002, interpolation='nearest')
    ax.set_yticklabels([]); ax.set_xticklabels([])
    xtick = ax.set_xticks([0,NX]); ytick = ax.set_yticks([0,NY])
    ax.text(xlab, ylab, r'd) Grism$-$model', fontsize=fs1, backgroundcolor='white', verticalalignment='top')
    
    ax = fig.add_subplot(224)
    ax.imshow(0-model[yc-NY/2:yc+NY/2, xc-NX/2:xc+NX/2], vmin=-0.04, vmax=0.004, interpolation='nearest')
    ax.set_yticklabels([]); ax.set_xticklabels([])
    xtick = ax.set_xticks([0,NX]); ytick = ax.set_yticks([0,NY])
    ax.text(xlab, ylab, r'c) aXe Model', fontsize=fs1, backgroundcolor='white', verticalalignment='top')
    
    fig.savefig('grism_model.pdf')
    
def sync():
    pass
    """
paths="RAW HTML/scripts PREP_FLT"
dirs="AEGIS COSMOS ERS GOODS-N GOODS-S SN-GEORGE SN-MARSHALL SN-PRIMO UDS"
for dir in $dirs; do 
    mkdir ${dir}
    mkdir ${dir}/HTML
    for path in $paths; do 
        # du -sh ${dir}/${path}
        mkdir ${dir}/${path}
        rsync -avz --progress $UNICORN:/3DHST/Spectra/Work/${dir}/${path} ${dir}/${path} 
    done
done


    """
def all_pointings():
    pointings(ROOT='GOODS-SOUTH')
    pointings(ROOT='COSMOS')
    pointings(ROOT='AEGIS')
    pointings(ROOT='UDS')
    pointings(ROOT='GOODS-N')

def all_pointings_width():
    from unicorn.survey_paper import pointings
    
    pointings(ROOT='GOODS-SOUTH', width=7, corner='ll')
    pointings(ROOT='COSMOS', width=6, corner='lr')
    pointings(ROOT='AEGIS', width=7, corner='ll')
    pointings(ROOT='UDS', width=9, corner='lr')
    pointings(ROOT='GOODS-N', width=6, corner='ur')
        
def pointings(ROOT='GOODS-SOUTH', width=None, corner='lr'):
    """ 
    Make a figure showing the 3D-HST pointing poisitions, read from region files
    """
    import unicorn.survey_paper as sup
    
    plt.rcParams['lines.linewidth'] = 0.3
    wfc3_color = 'blue'
    acs_color = 'green'
    
    os.chdir(unicorn.GRISM_HOME+'ANALYSIS/SURVEY_PAPER')
    yticklab = None
    
    dx_ref = (53.314005633802822-52.886197183098595)*np.cos(-27.983151830808076/360*2*np.pi)
    CANDELS_PATH = '/research/HST/GRISM/3DHST/REGIONS/CANDELS/'
    candels_files = []
    candels_alpha = 0.3
    candels_color = '0.1'
    
    
    #### GOODS-S
    if ROOT=='GOODS-SOUTH':
        x0, x1 = 53.314005633802822,  52.886197183098595
        y0, y1 = -27.983151830808076, -27.654474431818176
        xticklab = [r'$3^\mathrm{h}33^\mathrm{m}00^\mathrm{s}$', r'$3^\mathrm{h}32^\mathrm{m}30^\mathrm{s}$', r'$3^\mathrm{h}32^\mathrm{m}00^\mathrm{s}$']
        xtickv = [degrees(3,33,00, hours=True), degrees(3,32,30, hours=True), degrees(3,32,00, hours=True)]
        yticklab = [r'$-27^\circ40^\prime00^{\prime\prime}$', r'$45^\prime00^{\prime\prime}$', r'$-27^\circ50^\prime00^{\prime\prime}$', r'$55^\prime00^{\prime\prime}$']
        ytickv = [degrees(-27, 40, 00, hours=False), degrees(-27, 45, 00, hours=False), degrees(-27, 50, 00, hours=False), degrees(-27, 55, 00, hours=False)]
        candels_files = glob.glob(CANDELS_PATH+'/GOODS-S*reg')
        candels_files.extend(glob.glob(CANDELS_PATH+'/GOODS-W*reg'))
    
    #### COSMOS
    if ROOT=='COSMOS':
        x1, x0 = 149.99120563380279, 150.23823661971829
        y0, y1 = 2.1678109478476815, 2.5996973302980129
        xticklab = [r'$10^\mathrm{h}00^\mathrm{m}30^\mathrm{s}$', r'$00^\mathrm{m}00^\mathrm{s}$']
        xtickv = [degrees(10,00,30, hours=True), degrees(10,00,00, hours=True)]
        yticklab = [r'$+2^\circ15^\prime00^{\prime\prime}$', r'$25^\prime00^{\prime\prime}$', r'$35^\prime00^{\prime\prime}$']
        ytickv = [degrees(02, 15, 00, hours=False), degrees(02, 25, 00, hours=False), degrees(02, 35, 00, hours=False)]
        candels_files = glob.glob(CANDELS_PATH+'/COSMOS*reg')
    
    #### AEGIS
    if ROOT=='AEGIS':
        x1, x0 = 214.49707154104345, 215.12704734584406
        y0, y1 = 52.680946433013482, 53.01597137966467
        xticklab = [r'$18^\mathrm{m}00^\mathrm{s}$', r'$14^\mathrm{h}19^\mathrm{m}00^\mathrm{s}$', r'$20^\mathrm{m}00^\mathrm{s}$']
        xtickv = [degrees(14,18,00, hours=True), degrees(14,19,00, hours=True), degrees(14,20,00, hours=True)]
        yticklab = [r'$+52^\circ45^\prime00^{\prime\prime}$', r'$50^\prime00^{\prime\prime}$', r'$55^\prime00^{\prime\prime}$']
        ytickv = [degrees(52, 45, 00, hours=False), degrees(52, 50, 00, hours=False), degrees(52, 55, 00, hours=False)]
        candels_files = glob.glob(CANDELS_PATH+'/EGS*reg')
    
    #### UDS
    if ROOT=='UDS':
        x1, x0 = 34.116935194128146, 34.51871547581829
        y0, y1 = -5.2957542206957582, -5.0834327182123147+2./3600
        xticklab = [r'$18^\mathrm{m}00^\mathrm{s}$', r'$2^\mathrm{h}17^\mathrm{m}30^\mathrm{s}$', r'$17^\mathrm{m}00^\mathrm{s}$', r'$16^\mathrm{m}30^\mathrm{s}$']
        xtickv = [degrees(2,18,00, hours=True), degrees(2,17,30, hours=True), degrees(2,17,00, hours=True), degrees(2,16,30, hours=True)]
        yticklab = [r'$05^\prime00^{\prime\prime}$', r'$-5^\circ10^\prime00^{\prime\prime}$', r'$15^\prime00^{\prime\prime}$']
        ytickv = [degrees(-5, 05, 00, hours=False), degrees(-5, 10, 00, hours=False), degrees(-5, 15, 00, hours=False)]
        candels_files = glob.glob(CANDELS_PATH+'/UDS*reg')
    
    #### GOODS-N
    if ROOT=='GOODS-N':
        wfc3_color = 'orange'
        acs_color = None
        x1, x0 = 188.9139017749491, 189.44688055895648
        y0, y1 = 62.093791549511998, 62.384068625281309
        xticklab = [r'$12^\mathrm{h}37^\mathrm{m}30^\mathrm{s}$', r'$37^\mathrm{m}00^\mathrm{s}$', r'$36^\mathrm{m}30^\mathrm{s}$', r'$36^\mathrm{m}00^\mathrm{s}$']
        xtickv = [degrees(12,37,30, hours=True), degrees(12,37,00, hours=True), degrees(12,36,30, hours=True), degrees(12,36,00, hours=True)]
        yticklab = [r'$+62^\circ10^\prime00^{\prime\prime}$', r'$15^\prime00^{\prime\prime}$', r'$20^\prime00^{\prime\prime}$']
        ytickv = [degrees(62, 10, 00, hours=False), degrees(62, 15, 00, hours=False), degrees(62, 20, 00, hours=False)]
        candels_files = glob.glob(CANDELS_PATH+'/GOODSN-OR*reg')
        candels_files.extend(glob.glob(CANDELS_PATH+'/GOODSN-SK*reg'))
        
    #### Make square for given plot dimensions
    dx = np.abs(x1-x0)*np.cos(y0/360*2*np.pi)
    dy = (y1-y0)
    
    if width is None:
        width = 7*dx/dx_ref
    
    print '%s: plot width = %.2f\n' %(ROOT, width)
        
    fig = unicorn.catalogs.plot_init(square=True, xs=width, aspect=dy/dx)
    #fig = unicorn.catalogs.plot_init(square=True)
    
    ax = fig.add_subplot(111)
    
    polys = []
    for file in candels_files:
        fp = open(file)
        lines = fp.readlines()
        fp.close()
        #
        polys.append(sup.polysplit(lines[1], get_shapely=True))
        #fi = ax.fill(wfcx, wfcy, alpha=candels_alpha, color=candels_color)
    
    sup.polys = polys
    
    un = polys[0]
    for pp in polys[1:]:
        un = un.union(pp)
    
    if un.geometryType() is 'MultiPolygon':
        for sub_poly in un.geoms:
            x,y = sub_poly.exterior.xy
            ax.plot(x,y, alpha=candels_alpha, color=candels_color, linewidth=1)
            ax.fill(x,y, alpha=0.1, color='0.7')
    else:        
        x,y = un.exterior.xy
        ax.plot(x,y, alpha=candels_alpha, color=candels_color, linewidth=1)
        ax.fill(x,y, alpha=0.1, color='0.7')
    
    files=glob.glob(unicorn.GRISM_HOME+'REGIONS/'+ROOT+'-[0-9]*reg')
    for file in files:
        #
        field = re.split('-[0-9]', file)[0]
        pointing = file.split(field+'-')[1].split('.reg')[0]
        fp = open(file)
        lines = fp.readlines()
        fp.close()
        #
        wfcx, wfcy = sup.polysplit(lines[1])
        fi = ax.fill(wfcx, wfcy, alpha=0.2, color=wfc3_color)
        #
        if acs_color is not None:
            acsx1, acsy1 = sup.polysplit(lines[2])
            acsx2, acsy2 = sup.polysplit(lines[3])
            #
            fi = ax.fill(acsx1, acsy1, alpha=0.05, color=acs_color)
            fi = ax.fill(acsx2, acsy2, alpha=0.05, color=acs_color)
            pl = ax.plot(acsx1, acsy1, alpha=0.1, color=acs_color)
            pl = ax.plot(acsx2, acsy2, alpha=0.1, color=acs_color)
        #
        xoff, yoff = 0.0, 0.0
        if ROOT=='GOODS-SOUTH':
            #print pointing
            if pointing == '36':
                xoff, yoff = 0.002,0.0075
            if pointing == '37':
                xoff, yoff = -0.005,-0.007
            if pointing == '38':
                xoff, yoff = 0.007,-0.007
            
        te = ax.text(np.mean(wfcx[:-1])+xoff, np.mean(wfcy[:-1])+yoff, pointing, va='center', ha='center', fontsize=13)
    
    #    
    if yticklab is not None:
        ax.set_xticklabels(xticklab)
        xtick = ax.set_xticks(xtickv)
        ax.set_yticklabels(yticklab)
        ytick = ax.set_yticks(ytickv)
    
    ax.set_xlabel(r'$\alpha$')
    ax.set_ylabel(r'$\delta$')
    
    fsi = '20'
    
    if corner=='lr':
        ax.text(0.95, 0.05,r'$\mathit{%s}$' %(ROOT),
            horizontalalignment='right',
            verticalalignment='bottom',
            transform = ax.transAxes, fontsize=fsi)
    #
    if corner=='ll':
        ax.text(0.05, 0.05,r'$\mathit{%s}$' %(ROOT),
            horizontalalignment='left',
            verticalalignment='bottom',
            transform = ax.transAxes, fontsize=fsi)
    #
    if corner=='ur':
        ax.text(0.95, 0.95,r'$\mathit{%s}$' %(ROOT),
            horizontalalignment='right',
            verticalalignment='top',
            transform = ax.transAxes, fontsize=fsi)
    #
    if corner=='ul':
        ax.text(0.05, 0.95,r'$\mathit{%s}$' %(ROOT),
            horizontalalignment='left',
            verticalalignment='top',
            transform = ax.transAxes, fontsize=fsi)
    
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    
    print 'RA  - ', hexagesimal(x0), hexagesimal(x1)
    print 'Dec - ', hexagesimal(y0, hours=False), hexagesimal(y1, hours=False)
    
    plt.savefig('%s_pointings.pdf' %(ROOT))

def degrees(deg, min, sec, hours=True):
    
    adeg = np.abs(deg)
    degrees = adeg + min/60. + sec/3600.
    if deg < 0:
        degrees *= -1
    
    if hours:
        degrees *= 360./24
        
    return degrees
    
def hexagesimal(degrees, hours=True, string=True):
    if hours:
        degrees *= 24/360.
    
    if degrees < 0:
        sign = -1
        si = '-'
    else:
        sign = 1
        si = ''
        
    degrees = np.abs(degrees)
    
    deg = np.int(degrees)
    min = np.int((degrees-deg)*60)
    sec = (degrees-deg-min/60.)*3600
    
    if string:
        return '%s%02d:%02d:%05.2f' %(si, deg, min, sec)
    else:
        return sign*deg, min, sec

def polysplit(region='polygon(150.099223,2.391097,150.086084,2.422515,150.050573,2.407277,150.064586,2.376241)', get_shapely=False):
    
    spl = region[region.find('(')+1:region.find(')')].split(',')
    px = spl[0::2]
    py = spl[1::2]
    px.append(px[0])
    py.append(py[0])
    px, py = np.cast[float](px), np.cast[float](py)
    
    if get_shapely:
        from shapely.geometry import Polygon
        list = []
        for i in range(len(px)):
            list.append((px[i], py[i]))
        
        poly = Polygon(tuple(list))
        return poly
    else:
        return px, py
#
def demo_background_subtract(root='COSMOS-13'):
    """
    Make a figure demonstrating the background subtraction of the grism images
    """
    import threedhst
    import threedhst.prep_flt_files
    import threedhst.grism_sky as bg
    
    import unicorn
    import unicorn.survey_paper as sup
    import pyfits
    import iraf
    
    path = unicorn.analysis.get_grism_path(root)
    os.chdir(path)
    if not os.path.exists('EXAMPLE'):
        os.system('mkdir EXAMPLE')
    
    os.chdir('EXAMPLE')
    files = glob.glob('../PREP_FLT/%s-G141*' %(root))
    files.append('../PREP_FLT/%s-F140W_tweak.fits' %(root))
    
    for file in files: 
        if 'drz.fits' not in file:
            os.system('cp %s .' %(file))
            print file
    
    threedhst.process_grism.fresh_flt_files(root+'-G141_asn.fits')
    asn = threedhst.utils.ASNFile(root+'-G141_asn.fits')
    flt = pyfits.open(asn.exposures[0]+'_flt.fits')
    angle = flt[1].header['PA_APER']
    
    #### First run on uncorrected images
    threedhst.prep_flt_files.startMultidrizzle(root+'-G141_asn.fits', 
            use_shiftfile=True, skysub=False,
            final_scale=0.128254, pixfrac=0.8, driz_cr=True,
            updatewcs=True, median=True, clean=True, final_rot=angle)
        
    os.system('mv %s-G141_drz.fits %s-G141_drz_first.fits' %(root, root))
    
    sup.root = root
    sup.first_prof = []
    for exp in asn.exposures:
        xp, yp = threedhst.grism_sky.profile(exp+'_flt.fits', flatcorr=False, biweight=True)
        sup.first_prof.append(yp)
    
    # for i,exp in enumerate(asn.exposures):
    #     plt.plot(xp, prof[i])
        

    #### Now divide by the flat
    threedhst.process_grism.fresh_flt_files(root+'-G141_asn.fits')
    sup.flat_prof = []
    for exp in asn.exposures:
        bg.remove_grism_sky(flt=exp+'_flt.fits', list=['sky_cosmos.fits', 'sky_goodsn_lo.fits', 'sky_goodsn_hi.fits', 'sky_goodsn_vhi.fits'],  path_to_sky = '../CONF/', out_path='./', verbose=False, plot=False, flat_correct=True, sky_subtract=False, second_pass=False, overall=False)
        xp, yp = threedhst.grism_sky.profile(exp+'_flt.fits', flatcorr=False, biweight=True)
        sup.flat_prof.append(yp)
    
    threedhst.prep_flt_files.startMultidrizzle(root+'-G141_asn.fits', 
            use_shiftfile=True, skysub=False,
            final_scale=0.128254, pixfrac=0.8, driz_cr=True,
            updatewcs=True, median=True, clean=True, final_rot=angle)

    os.system('mv %s-G141_drz.fits %s-G141_drz_flat.fits' %(root, root))
    
    #### Divide by the sky
    threedhst.process_grism.fresh_flt_files(root+'-G141_asn.fits')
    sup.sky_prof = []
    for exp in asn.exposures:
        print exp
        bg.remove_grism_sky(flt=exp+'_flt.fits', list=['sky_cosmos.fits', 'sky_goodsn_lo.fits', 'sky_goodsn_hi.fits', 'sky_goodsn_vhi.fits'],  path_to_sky = '../CONF/', out_path='./', verbose=False, plot=False, flat_correct=True, sky_subtract=True, second_pass=False, overall=False)
        xp, yp = threedhst.grism_sky.profile(exp+'_flt.fits', flatcorr=False, biweight=True)
        sup.sky_prof.append(yp)
    
    threedhst.prep_flt_files.startMultidrizzle(root+'-G141_asn.fits', 
            use_shiftfile=True, skysub=False,
            final_scale=0.128254, pixfrac=0.8, driz_cr=True,
            updatewcs=True, median=True, clean=True, final_rot=angle)

    os.system('mv %s-G141_drz.fits %s-G141_drz_sky.fits' %(root, root))

    #### Last pass along columns
    threedhst.process_grism.fresh_flt_files(root+'-G141_asn.fits')
    sup.final_prof = []
    for exp in asn.exposures:
        print exp
        bg.remove_grism_sky(flt=exp+'_flt.fits', list=['sky_cosmos.fits', 'sky_goodsn_lo.fits', 'sky_goodsn_hi.fits', 'sky_goodsn_vhi.fits'],  path_to_sky = '../CONF/', out_path='./', verbose=False, plot=False, flat_correct=True, sky_subtract=True, second_pass=True, overall=True)
        xp, yp = threedhst.grism_sky.profile(exp+'_flt.fits', flatcorr=False, biweight=True)
        sup.final_prof.append(yp)
    
    threedhst.prep_flt_files.startMultidrizzle(root+'-G141_asn.fits', 
            use_shiftfile=True, skysub=False,
            final_scale=0.128254, pixfrac=0.8, driz_cr=True,
            updatewcs=True, median=True, clean=True, final_rot=angle)
    
    # ##### Make segmentation images
    # run = threedhst.prep_flt_files.MultidrizzleRun(root+'-G141')
    # for i,exp in enumerate(asn.exposures):
    #     run.blot_back(ii=i, copy_new=(i is 0))
    #     threedhst.prep_flt_files.make_segmap(run.flt[i])
    
    os.system('mv %s-G141_drz.fits %s-G141_drz_final.fits' %(root, root))
    
    make_plot(root=root)
    
def make_background_demo(root='AEGIS-11', range1=(0.90,1.08), range2=(-0.02, 0.02)):
    import unicorn.survey_paper as sup
    
    if sup.root != root:
        print "Need to run sup.demo_background_subtract(root='%s')." %(root)
        
    path = unicorn.analysis.get_grism_path(root)
    os.chdir(path+'EXAMPLE')

    first = pyfits.open('%s-G141_drz_first.fits' %(root))
    flat = pyfits.open('%s-G141_drz_flat.fits' %(root))
    sky = pyfits.open('%s-G141_drz_sky.fits' %(root))
    final = pyfits.open('%s-G141_drz_final.fits' %(root))
    
    im_shape = first[1].data.shape
    sup.im_shape = im_shape
    
    med = threedhst.utils.biweight(sky[1].data, mean=True)

    ysize = 3.
    #fig = plt.figure(figsize=[ysize*im_shape[1]*1./im_shape[0]*4,ysize], dpi=100)
    
    top_panel = 0.2
    NPANEL = 4
    
    if USE_PLOT_GUI:
        fig = plt.figure(figsize=[ysize*im_shape[1]*1./im_shape[0]*NPANEL*(1-top_panel),ysize],dpi=100)
    else:
        fig = Figure(figsize=[ysize*im_shape[1]*1./im_shape[0]*NPANEL*(1-top_panel),ysize], dpi=100)
    
    fig.subplots_adjust(wspace=0.02,hspace=0.02,left=0.01,
                        bottom=0.07,right=0.99,top=0.97)
    #
    
    vmin, vmax = -0.2, 0.1
    
    x0 = 0.005
    y0 = x0
    dx = (1.-(NPANEL+1)*x0)/NPANEL
    
    #ax = fig.add_subplot(141)
    ax = fig.add_axes(((x0+(dx+x0)*0), y0, dx, 1-top_panel-y0))
    
    ax.imshow(0-(first[1].data-med), interpolation='nearest',aspect='auto',vmin=vmin-0.1,vmax=vmax+0.15)    
    axis_imshow(ax, text='a)\ Raw')
    ax.text(0.12, 0.85, r'$\mathrm{%s}$' %(root), horizontalalignment='left', verticalalignment='center',
                 transform = ax.transAxes, color='black', fontsize=14)
    #
    #show_limits(ax, -(vmax+0.15)+med, -(vmin-0.1)+med)
    
    #### Show profiles
    ax = fig.add_axes(((x0+(dx+x0)*0), (1-top_panel), dx, top_panel-2*y0))
    pp = sup.first_prof[0]*0.
    for i in range(4):
        #ax.plot(sup.first_prof[i])
        pp += sup.first_prof[i]
    ax.plot(pp/4., color='black')
    axis_profile(ax, yrange=range1, text='a)\ Raw')
    
    #ax = fig.add_subplot(142)
    ax = fig.add_axes(((x0+(dx+x0)*1), y0, dx, 1-top_panel-y0))
    ax.imshow(0-(flat[1].data-med), interpolation='nearest',aspect='auto',vmin=vmin,vmax=vmax)    
    axis_imshow(ax, text='b)\ Flat')
    #show_limits(ax, -vmax+med, -vmin+med)

    #### Show profiles
    ax = fig.add_axes(((x0+(dx+x0)*1), (1-top_panel), dx, top_panel-2*y0))
    pp = sup.flat_prof[0]*0.
    for i in range(4):
        #ax.plot(sup.flat_prof[i])
        pp += sup.flat_prof[i]
    ax.plot(pp/4., color='black')
    axis_profile(ax, yrange=range1, text='b)\ Flat')
    
    #ax = fig.add_subplot(143)
    ax = fig.add_axes(((x0+(dx+x0)*2), y0, dx, 1-top_panel-y0))
    ax.imshow(0-(sky[1].data-med), interpolation='nearest',aspect='auto',vmin=vmin,vmax=vmax)    
    axis_imshow(ax, text='c)\ Sky')
    #show_limits(ax, -vmax+med, -vmin+med)
    
    #### Show profiles
    ax = fig.add_axes(((x0+(dx+x0)*2), (1-top_panel), dx, top_panel-2*y0))
    pp = sup.sky_prof[0]*0.
    for i in range(4):
        #ax.plot(sup.sky_prof[i])
        pp += sup.sky_prof[i]
    ax.plot(pp/4., color='black')
    axis_profile(ax, yrange=range1, text='c)\ Sky')

    #ax = fig.add_subplot(144)
    ax = fig.add_axes(((x0+(dx+x0)*3), y0, dx, 1-top_panel-y0))
    ax.imshow(0-(final[1].data), interpolation='nearest',aspect='auto',vmin=vmin,vmax=vmax)    
    axis_imshow(ax, text='d)\ Final')
    #show_limits(ax, -vmax, -vmin)
    
    #### Show profiles
    ax = fig.add_axes(((x0+(dx+x0)*3), (1-top_panel), dx, top_panel-2*y0))
    pp = sup.final_prof[0]*0.
    for i in range(4):
        #ax.plot(sup.final_prof[i])
        pp += sup.final_prof[i]
    ax.plot(pp/4., color='black')
    axis_profile(ax, yrange=range2, text='d)\ Final')
    
    outfile = '%s-G141_demo.pdf' %(root)
    
    if USE_PLOT_GUI:
        fig.savefig(outfile,dpi=100,transparent=False)
    else:
        canvas = FigureCanvasAgg(fig)
        canvas.print_figure(outfile, dpi=100, transparent=False)

def show_limits(ax, vmin, vmax):
    ax.text(0.98, -0.02,r'$\mathrm{[%.1f,\ %.1f]}$' %(vmin, vmax),
                 horizontalalignment='right',
                 verticalalignment='top',
                 transform = ax.transAxes, color='black', fontsize=12)

def axis_profile(ax, yrange=None, prof=None, text=''):
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_xlim(0,1000)
    if yrange is not None:
        ax.set_ylim(yrange[0], yrange[1])
        ylimits = yrange
    else:
        ylimits = ax.get_ylim()
    
    #
    if text is  not '':
        ax.text(0.5, 0.06,r'$\mathrm{'+text+'}$',
                     horizontalalignment='center',
                     verticalalignment='bottom',
                     transform = ax.transAxes, color='black', fontsize=10)
    
    ax.text(0.98, 0.08,r'$\mathrm{[%.3f,\ %.3f]}$' %(ylimits[0], ylimits[1]),
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 transform = ax.transAxes, color='black', fontsize=8)
    
        
def axis_imshow(ax, text='', shape=None):
    import numpy as np
    import unicorn.survey_paper as sup
    
    if shape is None:
        shape = sup.im_shape
    
    ax.set_yticklabels([])
    xtick = ax.set_xticks([0,shape[1]])
    ax.set_xticklabels([])
    ytick = ax.set_yticks([0,shape[0]])
    #
    # if text is  not '':
    #     ax.text(0.5, 1.02,r'$\mathrm{'+text+'}$',
    #                  horizontalalignment='center',
    #                  verticalalignment='bottom',
    #                  transform = ax.transAxes, color='black', fontsize=12)

def compare_sky():
    """
    Make a figure showing the aXe default and derived sky images.
    """
    import unicorn.survey_paper as sup
    
    sco = pyfits.open('../CONF/sky_cosmos.fits')
    shi = pyfits.open('../CONF/sky_goodsn_hi.fits')
    slo = pyfits.open('../CONF/sky_goodsn_lo.fits')
    svh = pyfits.open('../CONF/sky_goodsn_vhi.fits')
    
    shape = sco[0].data.shape
    
    figsize = 6
    fig = Figure(figsize=[figsize,figsize], dpi=200)
    #fig = plt.figure(figsize=[figsize,figsize], dpi=100)
    
    fig.subplots_adjust(wspace=0.02,hspace=0.02,left=0.02,
                        bottom=0.02,right=0.98,top=0.98)

    ####### COSMOS
    ax = fig.add_subplot(221)
    ax.imshow(sco[0].data, interpolation='nearest',aspect='auto',vmin=0.95,vmax=1.05)    
    sup.axis_imshow(ax, shape=shape)
    
    ax.fill_between([850,950],[50,50],[150,150], color='white', alpha=0.8)
    ax.text(900/1014., 100./1014,r'$\mathrm{a)}$', horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, color='black', fontsize=12)
    
    ####### GOODS-N Lo
    ax = fig.add_subplot(222)
    ax.imshow(slo[0].data, interpolation='nearest',aspect='auto',vmin=0.95,vmax=1.05)    
    sup.axis_imshow(ax, shape=shape)

    ax.fill_between([850,950],[50,50],[150,150], color='white', alpha=0.8)
    ax.text(900/1014., 100./1014,r'$\mathrm{b)}$', horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, color='black', fontsize=12)

    ####### GOODS-N Hi
    ax = fig.add_subplot(223)
    ax.imshow(shi[0].data, interpolation='nearest',aspect='auto',vmin=0.95,vmax=1.05)    
    sup.axis_imshow(ax, shape=shape)
    
    ax.fill_between([850,950],[50,50],[150,150], color='white', alpha=0.8)
    ax.text(900/1014., 100./1014,r'$\mathrm{c)}$', horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, color='black', fontsize=12)

    ####### GOODS-N Very hi
    ax = fig.add_subplot(224)
    ax.imshow(svh[0].data, interpolation='nearest',aspect='auto',vmin=0.95,vmax=1.05)    
    sup.axis_imshow(ax, shape=shape)
    
    ax.fill_between([850,950],[50,50],[150,150], color='white', alpha=0.8)
    ax.text(900/1014., 100./1014,r'$\mathrm{d)}$', horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, color='black', fontsize=12)
    
    #### Done
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure('sky_backgrounds.pdf', dpi=100, transparent=False)

def grism_flat_dependence():
    """
    Compute the higher order terms for the grism flat-field
    """
    
    import unicorn
    import threedhst
    
    # f140 = threedhst.grism_sky.flat_f140[1].data[5:-5, 5:-5]
    # 
    # flat = pyfits.open(unicorn.GRISM_HOME+'CONF/WFC3.IR.G141.flat.2.fits')
    # wmin, wmax = flat[0].header['WMIN'], flat[0].header['WMAX']
    # 
    # a0 = flat[0].data
    # 
    # lam = 1.1e4
    # x = (lam-wmin)/(wmax-wmin)
    # 
    # aX = a0*0.
    # for i,ext in enumerate(flat[1:]):
    #     print i
    #     aX += ext.data*x**(i+1)
        
    f105 = pyfits.open(os.getenv('iref')+'/uc72113oi_pfl.fits')[1].data[5:-5,5:-5]
    #f105 = pyfits.open(os.getenv('iref')+'/uc72113ni_pfl.fits')[1].data[5:-5,5:-5] # F098M
    f140 = pyfits.open(os.getenv('iref')+'/uc721143i_pfl.fits')[1].data[5:-5,5:-5]
    f160 = pyfits.open(os.getenv('iref')+'/uc721145i_pfl.fits')[1].data[5:-5,5:-5]
    
    xs = 8
    fig = plt.figure(figsize=(xs,xs/3.), dpi=100)
    fig.subplots_adjust(wspace=0.01,hspace=0.01,left=0.01, bottom=0.01,right=0.99,top=0.99)        
    
    vmin, vmax = 0.95, 1.05
    ### put scale within the box
    NX = 100
    y0, y1 = 1014-1.5*NX, 1014-1*NX
    y0 -= NX; y1 -= NX
    
    ### F140W flat
    ax = fig.add_subplot(131)
    ax.imshow(f140, vmin=0.95, vmax=1.05, interpolation='nearest')
    ax.text(50,950, 'F140W', verticalalignment='top', fontsize=14, backgroundcolor='white')
    ax.set_xlim(0,1014)
    ax.set_ylim(0,1014)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    
    ### F105W/F140W, with label
    ratio = f105/f140
    x0 = 300
    ratio[y0:y1,x0-2.5*NX:x0-1.5*NX] = vmin
    ratio[y0:y1,x0-1.5*NX:x0-0.5*NX] = (vmin+1)/2.
    ratio[y0:y1,x0-0.5*NX:x0+0.5*NX] = 1.
    ratio[y0:y1,x0+0.5*NX:x0+1.5*NX] = (vmax+1)/2.
    ratio[y0:y1,x0+1.5*NX:x0+2.5*NX] = vmax
    xbox = np.array([0,1,1,0,0])*NX
    ybox = np.array([0,0,1,1,0])*NX/2
    
    ax = fig.add_subplot(132)
    ax.imshow(ratio, vmin=0.95, vmax=1.05, interpolation='nearest')
    ax.plot(xbox+x0-0.5*NX, ybox+y1-0.5*NX, color='0.6', alpha=0.1)
    
    fs = 9
    ax.text(x0-2*NX, y0-0.5*NX, '%.2f' %(vmin), horizontalalignment='center', verticalalignment='center', fontsize=fs)
    ax.text(x0-0*NX, y0-0.5*NX, '%.2f' %(1), horizontalalignment='center', verticalalignment='center', fontsize=fs)
    ax.text(x0+2*NX, y0-0.5*NX, '%.2f' %(vmax), horizontalalignment='center', verticalalignment='center', fontsize=fs)

    ax.text(50,950, 'F105W / F140W', verticalalignment='top', fontsize=14)
    ax.set_xlim(0,1014)
    ax.set_ylim(0,1014)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
        
    ### F160W/F140W
    ax = fig.add_subplot(133)
    ax.imshow(f160/f140, vmin=0.95, vmax=1.05, interpolation='nearest')
    ax.text(50,950, 'F160W / F140W', verticalalignment='top', fontsize=14)
    ax.set_xlim(0,1014)
    ax.set_ylim(0,1014)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    
    fig.savefig('compare_flats.pdf')
    