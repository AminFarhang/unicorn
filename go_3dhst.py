"""
DEPRECATED by new Interlaced reductions....

Run the full reduction scripts.

> Make the tarfiles for the web outputs:

dirs="SN-MARSHALL SN-GEORGE GOODS-S AEGIS COSMOS GOODS-N" 
for dir in ${dirs}; do 
    cd ${THREEDHST}
    cd ${dir}
    echo ${PWD}
    rm HTML/images/*tar.gz
    make_3dhst_tarfiles.sh
done

dirs="SN-MARSHALL SN-GEORGE GOODS-S AEGIS COSMOS GOODS-N" 
for dir in ${dirs}; do 
    cd ${THREEDHST}/${dir}
    echo ${dir}
    # ls -l HTML/images/*tar.gz
    # mv HTML/images/*tar.gz ~/Sites_GLOBAL/P/GRISM_v1.6/tarfiles/
    cp HTML/ascii/*tar.gz ~/Sites_GLOBAL/P/GRISM_v1.6/tarfiles/
done

"""
import threedhst
import unicorn
import glob
import os
import shutil

def redo_all_SED_plots():
    import glob
    import threedhst

    for dir in ['COSMOS','GOODS-N','AEGIS','SN-PRIMO','SN-GEORGE'][1:]:
        os.chdir(unicorn.GRISM_HOME+dir+'/DATA/')
        files=glob.glob('*G141_asn.fits')
        os.chdir('../')
        for file in files:
            print file.split('_asn')[0]
            unicorn.analysis.make_SED_plots(grism_root=file.split('_asn')[0])
            
def UDF():
    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis
    
    os.chdir(unicorn.GRISM_HOME+'UDF')
    
    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')

    files = []
    files.extend(glob.glob('UDF-*F140W_tweak.fits'))
    files.extend(glob.glob('UDF-*G141_shifts.txt'))
    files.extend(glob.glob('UDF-*G141_asn.fits'))

    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')
    os.chdir('../')
    
    ### UDF
    go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=25)
    
    #### Run various test combinations (Nov 9, 2011)
    files = glob.glob('PREP_FLT/UDF*F140W_drz.fits')
    for file in files:
        threedhst.options['PREFAB_DIRECT_IMAGE'] = '../'+file
        proc.reduction_script(asn_grism_file= os.path.basename(file).replace('F140W_drz', 'G141_asn'))
        unicorn.analysis.make_SED_plots(grism_root=os.path.basename(file).replace('F140W_drz.fits','G141'))
        go.clean_up()
        
    #threedhst.options['OTHER_BANDS'] = [['../PREP_FLT/udf-candels-f125w.fits', 'F125W' , 1248.6, 26.25], ['../PREP_FLT/udf-candels-f160w.fits', 'F160W' , 1537.6, 25.96]]
    
    #### Use a detection image that has the candels imaging filling in the perimeter
    #### of the 3D-HST pointing
    
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/UDF-fill-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='UDF-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='UDF-G141')
    go.clean_up()
    
    # #### Test with fluxcube
    # go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=25.5)
    # 
    # CANDELS='/3DHST/Ancillary/GOODS-S/CANDELS/'
    # 
    # threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/UDF-F140W_drz.fits'
    # threedhst.options['OTHER_BANDS'] = [[CANDELS+'hlsp_candels_hst_wfc3_gsd01_f125w_v0.5_drz.fits', 'F125W' , 1248.6, 26.25], [CANDELS+'hlsp_candels_hst_wfc3_gsd01_f160w_v0.5_drz.fits', 'F160W' , 1537.6, 25.96]]
    # 
    # proc.reduction_script(asn_grism_file='UDF-FC-G141_asn.fits')
    # unicorn.analysis.make_SED_plots(grism_root='UDF-FC-G141')
    # go.clean_up()
    
