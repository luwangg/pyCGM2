# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 11:09:22 2016

@author: aaa34169

TODO : these cases are lacking :
 - progression Z lateral axis (X or Y)
 - progression X lateral axis Z
 - progression Y lateral axis Z

"""

import numpy as np
import pdb
import logging

import pyCGM2
from pyCGM2 import log; log.setLoggingLevel(logging.INFO)

# pyCGM2
from pyCGM2.Tools import  btkTools,trialTools

# ---- BTK ------

# Gait
class BtkProgressionTest_gaitTrial():

    @classmethod
    def gaitTrialProgressionX_forward_lateralY(cls):
        """
        """
        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"


        gaitFilename="gait_X_forward.c3d"
        acq = btkTools.smartReader(str(MAIN_PATH +  gaitFilename))

        valSACR=(acq.GetPoint("LPSI").GetValues() + acq.GetPoint("RPSI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"SACR",valSACR,desc="")

        valMidAsis=(acq.GetPoint("LASI").GetValues() + acq.GetPoint("RASI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"midASIS",valMidAsis,desc="")

        longitudinalAxis,forwardProgression,globalFrame = btkTools.findProgression(acq,"LASI")

        np.testing.assert_equal( longitudinalAxis,"X")
        np.testing.assert_equal( forwardProgression,True)
        np.testing.assert_equal( globalFrame,"XYZ")



    @classmethod
    def gaitTrialProgressionX_backward_lateralY(cls):
        """

        """
        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"

        gaitFilename="gait_X_backward.c3d"
        acq = btkTools.smartReader(str(MAIN_PATH +  gaitFilename))

        valSACR=(acq.GetPoint("LPSI").GetValues() + acq.GetPoint("RPSI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"SACR",valSACR,desc="")

        valMidAsis=(acq.GetPoint("LASI").GetValues() + acq.GetPoint("RASI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"midASIS",valMidAsis,desc="")


        longitudinalAxis,forwardProgression,globalFrame = btkTools.findProgression(acq,"LASI")

        np.testing.assert_equal( longitudinalAxis,"X")
        np.testing.assert_equal( forwardProgression,False)
        np.testing.assert_equal( globalFrame,"XYZ")

    @classmethod
    def gaitTrialProgressionY_forward_lateralX(cls):
        """
        """
        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"


        gaitFilename="gait_Y_forward.c3d"
        acq = btkTools.smartReader(str(MAIN_PATH +  gaitFilename))

        valSACR=(acq.GetPoint("LPSI").GetValues() + acq.GetPoint("RPSI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"SACR",valSACR,desc="")

        valMidAsis=(acq.GetPoint("LASI").GetValues() + acq.GetPoint("RASI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"midASIS",valMidAsis,desc="")


        validFrames,vff,vlf = btkTools.findValidFrames(acq,["LPSI","LASI","RPSI"])


        longitudinalAxis,forwardProgression,globalFrame = btkTools.findProgression(acq,"LASI")

        np.testing.assert_equal( longitudinalAxis,"Y")
        np.testing.assert_equal( forwardProgression,True)
        np.testing.assert_equal( globalFrame,"YXZ")


    @classmethod
    def gaitTrialProgressionY_backward_lateralX(cls):
        """
        """
        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"


        gaitFilename="gait_Y_backward.c3d"
        acq = btkTools.smartReader(str(MAIN_PATH +  gaitFilename))

        valSACR=(acq.GetPoint("LPSI").GetValues() + acq.GetPoint("RPSI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"SACR",valSACR,desc="")

        valMidAsis=(acq.GetPoint("LASI").GetValues() + acq.GetPoint("RASI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"midASIS",valMidAsis,desc="")


        longitudinalAxis,forwardProgression,globalFrame = btkTools.findProgression(acq,"LASI")

        np.testing.assert_equal( longitudinalAxis,"Y")
        np.testing.assert_equal( forwardProgression,False)
        np.testing.assert_equal( globalFrame,"YXZ")

    @classmethod
    def gaitTrialGarches(cls):
        """
        """
        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"

        translators = {
        		"LASI":"L.ASIS",
        		"RASI":"R.ASIS",
        		"LPSI":"L.PSIS",
        		"RPSI":"R.PSIS",
        		"RTHI":"R.Thigh",
        		"RKNE":"R.Knee",
        		"RTHAP":"R.THAP",
        		"RTHAD":"R.THAD",
        		"RTIB":"R.Shank",
        		"RANK":"R.Ankle",
        		"RTIAP":"R.TIAP",
        		"RTIAD":"R.TIAD",
        		"RHEE":"R.Heel",
        		"RSMH":"R.SMH",
        		"RTOE":"R.Toe",
        		"RFMH":"R.FMH",
        		"RVMH":"R.VMH",
        		"LTHI":"L.Thigh",
        		"LKNE":"L.Knee",
        		"LTHAP":"L.THAP",
        		"LTHAD":"L.THAD",
        		"LTIB":"L.Shank",
        		"LANK":"L.Ankle",
        		"LTIAP":"L.TIAP",
        		"LTIAD":"L.TIAD",
        		"LHEE":"L.Heel",
        		"LSMH":"L.SMH",
        		"LTOE":"L.Toe",
        		"LFMH":"L.FMH",
        		"LVMH":"L.VMH",
        		"RKNM":"R.Knee.Medial",
                "LKNM":"L.Knee.Medial",
                "RMED":"R.Ankle.Medial",
                "LMED":"L.Ankle.Medial"
        		}

        gaitFilename="gait_garches_issue.c3d"

        acq = btkTools.smartReader(str(MAIN_PATH +  gaitFilename),translators =translators )

        valSACR=(acq.GetPoint("RPSI").GetValues() + acq.GetPoint("LPSI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"SACR",valSACR,desc="")

        valMidAsis=(acq.GetPoint("RASI").GetValues() + acq.GetPoint("LASI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"midASIS",valMidAsis,desc="")


        longitudinalAxis,forwardProgression,globalFrame = btkTools.findProgression(acq,"LASI")
        longitudinalAxis2,forwardProgression2,globalFrame2 = btkTools.findProgressionAxisFromPelvicMarkers(acq,["LASI","LPSI","RASI","RPSI"])

        np.testing.assert_equal( longitudinalAxis,"Y")
        np.testing.assert_equal( longitudinalAxis2,"Y")
#--- static
class BtkProgressionTest_static():

    @classmethod
    def gaitTrialProgressionX_forward_lateralY_static(cls):
        """

        """
        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"

        gaitFilename="static_X.c3d"
        acq = btkTools.smartReader(str(MAIN_PATH +  gaitFilename))

        valSACR=(acq.GetPoint("LPSI").GetValues() + acq.GetPoint("RPSI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"SACR",valSACR,desc="")

        valMidAsis=(acq.GetPoint("LASI").GetValues() + acq.GetPoint("RASI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"midASIS",valMidAsis,desc="")


        longitudinalAxis,forwardProgression,globalFrame = btkTools.findProgressionAxisFromPelvicMarkers(acq,["LASI","LPSI","RASI","RPSI"])

        np.testing.assert_equal( longitudinalAxis,"X")
        np.testing.assert_equal( forwardProgression,True)
        np.testing.assert_equal( globalFrame,"XYZ")


    @classmethod
    def gaitTrialProgressionX_backward_lateralY_static(cls):
        """

        """
        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"

        gaitFilename="static_X_backward.c3d"
        acq = btkTools.smartReader(str(MAIN_PATH +  gaitFilename))

        valSACR=(acq.GetPoint("LPSI").GetValues() + acq.GetPoint("RPSI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"SACR",valSACR,desc="")

        valMidAsis=(acq.GetPoint("LASI").GetValues() + acq.GetPoint("RASI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"midASIS",valMidAsis,desc="")


        longitudinalAxis,forwardProgression,globalFrame = btkTools.findProgressionAxisFromPelvicMarkers(acq,["LASI","LPSI","RASI","RPSI"])

        np.testing.assert_equal( longitudinalAxis,"X")
        np.testing.assert_equal( forwardProgression,False)
        np.testing.assert_equal( globalFrame,"XYZ")



    @classmethod
    def gaitTrialProgressionY_backward_lateralX_static(cls):
        """
        """
        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"


        gaitFilename="static_Y_backward.c3d"
        acq = btkTools.smartReader(str(MAIN_PATH +  gaitFilename))

        valSACR=(acq.GetPoint("LPSI").GetValues() + acq.GetPoint("RPSI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"SACR",valSACR,desc="")

        valMidAsis=(acq.GetPoint("LASI").GetValues() + acq.GetPoint("RASI").GetValues()) / 2.0
        btkTools.smartAppendPoint(acq,"midASIS",valMidAsis,desc="")


        longitudinalAxis,forwardProgression,globalFrame = btkTools.findProgressionAxisFromPelvicMarkers(acq,["LASI","LPSI","RASI","RPSI"])

        np.testing.assert_equal( longitudinalAxis,"Y")
        np.testing.assert_equal( forwardProgression,False)
        np.testing.assert_equal( globalFrame,"YXZ")


#---- OPENMA -----

#---gait Trial
class OpenmaProgressionTest_gaitTrial():

    @classmethod
    def gaitTrialProgressionX_forward_lateralY(cls):
        """
        """

        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"


        gaitFilename="gait_X_forward.c3d"

        trial = trialTools.smartTrialReader(MAIN_PATH,gaitFilename)


        longitudinalAxis,forwardProgression,globalFrame = trialTools.findProgression(trial,"LPSI")

        np.testing.assert_equal( longitudinalAxis,"X")
        np.testing.assert_equal( forwardProgression,True)
        np.testing.assert_equal( globalFrame,"XYZ")

        longitudinalAxisFoot,forwardProgressionFoot,globalFrameFoot = trialTools.findProgression(trial,"RHEE")
        np.testing.assert_equal( longitudinalAxisFoot,"X")
        np.testing.assert_equal( forwardProgressionFoot,True)
        np.testing.assert_equal( globalFrameFoot,"XYZ")

    @classmethod
    def gaitTrialProgressionX_backward_lateralY(cls):
        """

        """
        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"

        gaitFilename="gait_X_backward.c3d"

        trial = trialTools.smartTrialReader(MAIN_PATH,gaitFilename)
        longitudinalAxis,forwardProgression,globalFrame = trialTools.findProgression(trial,"LPSI")

        np.testing.assert_equal( longitudinalAxis,"X")
        np.testing.assert_equal( forwardProgression,False)
        np.testing.assert_equal( globalFrame,"XYZ")

        longitudinalAxisFoot,forwardProgressionFoot,globalFrameFoot = trialTools.findProgression(trial,"RHEE")


        np.testing.assert_equal( longitudinalAxisFoot,"X")
        np.testing.assert_equal( forwardProgressionFoot,False)
        np.testing.assert_equal( globalFrameFoot,"XYZ")

    @classmethod
    def gaitTrialProgressionY_forward_lateralX(cls):
        """
        """
        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"


        gaitFilename="gait_Y_forward.c3d"
        trial = trialTools.smartTrialReader(MAIN_PATH,gaitFilename)
        longitudinalAxis,forwardProgression,globalFrame = trialTools.findProgression(trial,"LPSI")



        np.testing.assert_equal( longitudinalAxis,"Y")
        np.testing.assert_equal( forwardProgression,True)
        np.testing.assert_equal( globalFrame,"YXZ")

        longitudinalAxisFoot,forwardProgressionFoot,globalFrameFoot = trialTools.findProgression(trial,"RHEE")
        np.testing.assert_equal( longitudinalAxis,"Y")
        np.testing.assert_equal( forwardProgression,True)
        np.testing.assert_equal( globalFrame,"YXZ")

    @classmethod
    def gaitTrialProgressionY_backward_lateralX(cls):
        """
        """
        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"


        gaitFilename="gait_Y_backward.c3d"
        trial = trialTools.smartTrialReader(MAIN_PATH,gaitFilename)
        longitudinalAxis,forwardProgression,globalFrame = trialTools.findProgression(trial,"LPSI")


        np.testing.assert_equal( longitudinalAxis,"Y")
        np.testing.assert_equal( forwardProgression,False)
        np.testing.assert_equal( globalFrame,"YXZ")

        longitudinalAxis,forwardProgression,globalFrame = trialTools.findProgression(trial,"RHEE")

        np.testing.assert_equal( longitudinalAxis,"Y")
        np.testing.assert_equal( forwardProgression,False)
        np.testing.assert_equal( globalFrame,"YXZ")

    @classmethod
    def gaitTrialGarches(cls):
        """
        """
        MAIN_PATH = pyCGM2.TEST_DATA_PATH + "operations\\progression\\"

        gaitFilename="gait_garches_issue2.c3d"
        trial = trialTools.smartTrialReader(MAIN_PATH,gaitFilename)

        longitudinalAxis,forwardProgression,globalFrame = trialTools.findProgression(trial,"RHEE")

        np.testing.assert_equal( longitudinalAxis,"Y")
        np.testing.assert_equal( forwardProgression,False)
        np.testing.assert_equal( globalFrame,"YXZ")



if __name__ == "__main__":

    BtkProgressionTest_gaitTrial.gaitTrialProgressionX_forward_lateralY()
    BtkProgressionTest_gaitTrial.gaitTrialProgressionX_backward_lateralY()
    #BtkProgressionTest_gaitTrial.gaitTrialProgressionY_forward_lateralX() # issue with residual !! (FIXME)
    BtkProgressionTest_gaitTrial.gaitTrialProgressionY_backward_lateralX()
    BtkProgressionTest_gaitTrial.gaitTrialGarches()

    BtkProgressionTest_static.gaitTrialProgressionX_forward_lateralY_static()
    BtkProgressionTest_static.gaitTrialProgressionX_backward_lateralY_static()
    BtkProgressionTest_static.gaitTrialProgressionY_backward_lateralX_static()


    OpenmaProgressionTest_gaitTrial.gaitTrialProgressionX_forward_lateralY()
    OpenmaProgressionTest_gaitTrial.gaitTrialProgressionX_backward_lateralY()
    OpenmaProgressionTest_gaitTrial.gaitTrialProgressionY_forward_lateralX()
    OpenmaProgressionTest_gaitTrial.gaitTrialProgressionY_backward_lateralX()
    OpenmaProgressionTest_gaitTrial.gaitTrialGarches()
