# -*- coding: utf-8 -*-
#import ipdb
import logging
import matplotlib.pyplot as plt
import argparse


# pyCGM2 settings
import pyCGM2

# pyCGM2 libraries
from pyCGM2.Tools import btkTools
from pyCGM2 import enums

from pyCGM2.Model import modelFilters, modelDecorator,bodySegmentParameters
from pyCGM2.Model.CGM2 import cgm
from pyCGM2.Model.CGM2.coreApps import decorators
from pyCGM2.ForcePlates import forceplates


def get_markerLabelForPiGStatic(smc):

    useLeftKJCmarkerLabel = "LKJC"
    useLeftAJCmarkerLabel = "LAJC"
    useRightKJCmarkerLabel = "RKJC"
    useRightAJCmarkerLabel = "RAJC"


    # KAD
    if smc["left"] == enums.CgmStaticMarkerConfig.KAD:
        useLeftKJCmarkerLabel = "LKJC_KAD"
        useLeftAJCmarkerLabel = "LAJC_KAD"

    if smc["right"] == enums.CgmStaticMarkerConfig.KAD:
        useRightKJCmarkerLabel = "RKJC_KAD"
        useRightAJCmarkerLabel = "RAJC_KAD"

    # KADmed
    if smc["left"] == enums.CgmStaticMarkerConfig.KADmed:
        useLeftKJCmarkerLabel = "LKJC_KAD"
        useLeftAJCmarkerLabel = "LAJC_MID"

    if smc["right"] == enums.CgmStaticMarkerConfig.KADmed:
        useRightKJCmarkerLabel = "RKJC_KAD"
        useRightAJCmarkerLabel = "RAJC_MID"

    return [useLeftKJCmarkerLabel,useLeftAJCmarkerLabel,useRightKJCmarkerLabel,useRightAJCmarkerLabel]





def calibrate(DATA_PATH,calibrateFilenameLabelled,translators,
              required_mp,optional_mp,
              leftFlatFoot,rightFlatFoot,markerDiameter,
              pointSuffix):

    # --------------------------ACQUISITION ------------------------------------

    # ---btk acquisition---
    acqStatic = btkTools.smartReader(str(DATA_PATH+calibrateFilenameLabelled))
    btkTools.checkMultipleSubject(acqStatic)

    acqStatic =  btkTools.applyTranslators(acqStatic,translators)

    # ---definition---
    model=cgm.CGM1LowerLimbs()
    model.configure()
    model.addAnthropoInputParameters(required_mp,optional=optional_mp)

    # --store calibration parameters--
    model.setStaticFilename(calibrateFilenameLabelled)
    model.setCalibrationProperty("leftFlatFoot",leftFlatFoot)
    model.setCalibrationProperty("rightFlatFoot",rightFlatFoot)
    model.setCalibrationProperty("markerDiameter",markerDiameter)

    # ---check marker set used----
    smc= cgm.CGM.checkCGM1_StaticMarkerConfig(acqStatic)
    # --------------------------STATIC CALBRATION--------------------------
    scp=modelFilters.StaticCalibrationProcedure(model) # load calibration procedure

    # ---initial calibration filter----
    modelFilters.ModelCalibrationFilter(scp,acqStatic,model,
                                        leftFlatFoot = leftFlatFoot,
                                        rightFlatFoot = rightFlatFoot,
                                        markerDiameter = markerDiameter,
                                        viconCGM1compatible=True
                                        ).compute()
    # ---- Decorators -----
    decorators.applyDecorators_CGM1(smc, model,acqStatic,optional_mp,markerDiameter)
    pigStaticMarkers = get_markerLabelForPiGStatic(smc)

    # ----Final Calibration filter if model previously decorated -----
    if model.decoratedModel:
        # initial static filter
        modelFilters.ModelCalibrationFilter(scp,acqStatic,model,
                           leftFlatFoot = leftFlatFoot, rightFlatFoot = rightFlatFoot,
                           markerDiameter=markerDiameter,
                           viconCGM1compatible=True).compute()


    # ----------------------CGM MODELLING----------------------------------
    # ----motion filter----
    # notice : viconCGM1compatible option duplicate error on Construction of the foot coordinate system

    modMotion=modelFilters.ModelMotionFilter(scp,acqStatic,model,enums.motionMethod.Determinist,
                                              markerDiameter=markerDiameter,
                                              viconCGM1compatible=False,
                                              pigStatic=True,
                                              useLeftKJCmarker=pigStaticMarkers[0], useLeftAJCmarker=pigStaticMarkers[1],
                                              useRightKJCmarker=pigStaticMarkers[2], useRightAJCmarker=pigStaticMarkers[3])
    modMotion.compute()


    #---- Joint kinematics----
    # relative angles
    modelFilters.ModelJCSFilter(model,acqStatic).compute(description="vectoriel", pointLabelSuffix=pointSuffix)

    # detection of traveling axis
    longitudinalAxis,forwardProgression,globalFrame = btkTools.findProgressionAxisFromPelvicMarkers(acqStatic,["LASI","RASI","RPSI","LPSI"])


    # absolute angles
    modelFilters.ModelAbsoluteAnglesFilter(model,acqStatic,
                                           segmentLabels=["Left Foot","Right Foot","Pelvis"],
                                            angleLabels=["LFootProgress", "RFootProgress","Pelvis"],
                                            eulerSequences=["TOR","TOR", "TOR"],
                                            globalFrameOrientation = globalFrame,
                                            forwardProgression = forwardProgression).compute(pointLabelSuffix=pointSuffix)

    return model, acqStatic