def goods_s():
    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis
    
    os.chdir(unicorn.GRISM_HOME+'GOODS-S')
    
    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')
    grism_asn  = glob.glob('GOODS-S-[0-9]*-G141_asn.fits')
    files=glob.glob('GOODS-S-[0-9]*-G141_shifts.txt')
    files.extend(grism_asn)
    files.extend(glob.glob('GOODS-S-[0-9]*-F140W_tweak.fits'))
    
    files.extend(glob.glob('UDF-*F140W_tweak.fits'))
    files.extend(glob.glob('UDF-*G141_shifts.txt'))
    files.extend(glob.glob('UDF-*G141_asn.fits'))

    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')
    os.chdir('../')
    
    #### Initialize parameters
    go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=25.5)
    
    #### Main loop for reduction
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/GOODS-S-6-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='GOODS-S-6-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='GOODS-S-6-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/GOODS-S-27-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='GOODS-S-27-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='GOODS-S-27-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/GOODS-S-24-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='GOODS-S-24-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='GOODS-S-24-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/GOODS-S-28-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='GOODS-S-28-G141_asn.fits')
    #### HUDF09, doesn't overlap with FIREWORKS
    # unicorn.analysis.make_SED_plots(grism_root='GOODS-S-27-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/GOODS-S-23-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='GOODS-S-23-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='GOODS-S-23-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/GOODS-S-26-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='GOODS-S-26-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='GOODS-S-26-G141')
    go.clean_up()
    
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/GOODS-S-34-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='GOODS-S-34-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='GOODS-S-34-G141')
    go.clean_up()
    
    # go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=20.5)
    # 
    # threedhst.options['AXE_EDGES'] = "0,0,0,0"
    # 
    # threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/GOODS-S-6-F140W_drz.fits'
    # proc.reduction_script(asn_grism_file='GOODS-S-6-G141_asn.fits')
    # unicorn.analysis.make_SED_plots(grism_root='GOODS-S-6-G141')
    # go.clean_up()
    # 
    # os.chdir('./DATA')
    # threedhst.gmap.makeImageMap(['GOODS-S-6-G141_drz.fits', 'GOODS-S-6-G141CONT_drz.fits'][0:], aper_list=[14,15,16], polyregions=glob.glob("GOODS-S-*-F140W_asn.pointing.reg"))
    # os.chdir('../')
    
def aegis():
    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    
    import unicorn.analysis
    
    # ######################## Test!
    # go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=21)
    # 
    # threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-11-F140W_drz.fits'
    # # threedhst.options['PREFAB_GRISM_IMAGE'] = '../PREP_FLT/AEGIS-11-G141_drz.fits'
    # proc.reduction_script(asn_grism_file='AEGIS-11-G141_asn.fits')
    # ########################
    
    os.chdir(unicorn.GRISM_HOME+'AEGIS')
    
    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')
    grism_asn  = glob.glob('AEGIS-[0-9]*-G141_asn.fits')
    files=glob.glob('AEGIS-[0-9]*-G141_shifts.txt')
    files.extend(grism_asn)
    files.extend(glob.glob('AEGIS-[0-9]*-F140W_tweak.fits'))
    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')
    os.chdir('../')
    
    #### Initialize parameters
    go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=25.5)
    
    #### Main loop for reduction
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-4-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-4-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-4-G141')
    go.clean_up()
    
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-5-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-5-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-5-G141')
    go.clean_up()
    
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-11-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-11-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-11-G141')
    go.clean_up()
 
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-2-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-2-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-2-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-1-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-1-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-1-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-3-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-3-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-3-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-9-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-9-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-9-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-12-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-12-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-12-G141')
    go.clean_up()
    
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-15-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-15-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-15-G141')
    go.clean_up()
    
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-25-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-25-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-25-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-14-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-14-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-14-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-28-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-28-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-28-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-6-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-6-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-6-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/AEGIS-7-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='AEGIS-7-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='AEGIS-7-G141')
    go.clean_up()

    
