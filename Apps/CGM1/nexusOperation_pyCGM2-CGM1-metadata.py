# -*- coding: utf-8 -*-
import logging
import pdb
import os
import json
import argparse
import cPickle
import numpy as np

import pyCGM2
pyCGM2.CONFIG.setLoggingLevel(logging.DEBUG)


import ViconNexus
import btk


from pyCGM2.Tools import btkTools


def getViconMP(model):

    out= dict()

    th_l = 0 if np.abs(model.getViconThighOffset("Left")) < 0.000001 else model.getViconThighOffset("Left")
    sh_l = 0 if np.abs(model.getViconShankOffset("Left"))< 0.000001 else model.getViconShankOffset("Left")
    tt_l = 0 if np.abs(model.getViconTibialTorsion("Left")) < 0.000001 else model.getViconTibialTorsion("Left")

    th_r = 0 if np.abs(model.getViconThighOffset("Right")) < 0.000001 else model.getViconThighOffset("Right")
    sh_r = 0 if np.abs(model.getViconShankOffset("Right")) < 0.000001 else model.getViconShankOffset("Right")
    tt_r = 0 if np.abs(model.getViconTibialTorsion("Right")) < 0.000001 else model.getViconTibialTorsion("Right")

    spf_l,sro_l = model.getViconFootOffset("Left")
    spf_r,sro_r = model.getViconFootOffset("Right")

    abdAdd_l = 0 if np.abs(model.getViconAnkleAbAddOffset("Left")) < 0.000001 else model.getViconAnkleAbAddOffset("Left") 
    abdAdd_r = 0 if np.abs(model.getViconAnkleAbAddOffset("Right")) < 0.000001 else model.getViconAnkleAbAddOffset("Right")

    out["InterAsisDistance"]  = model.mp_computed["InterAsisDistance"]
    out["LeftAsisTrocanterDistance"]  = model.mp_computed["LeftAsisTrocanterDistance"]
    out["LeftThighRotation"]  = th_l
    out["LeftShankRotation"]  = sh_l
    out["LeftTibialTorsion"]  = tt_l

    out["RightAsisTrocanterDistance"]  = model.mp_computed["RightAsisTrocanterDistance"]
    out["RightThighRotation"]  = th_r
    out["RightShankRotation"]  = sh_r
    out["RightTibialTorsion"]  = tt_r


    out["LeftStaticPlantFlex"]  = spf_l
    out["LeftStaticRotOff"]  = sro_l
    out["LeftAnkleAbAdd"]  = abdAdd_l

    out["RightStaticPlantFlex"]  = spf_r
    out["RightStaticRotOff"]  = sro_r
    out["RightAnkleAbAdd"]  = abdAdd_r

    return out

if __name__ == "__main__":

    DEBUG = False

    pyNEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = pyNEXUS.Client.IsConnected()


    parser = argparse.ArgumentParser(description='CGM1')
    parser.add_argument('-c','--calibration', action='store_true', help='Calibration')
    parser.add_argument('-f','--fitting', action='store_true', help='Fitting')
    args = parser.parse_args()
    
    if NEXUS_PYTHON_CONNECTED: # run Operation

        # --------------------------INPUTS ------------------------------------

        # ----- trial -----
        if DEBUG:
            DATA_PATH = "C:\\Users\\AAA34169\\Documents\\VICON DATA\\pyCGM2-Data\\CGM1\\CGM1-NexusPlugin\\CGM1-Calibration\\"
            filenameNoExt = "static Cal 01-noKAD-noAnkleMed" 
            pyNEXUS.OpenTrial( str(DATA_PATH+filenameNoExt), 30 )

        else:
            DATA_PATH, filenameNoExt = pyNEXUS.GetTrialName()

        # ----- inputs -----
        if args.calibration:
            if not os.path.isfile(DATA_PATH + "pyCGM2.model"):
                raise Exception ("pyCGM2.model file doesn't exist. Run Calibration operation")
            else:
                f = open(DATA_PATH + 'pyCGM2.model', 'r')
                model = cPickle.load(f)
                f.close()
    
            if not os.path.isfile(DATA_PATH + "pyCGM2.inputs"): #DATA_PATH + "pyCGM2.inputs"):
                raise Exception ("pyCGM2.inputs file doesn't exist")
            else:
                inputs = json.loads(open(DATA_PATH + 'pyCGM2.inputs').read())

        filename = filenameNoExt+".c3d"

        # ---------------METADATA PROCESSING-----------------------------------
        acq= btkTools.smartReader(str(DATA_PATH + filename))
        
        md=acq.GetMetaData() # main metadata levekl
        md_Model = btkTools.hasChild(md,"MODEL") # find MODEL level
                
        # create or update MODEL section        
        if md_Model is not None: 
            logging.debug( "[pyCGM2] : MODEL section exits within metadata")
            md_Model.ClearChildren()
            btk.btkMetaDataCreateChild(md_Model, "NAME", "CGM1")
            btk.btkMetaDataCreateChild(md_Model, "PROCESSOR", "pyCGM2")
            if args.calibration:

                for item in inputs["Calibration"].items():
                    print item
                    btk.btkMetaDataCreateChild(md_Model, str(item[0]), str(item[1]))
                    
                mps = getViconMP(model)
                for item in mps.items():
                    btk.btkMetaDataCreateChild(md_Model, str(item[0]), str(item[1]))
                    

        else: 
            logging.warning( "[pyCGM2] : MODEL section doesn t exist. It will be created")               
            md_Model = btk.btkMetaData('MODEL') # create main metadata
            btk.btkMetaDataCreateChild(md_Model, "NAME", "CGM1")
            btk.btkMetaDataCreateChild(md_Model, "PROCESSOR", "pyCGM2")
            
            if args.calibration:
                for item in inputs["Calibration"].items():
                    print item
                    btk.btkMetaDataCreateChild(md_Model, str(item[0]), str(item[1]))
                
                mps = getViconMP(model)
                for item in mps.items():
                    btk.btkMetaDataCreateChild(md_Model, str(item[0]), str(item[1]))
                    
                
        # add metataData to acq
        acq.GetMetaData().AppendChild(md_Model)

        # save
        btkTools.smartWriter(acq,str(DATA_PATH + filenameNoExt + ".c3d"))
        logging.info( "[pyCGM2] : add Model Metadata in file ( %s) " % (filename))
            
    else:

        raise Exception("NO Nexus connection. Turn on Nexus")