def fitting(model,DATA_PATH, reconstructFilenameLabelled,
    translators,
    markerDiameter,
    pointSuffix,
    mfpa,
    momentProjection):
    # --------------------------ACQUISITION ------------------------------------

    # --- btk acquisition ----
    acqGait = btkTools.smartReader(str(DATA_PATH + reconstructFilenameLabelled))

    btkTools.checkMultipleSubject(acqGait)
    acqGait =  btkTools.applyTranslators(acqGait,translators)
    validFrames,vff,vlf = btkTools.findValidFrames(acqGait,cgm.CGM1LowerLimbs.TRACKING_MARKERS)

    scp=modelFilters.StaticCalibrationProcedure(model) # procedure

    # ---Motion filter----
    modMotion=modelFilters.ModelMotionFilter(scp,acqGait,model,enums.motionMethod.Determinist,
                                              markerDiameter=markerDiameter,
                                              viconCGM1compatible=True)

    modMotion.compute()


    #---- Joint kinematics----
    # relative angles
    modelFilters.ModelJCSFilter(model,acqGait).compute(description="vectoriel", pointLabelSuffix=pointSuffix)

    # detection of traveling axis
    longitudinalAxis,forwardProgression,globalFrame = btkTools.findProgressionAxisFromPelvicMarkers(acqGait,["LASI","LPSI","RASI","RPSI"])

    # absolute angles
    modelFilters.ModelAbsoluteAnglesFilter(model,acqGait,
                                           segmentLabels=["Left Foot","Right Foot","Pelvis"],
                                            angleLabels=["LFootProgress", "RFootProgress","Pelvis"],
                                            eulerSequences=["TOR","TOR", "TOR"],
                                            globalFrameOrientation = globalFrame,
                                            forwardProgression = forwardProgression).compute(pointLabelSuffix=pointSuffix)

    #---- Body segment parameters----
    bspModel = bodySegmentParameters.Bsp(model)
    bspModel.compute()

    # --- force plate handling----
    # find foot  in contact
    mappedForcePlate = forceplates.matchingFootSideOnForceplate(acqGait)
    forceplates.addForcePlateGeneralEvents(acqGait,mappedForcePlate)
    logging.debug("Force plate assignment : %s" %mappedForcePlate)

    if mfpa is not None:
        if len(mfpa) != len(mappedForcePlate):
            raise Exception("[pyCGM2] manual force plate assignment badly sets. Wrong force plate number. %s force plate require" %(str(len(mappedForcePlate))))
        else:
            mappedForcePlate = mfpa
            logging.warning("Manual Force plate assignment : %s" %mappedForcePlate)
            forceplates.addForcePlateGeneralEvents(acqGait,mappedForcePlate)

    # assembly foot and force plate
    modelFilters.ForcePlateAssemblyFilter(model,acqGait,mappedForcePlate,
                             leftSegmentLabel="Left Foot",
                             rightSegmentLabel="Right Foot").compute()

    #---- Joint kinetics----
    idp = modelFilters.CGMLowerlimbInverseDynamicProcedure()
    modelFilters.InverseDynamicFilter(model,
                         acqGait,
                         procedure = idp,
                         projection = momentProjection,
                         viconCGM1compatible=True
                         ).compute(pointLabelSuffix=pointSuffix)


    #---- Joint energetics----
    modelFilters.JointPowerFilter(model,acqGait).compute(pointLabelSuffix=pointSuffix)

    #---- zero unvalid frames ---
    btkTools.applyValidFramesOnOutput(acqGait,validFrames)

    return acqGait