def cosmos():
    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis
    
    os.chdir(unicorn.GRISM_HOME+'COSMOS')
    
    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')
    grism_asn  = glob.glob('COSMOS-[0-9]*-G141_asn.fits')
    files=glob.glob('COSMOS-[0-9]*-G141_shifts.txt')
    files.extend(grism_asn)
    files.extend(glob.glob('COSMOS-[0-9]*-F140W_tweak.fits'))
    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')
    
    os.chdir('../')
    
    #### Initialize parameters
    go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=25.5)
    
    #threedhst.options['DRZRESOLA'] = '100.0'
    
    grism_asn = grism_asn
    
    #### Main loop for reduction
    for i in range(len(grism_asn))[0:]:
        asn = grism_asn[i]
        threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/' +  asn.replace('G141_asn','F140W_drz')
        # threedhst.options['PIXFRAC'] = 0.8
        # threedhst.options['DRZRESOLA'] = '35'
        # threedhst.options['DRZSCALE'] = '0.10'
        #### Images for a better fluxcube
        root=asn.replace('_asn.fits','')
        threedhst.options['OTHER_BANDS'] = []
        # for wave in [1.1e4,1.25e4,1.6e4]:
        #     out = unicorn.analysis.make_fluximage(grism_root=root,
        #                wavelength=wave)
        #     threedhst.options['OTHER_BANDS'].append([os.path.basename(out), 'F%03dW' %(wave/100), wave/10., 26.46])
        proc.reduction_script(asn_grism_file=asn)
        unicorn.analysis.make_SED_plots(grism_root=asn.split('_asn.fits')[0])
        go.clean_up()

def goodsn():
    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis
    
    os.chdir(unicorn.GRISM_HOME+'GOODS-N')
    
    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')
    grism_asn  = glob.glob('GOODS-N-[0-9]*-G141_asn.fits')
    files=glob.glob('GOODS-N-[0-9]*-G141_shifts.txt')
    files.extend(grism_asn)
    files.extend(glob.glob('GOODS-N-[0-9]*-F140W_tweak.fits'))
    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')
    os.chdir('../')
    
    #### Initialize parameters
    go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=25)
            
    #### Main loop for reduction
    for i in range(len(grism_asn)):
        asn=grism_asn[i]
        threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/' +  asn.replace('G141_asn','F140W_drz')
        proc.reduction_script(asn_grism_file=asn)
        unicorn.analysis.make_SED_plots(grism_root=asn.split('_asn.fits')[0])
        go.clean_up()
   
#
def sn_primo():
    from pyraf import iraf

    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis
    
    os.chdir(unicorn.GRISM_HOME+'SN-PRIMO')
    
    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')
    grism_asn  = glob.glob('PRIMO-1???-G141_asn.fits')
    files=glob.glob('PRIMO-1???-G141_shifts.txt')
    files.extend(grism_asn)
    files.append('PRIMO-1026-F160W_tweak.fits')
    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')
    
    try:
        iraf.imcopy('/Users/gbrammer/CANDELS/GOODS-S/PREP_FLT/PRIMO-F125W_drz.fits[1]', '../DATA/f125w.fits')
    except:
        os.remove('../DATA/f125w.fits')
        iraf.imcopy('/Users/gbrammer/CANDELS/GOODS-S/PREP_FLT/PRIMO-F125W_drz.fits[1]', '../DATA/f125w.fits')
    
    os.chdir('../')
    
    #### Initialize parameters
    go.set_parameters(direct='F160W', LIMITING_MAGNITUDE=26)
    
    #### Main loop for reduction
    for i, asn in enumerate(grism_asn):
        threedhst.options['PREFAB_DIRECT_IMAGE'] = '/Users/gbrammer/CANDELS/GOODS-S/PREP_FLT/PRIMO-F160W_drz.fits'
        threedhst.options['OTHER_BANDS'] = [['f125w.fits', 'F125W' , 1248.6, 26.25]]
        proc.reduction_script(asn_grism_file=asn)
        unicorn.analysis.make_SED_plots(grism_root=asn.split('_asn.fits')[0])
        go.clean_up()
#
def sn_tile41():
    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis
    
    os.chdir(unicorn.GRISM_HOME+'SN-TILE41')
    
    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')
    grism_asn  = glob.glob('TILE41*-G1*_asn.fits')
    files=glob.glob('TILE41*-G1*_shifts.txt')
    files.extend(grism_asn)
    files.extend(glob.glob('TILE41*tweak.fits'))
    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')
        
    os.chdir('../')
    
    #### Initialize parameters
    go.set_parameters(direct='F160W', LIMITING_MAGNITUDE=23)
    
    #### Main loop for reduction
    for i, asn in enumerate(grism_asn):
        threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/TILE41-F160W_drz.fits'
        threedhst.options['OTHER_BANDS'] = [['TILE41-F105W_sci.fits', 'F105W' , 1055.2, 26.27], ['TILE41-F125W_sci.fits', 'F125W' , 1248.6, 26.25]]
        proc.reduction_script(asn_grism_file=asn)
        #unicorn.analysis.make_SED_plots(grism_root=asn.split('_asn.fits')[0])
        go.clean_up()

def uds():
    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis
    
    os.chdir(unicorn.GRISM_HOME+'UDS')
    
    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')
    grism_asn  = glob.glob('UDS-[0-9]*-G141_asn.fits')
    files=glob.glob('UDS-[0-9]*-G141_shifts.txt')
    files.extend(grism_asn)
    files.extend(glob.glob('UDS-[0-9]*-F140W_tweak.fits'))
    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')
    os.chdir('../')
    
    #### Initialize parameters
    go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=23.5)
    
    #### Main loop for reduction
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/UDS-5-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='UDS-5-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='UDS-5-G141')
    go.clean_up()

    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/UDS-23-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='UDS-23-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='UDS-23-G141')
    go.clean_up()

    go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=26)
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/UDS-18-F140W_drz.fits'
    proc.reduction_script(asn_grism_file='UDS-18-G141_asn.fits')
    unicorn.analysis.make_SED_plots(grism_root='UDS-18-G141')
    go.clean_up()

def goods_ers():
    """

    """
    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis
    
    os.chdir(unicorn.GRISM_HOME+'ERS')
    
    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')
    grism_asn  = glob.glob('WFC3*-G1??_asn.fits')
    files=glob.glob('WFC3*-G1??_shifts.txt')
    files.extend(grism_asn)
    files.extend(glob.glob('WFC3*tweak.fits'))
    for file in files:
        status = os.system('cp '+file+' ../DATA')
    
    # try:
    #     iraf.imcopy('GEORGE-F125W_drz.fits[1]', '../DATA/f125w.fits')
    # except:
    #     os.remove('f125w.fits')
    #     iraf.imcopy('GEORGE-F125W_drz.fits[1]', '../DATA/f125w.fits')
    
    os.chdir('../')
    
    #### Initialize parameters
    go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=25.5)
    
    #### Run aXe
    asn = 'WFC3-ERSII-G01-G141_asn.fits'
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/WFC3-ERSII-G01-F140W_drz.fits'
    #threedhst.options['OTHER_BANDS'] = [['f125w.fits', 'F125W' , 1248.6, 26.25]]
    proc.reduction_script(asn_grism_file=asn)
    unicorn.analysis.make_SED_plots(grism_root=asn.split('_asn.fits')[0])
    go.clean_up()

def sn_george():
    """

    """
    from pyraf import iraf

    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis
    
    os.chdir(unicorn.GRISM_HOME+'SN-GEORGE')
    
    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')
    grism_asn  = glob.glob('GEORGE-G141_asn.fits')
    files=glob.glob('GEORGE-G141_shifts.txt')
    files.extend(grism_asn)
    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')
    
    try:
        iraf.imcopy('GEORGE-F125W_drz.fits[1]', '../DATA/f125w.fits')
    except:
        os.remove('../DATA/f125w.fits')
        iraf.imcopy('GEORGE-F125W_drz.fits[1]', '../DATA/f125w.fits')
    
    os.chdir('../')
    
    #### Initialize parameters
    go.set_parameters(direct='F160W', LIMITING_MAGNITUDE=26)
    
    #### Run aXe
    asn = 'GEORGE-G141_asn.fits'
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/GEORGE-F160W_drz.fits'
    threedhst.options['OTHER_BANDS'] = [['f125w.fits', 'F125W' , 1248.6, 26.25]]
    proc.reduction_script(asn_grism_file=asn)
    unicorn.analysis.make_SED_plots(grism_root=asn.split('_asn.fits')[0])
    go.clean_up()

def sn_marshall():
    """

    """
    from pyraf import iraf

    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis

    os.chdir(unicorn.GRISM_HOME+'SN-MARSHALL')

    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')
    grism_asn  = glob.glob('MARSHALL-2??-G141_asn.fits')
    files=glob.glob('MARSHALL-2*-G141_shifts.txt')
    files.extend(grism_asn)
    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')

    try:
        iraf.imcopy('MARSHALL-F125W_drz.fits[1]', '../DATA/f125w_sci.fits')
    except:
        os.remove('../DATA/f125w_sci.fits')
        iraf.imcopy('MARSHALL-F125W_drz.fits[1]', '../DATA/f125w_sci.fits')
    
    os.chdir('../')

    #### Initialize parameters
    go.set_parameters(direct='F160W', LIMITING_MAGNITUDE=26)
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/MARSHALL-F160W_drz.fits'
    threedhst.options['OTHER_BANDS'] = [['f125w_sci.fits', 'F125W' , 1248.6, 26.25]]

    #### Main loop for reduction
    for i in range(len(grism_asn)):
        asn = grism_asn[i]
        proc.reduction_script(asn_grism_file=asn)
        unicorn.analysis.make_SED_plots(grism_root=asn.split('_asn.fits')[0])
        go.clean_up()
    
#
def daddi():
    """

    """
    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis

    os.chdir(unicorn.GRISM_HOME+'DADDI')

    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')
    grism_asn  = glob.glob('HIGHZ-CLUSTER-?-G141_asn.fits')
    files=glob.glob('HIGHZ-CLUSTER-?-G141_shifts.txt')
    files.extend(grism_asn)
    files.extend(glob.glob('*tweak.fits'))
    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')

    os.chdir('../')

    #### Initialize parameters
    go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=24.5)
    threedhst.options['OTHER_BANDS'] = []

    #### Main loop for reduction
    for i in range(len(grism_asn)):
        asn = grism_asn[i]
        threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/'+asn.replace('asn','drz').replace('G141', 'F140W')
        proc.reduction_script(asn_grism_file=asn)
        #unicorn.analysis.make_SED_plots(grism_root=asn.split('_asn.fits')[0])
        go.clean_up()

def stanford():
    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis
    
    os.chdir(unicorn.GRISM_HOME+'STANFORD')
    
    #### Copy necessary files from PREP_FLT to DATA
    os.chdir('PREP_FLT')
    grism_asn  = glob.glob('ISCS*G141_asn.fits')
    files=glob.glob('ISCS*G141_shifts.txt')
    files.extend(grism_asn)
    files.extend(glob.glob('ISCS*F160W_tweak.fits'))
    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')
    os.chdir('../')
    
    #### Initialize parameters
    go.set_parameters(direct='F160W', LIMITING_MAGNITUDE=23)
    
    #### Main loop for reduction
    # threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/ISCSJ1425.3+3250-F160W_drz.fits'
    # proc.reduction_script(asn_grism_file='ISCSJ1425.3+3250-G141_asn.fits')
    # go.clean_up()
    # 
    # threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/ISCSJ1426.5+3339-F160W_drz.fits'
    # proc.reduction_script(asn_grism_file='ISCSJ1426.5+3339-G141_asn.fits')
    # go.clean_up()
    
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/ISCSJ1429.2+3357-F160W_drz.fits'
    proc.reduction_script(asn_grism_file='ISCSJ1429.2+3357-G141_asn.fits')
    go.clean_up()
    
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/ISCSJ1429.3+3437-F160W_drz.fits'
    proc.reduction_script(asn_grism_file='ISCSJ1429.3+3437-G141_asn.fits')
    go.clean_up()
    
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/ISCSJ1431.1+3459-F160W_drz.fits'
    proc.reduction_script(asn_grism_file='ISCSJ1431.1+3459-G141_asn.fits')
    go.clean_up()
    
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/ISCSJ1432.4+3250-F160W_drz.fits'
    proc.reduction_script(asn_grism_file='ISCSJ1432.4+3250-G141_asn.fits')
    go.clean_up()
    
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/ISCSJ1434.5+3427-F160W_drz.fits'
    proc.reduction_script(asn_grism_file='ISCSJ1434.5+3427-G141_asn.fits')
    go.clean_up()
    
#
def GN20():
    from threedhst.prep_flt_files import process_3dhst_pair as pair
    import threedhst.prep_flt_files
    import glob
    import os
    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis
    
    os.chdir(unicorn.GRISM_HOME+'GOODS-N/PREP_FLT')
    
    #### Make detection image  
    direct_files = glob.glob('GOODS-N-18-F140W_asn.fits')
    threedhst.utils.combine_asn_shifts(direct_files, out_root='GN20-F140W',
                       path_to_FLT='./', run_multidrizzle=False)

    #
    direct_files = glob.glob('GOODS-N-18-G141_asn.fits')
    threedhst.utils.combine_asn_shifts(direct_files, out_root='GN20-G141',
                       path_to_FLT='./', run_multidrizzle=False)
    
    SCALE = 0.06
    threedhst.prep_flt_files.startMultidrizzle('GN20-F140W_asn.fits',
             use_shiftfile=True, skysub=False,
             final_scale=SCALE, pixfrac=0.6, driz_cr=False,
             updatewcs=False, clean=True, median=False,
             ra=189.30047, dec=62.368959, final_outnx = 960, final_outny = 800) #,
    
    #### Copy necessary files from PREP_FLT to DATA
    grism_asn  = glob.glob('GN20-G141_asn.fits')
    files=glob.glob('GN20-G141_shifts.txt')
    files.extend(grism_asn)
    files.extend(glob.glob('GN20-F140W_tweak.fits'))
    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')
    os.chdir('../')
    
    #### Initialize parameters
    go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=27.5)
            
    #### Main loop for reduction
    asn='GN20-G141_asn.fits'
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/GN20-F140W_drz.fits'
    proc.reduction_script(asn_grism_file=asn)
    unicorn.analysis.make_SED_plots(grism_root=asn.split('_asn.fits')[0])
    go.clean_up()
    

def GOODS_SMG():
    from threedhst.prep_flt_files import process_3dhst_pair as pair
    import threedhst.prep_flt_files
    import glob
    import os
    import unicorn.go_3dhst as go
    import threedhst.process_grism as proc
    import unicorn.analysis
    
    os.chdir(unicorn.GRISM_HOME+'GOODS-N/PREP_FLT')
    
    #### Make detection image  
    direct_files = glob.glob('GOODS-N-34-F140W_asn.fits')
    threedhst.utils.combine_asn_shifts(direct_files, out_root='G850.1-F140W',
                       path_to_FLT='./', run_multidrizzle=False)

    #
    direct_files = glob.glob('GOODS-N-34-G141_asn.fits')
    threedhst.utils.combine_asn_shifts(direct_files, out_root='G850.1-G141',
                       path_to_FLT='./', run_multidrizzle=False)
    
    SCALE = 0.06
    threedhst.prep_flt_files.startMultidrizzle('G850.1-F140W_asn.fits',
             use_shiftfile=True, skysub=False,
             final_scale=SCALE, pixfrac=0.6, driz_cr=False,
             updatewcs=False, clean=True, median=False,
             ra=189.21663, dec=62.207175, final_outnx = 1960, final_outny = 1800) #,
    
    #### Copy necessary files from PREP_FLT to DATA
    grism_asn  = glob.glob('G850.1-G141_asn.fits')
    files=glob.glob('G850.1-G141_shifts.txt')
    files.extend(grism_asn)
    files.extend(glob.glob('G850.1-F140W_tweak.fits'))
    for file in files:
        status = os.system('cp '+file+' ../DATA')
        #shutil.copy(file, '../DATA')
    os.chdir('../')
    
    #### Initialize parameters
    import unicorn.go_3dhst as go
    import unicorn
    os.chdir(unicorn.GRISM_HOME+'GOODS-N')
    import threedhst.process_grism as proc
    import threedhst
    import unicorn.analysis
    go.set_parameters(direct='F140W', LIMITING_MAGNITUDE=25)
    threedhst.options['AXE_EDGES'] = "180,0,0,0"
    threedhst.options['USE_TAXE'] = True
    
    threedhst.plotting.USE_PLOT_GUI = False
    #### Main loop for reduction
    asn='G850.1-G141_asn.fits'
    threedhst.options['PREFAB_DIRECT_IMAGE'] = '../PREP_FLT/G850.1-F140W_drz.fits'
    proc.reduction_script(asn_grism_file=asn)
    unicorn.analysis.make_SED_plots(grism_root=asn.split('_asn.fits')[0])
    go.clean_up()

def clean_3dhst_files(root='G850.1-G141'):
    """
    Remove files from DATA, DRIZZLE_G141, and HTML
    """
    files=[]
    files.extend(glob.glob('./DATA/'+root+'*'))
    files.extend(glob.glob('DRIZZLE_G141/'+root+'*'))
    files.extend(glob.glob('HTML/'+root+'*'))
    files.extend(glob.glob('HTML/images/'+root+'*'))
    files.extend(glob.glob('HTML/ascii/'+root+'*'))
    files.extend(glob.glob('HTML/tiles/'+root+'*'))
    files.extend(glob.glob('HTML/SED/'+root+'*'))
    
    fp = open('/tmp/clean_3dhst_files.list','w')
    for file in files:
        fp.write('rm %s\n' %(file))
    fp.close()
    
    print '!sh /tmp/clean_3dhst_files.list'
    
def set_parameters(direct='F140W', LIMITING_MAGNITUDE=25):
    
    #threedhst.sex.USE_CONVFILE = 'gauss_2.0_5x5.conv'
    threedhst.sex.USE_CONVFILE = 'gauss_4.0_7x7.conv'
    print '\nSExtractor convolution kernel: %s' %threedhst.sex.USE_CONVFILE
    
    threedhst.defaultOptions()
    
    threedhst.options['DETECT_THRESH'] = 1.4
    threedhst.options['ANALYSIS_THRESH'] = 1.4
    threedhst.options['LIMITING_MAGNITUDE'] = LIMITING_MAGNITUDE

    threedhst.options['FULL_EXTRACTION_GEOMETRY'] = False

    #### Already processed background and shifts
    threedhst.options['OTHER_BANDS'] = []
    threedhst.options['PATH_TO_RAW'] = '../PREP_FLT/'
    threedhst.options['SKY_BACKGROUND'] = None
    threedhst.options['MAKE_SHIFTFILES'] = False
    threedhst.options['ALIGN_IMAGE'] = None

    threedhst.options['DRZRESOLA'] = '22.0'
    threedhst.options['PIXFRAC'] = '0.8'
    threedhst.options['DRZSCALE'] = '0.06'

    threedhst.options['AXE_EDGES'] = "90,0,0,0"
    threedhst.options['USE_TAXE'] = True

    #### Use F140W as detection image
    threedhst.options['MAG_ZEROPOINT'] = 26.46
    threedhst.options['FILTWAVE'] = 1392.
        
    #### Use F125W as detection image
    if direct == 'F125W':
        threedhst.options['MAG_ZEROPOINT'] = 26.25
        threedhst.options['FILTWAVE'] = 1248.6
    
    #### Use F160W as detection image
    if direct == 'F160W':
        threedhst.options['MAG_ZEROPOINT'] = 25.96
        threedhst.options['FILTWAVE'] = 1537.
    
    #### Use F814W as detection image
    if direct == 'F814W':
        threedhst.options['MAG_ZEROPOINT'] = 25.943333
        threedhst.options['FILTWAVE'] = 805.6948
        threedhst.options['DRZRESOLA'] = '40.0'
        threedhst.options['PIXFRAC'] = '1.0'
        threedhst.options['DRZSCALE'] = '0.05'
        threedhst.options['AXE_EDGES'] = "0,0,0,0"
        
def clean_up():
    files=glob.glob('OUTPUT_G141/*')
    files.extend(glob.glob('DATA/*FLX*'))
    files.extend(glob.glob('PREP_FLT/*FLX*'))
    files.extend(glob.glob('DRIZZLE_G141/*mef*'))
    files.extend(glob.glob('DRIZZLE_G141/*PET*'))
    files.extend(glob.glob('DATA/threedhst_auto*swarp'))
    files.extend(glob.glob('DATA/*coeffs?.dat'))
    files.extend(glob.glob('HTML/ascii/*.FITS'))

    for file in files:
        os.remove(file)
       
#
def go_update_all_catalogs():
    import glob
    import threedhst
    import unicorn
    
    for dir in ['COSMOS','GOODS-N','AEGIS','GOODS-S','SN-MARSHALL','SN-GEORGE']:
        os.chdir(unicorn.GRISM_HOME+'/'+dir+'/DATA/')
        files=glob.glob('*G141_asn.fits')
        os.chdir('../')
        for file in files:
            print file.split('_asn')[0]
            try:
                threedhst.process_grism.update_catalogs(root=file.split('_asn')[0], 
                    CONT_LAM=1.4e4)
            except:
                pass