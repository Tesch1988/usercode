from PhysicsTools.PatAlgos.tools.coreTools import *

def addScrapingFilter( process ):
    process.scrapingFilter = cms.EDFilter( 'FilterOutScraping',
                                           applyfilter = cms.untracked.bool( True ),
                                           debugOn = cms.untracked.bool( False ),
                                           numtrack = cms.untracked.uint32( 10 ),
                                           thresh = cms.untracked.double( 0.25 )
                                           )
    process.p_scrapingFilter = cms.Path( process.scrapingFilter )
    process.ACSkimAnalysis.filterlist.append( 'p_scrapingFilter' )
    
def addCSCHaloFilter ( process ):
    process.load('RecoMET.METAnalyzers.CSCHaloFilter_cfi')
    process.p_CSCHaloFilter = cms.Path(process.CSCTightHaloFilter )
    process.ACSkimAnalysis.filterlist.append( 'p_CSCHaloFilter' )
    
def addHCALLaserFilter ( process ):
    process.load("RecoMET.METFilters.hcalLaserEventFilter_cfi")
    process.p_HCALLaserFilter = cms.Path(process.hcalLaserEventFilter)
    process.ACSkimAnalysis.filterlist.append( 'p_HCALLaserFilter' )
    

#make 2 filter for Trigger Primitive and  Boundary Energy:
def addECALDeadCellFilterTP ( process ):
    process.load('RecoMET.METFilters.EcalDeadCellTriggerPrimitiveFilter_cfi')
    ## For AOD and RECO recommendation to use recovered rechits
    process.EcalDeadCellTriggerPrimitiveFilter.tpDigiCollection = cms.InputTag("ecalTPSkimNA")
    process.p_ECALDeadCellFilterTP = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
    process.ACSkimAnalysis.filterlist.append( 'p_ECALDeadCellFilterTP' )

#use the default
def addECALDeadCellFilterBE ( process ):
    process.load('RecoMET.METFilters.EcalDeadCellBoundaryEnergyFilter_cfi')
    process.p_ECALDeadCellFilterBE = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
    process.ACSkimAnalysis.filterlist.append( 'p_ECALDeadCellFilterBE' )

def addTrackingFailureFilter ( process ):
    process.goodVertices = cms.EDFilter(
        "VertexSelector",
        filter = cms.bool(False),
        src = cms.InputTag("offlinePrimaryVertices"),
        cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.rho < 2")
    )
    process.load('RecoMET.METFilters.trackingFailureFilter_cfi')
    process.p_TrackingFailureFilter = cms.Path(process.goodVertices*process.trackingFailureFilter)
    process.ACSkimAnalysis.filterlist.append( 'p_TrackingFailureFilter' )
    
def addMuonFailureFilter ( process ):
    process.load('RecoMET.METFilters.inconsistentMuonPFCandidateFilter_cfi')
    process.load('RecoMET.METFilters.greedyMuonPFCandidateFilter_cfi')
    process.p_MuonFailureFilter = cms.Path(process.greedyMuonPFCandidateFilter*process.inconsistentMuonPFCandidateFilter)
    process.ACSkimAnalysis.filterlist.append( 'p_MuonFailureFilter' )

def addKinematicsFilter( process ):
    process.load( 'GeneratorInterface.GenFilters.TotalKinematicsFilter_cfi' )
    process.p_kinematicsfilter = cms.Path( process.totalKinematicsFilter )
    process.ACSkimAnalysis.filterlist.append( 'p_kinematicsfilter' )

def addBadSuperCrystalFilter( process ):
    process.load('RecoMET.METFilters.eeBadScFilter_cfi')
    process.p_BadSuperCrystalFilter = cms.Path(process.eeBadScFilter)
    process.ACSkimAnalysis.filterlist.append( 'p_BadSuperCrystalFilter' )

def addHBHENoiseFilter( process ):
    #see https://twiki.cern.ch/twiki/bin/view/CMS/HBHEAnomalousSignals2011
    #process.load("CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi")
    ## The iso-based HBHE noise filter ___________________________________________||
    process.load('CommonTools.RecoAlgos.HBHENoiseFilter_cfi')
    process.p_HBHENoiseFilter = cms.Path(process.HBHENoiseFilter)
    process.ACSkimAnalysis.filterlist.append( 'p_HBHENoiseFilter' )


process = cms.Process("ANA")

isData=@ISDATA@
qscalehigh=@QSCALE_LOW@
qscalelow=@QSCALE_HIGH@
tauSwitch=@DOTAU@
pfeleSwitch=@DOPFELE@
Pythia8Switch=@PYTHIA8@
SherpaSwitch=@SHERPA@
MatchAllSwitch=@MATCHALL@
SusyParSwith=@SUSYPAR@
IsPythiaShowered=@ISPYTHIASHOWERED@
#~ qscalehigh=-1.
#~ qscalelow=-1.
#~ isData=False
#~ tauSwitch=False
#~ IsPythiaShowered=True
# Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.extend(['SusyACSkimAnalysis'])
process.MessageLogger.cerr.default.limit = -1
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

#-- Calibration tag -----------------------------------------------------------
# Should match input file's tag
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('@GLOBALTAG@')
#~ process.GlobalTag.globaltag = cms.string('START44_V5::All')
process.load("Configuration.StandardSequences.MagneticField_cff")

#-- PAT standard config -------------------------------------------------------
process.load("PhysicsTools.PatAlgos.patSequences_cff")
process.load("RecoVertex.Configuration.RecoVertex_cff")

from RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi import *
process.load("RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi")

# see https://twiki.cern.ch/twiki/bin/view/CMS/HBHEAnomalousSignals2011
# process.load("CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi")

# Pythia GEN filter (used to correct for wrong 4-momentum-imbalance
# see https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/1489.html
process.load("GeneratorInterface.GenFilters.TotalKinematicsFilter_cfi")


#-- To get JEC in 4_2 return rho corrections:----------------------------------------------------
#process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
#~ process.load('RecoJets.Configuration.RecoPFJets_cff')
#process.kt6PFJets.doRhoFastjet = True
#process.ak5PFJets.doAreaFastjet = True

#--This is a temporary fix for electrons
#process.load("SHarper.HEEPAnalyzer.gsfElectronsHEEPCorr_cfi")
#process.load("RecoEgamma.ElectronIdentification.electronIdSequence_cff")

#--To modify noPU needed for METnoPU -------------------------------------------
process.load('CommonTools.ParticleFlow.pfNoPileUp_cff')

# Output (PAT file only created if
# process.outpath = cms.EndPath(process.out)
# is called at the end
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out2 = cms.OutputModule(
    "PoolOutputModule",
    fileName       = cms.untracked.string('dummy.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    dropMetaData   = cms.untracked.string('DROPPED'),
    outputCommands = cms.untracked.vstring('keep *')
    )

##dummy out to be modifyed by pf2pat
process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName       = cms.untracked.string('dummy2.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    dropMetaData   = cms.untracked.string('DROPPED'),
    outputCommands = cms.untracked.vstring('keep *')
    )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('out.root')
                                   )

from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0) ),
    src=cms.InputTag('offlinePrimaryVertices')
)


### Input / output ###

# Input file
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring([
#    'file:///user/mweber/AODSIM/DoubleMu+Run2012A-13Jul2012-v1.root',
    'file:///user/mweber/AODSIM/Summer12_DR53X+DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph.root'
    ]),
    #duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
#PAT Stuff


process.patMuons.embedCombinedMuon = False;
process.patMuons.embedStandAloneMuon = False;



if tauSwitch:
	process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")

# PF2PAT
from PhysicsTools.PatAlgos.tools.pfTools import *

postfix = "PFlow"
if isData:
    usePF2PAT(process, runPF2PAT=True, jetAlgo='AK5', runOnMC=False, postfix=postfix, jetCorrections=('AK5PFchs',['L1FastJet','L2Relative','L3Absolute','L2L3Residual']))
    removeMCMatching(process, ['All'])
else:
     usePF2PAT(process, runPF2PAT=True, jetAlgo='AK5', runOnMC=True, postfix=postfix, jetCorrections=('AK5PFchs',['L1FastJet', 'L2Relative', 'L3Absolute']))


process.load("PhysicsTools/PatAlgos/patSequences_cff")

from PhysicsTools.PatAlgos.tools.tauTools import *
switchToPFTauHPS(process)


# switch on PAT trigger
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
switchOnTrigger(process)

# for PFnoPU
process.pfPileUpPFlow.Enable = True
process.pfPileUpPFlow.checkClosestZVertex = cms.bool(False)
process.pfPileUpPFlow.Vertices = cms.InputTag('goodOfflinePrimaryVertices')
process.pfJetsPFlow.doAreaFastjet = True
process.pfJetsPFlow.doRhoFastjet = False


from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJetsPFlow = kt4PFJets.clone(
    rParam = cms.double(0.6),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True)
    )

# https://twiki.cern.ch/twiki/bin/view/CMS/EgammaEARhoCorrection Rho Computation for Electrons
process.kt6PFJetsForIsolation = kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
process.kt6PFJetsForIsolation.Rho_EtaMax = cms.double(2.5)

process.patJetCorrFactorsPFlow.rho = cms.InputTag("kt6PFJetsPFlow", "rho")
if isData:
    process.patJetCorrFactorsPFlow.levels = cms.vstring('L1FastJet', 'L2Relative', 'L3Absolute','L2L3Residual')
else:
    process.patJetCorrFactorsPFlow.levels = cms.vstring('L1FastJet', 'L2Relative', 'L3Absolute') # MC


if isData:
    process.patJetCorrFactors.levels = cms.vstring('L1FastJet', 'L2Relative', 'L3Absolute','L2L3Residual') # DATA
else:
    process.patJetCorrFactors.levels = cms.vstring('L1FastJet', 'L2Relative', 'L3Absolute') # MC

process.patJetCorrFactors.useRho = True

# Add anti-kt 5 jets
# this is only for calo met is there an other way?




# Add the PV selector and KT6 producer to the sequence
getattr(process,"patPF2PATSequence"+postfix).replace(
    getattr(process,"pfNoElectron"+postfix),
    getattr(process,"pfNoElectron"+postfix)*process.kt6PFJetsPFlow )


# add TrackCorrected  met
from PhysicsTools.PatAlgos.tools.metTools import *
addTcMET(process, 'TC')

# get the jet corrections
from PhysicsTools.PatAlgos.tools.jetTools import *

# Add met with NoPU to the Collections FIXED
#~ from aachen3a.ACSusyAnalysis.pfMET_cfi import *
#~ process.pfMetPFnoPU         = pfMET.clone()
#~ process.pfMetPFnoPU.alias   = 'pfMetNoPileUp'
#~ process.pfMetPFnoPU.src     = 'pfNoPileUpPFlow'
#~ process.pfMetPFnoPU.jets = cms.InputTag("ak5PFJets")


from CommonTools.ParticleFlow.Tools.pfIsolation import setupPFElectronIso, setupPFPhotonIso
process.eleIsoSequence = setupPFElectronIso(process, 'patElectrons')
process.phoIsoSequence = setupPFPhotonIso(process, 'patPhotons')


process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")
from JetMETCorrections.Type1MET.pfMETCorrections_cff import pfType1CorrectedMet

process.pfMETType1 = pfType1CorrectedMet.clone()
process.pfMETType1.applyType0Corrections = cms.bool(False)
process.pfMETType0 = pfType1CorrectedMet.clone()
process.pfMETType0.applyType1Corrections = cms.bool(False)

if tauSwitch:
    tausequence = cms.Sequence( process.PFTau)
else:
    tausequence = cms.Sequence()
if IsPythiaShowered:
    filtersequence = cms.Sequence( process.totalKinematicsFilter )
else:
    filtersequence = cms.Sequence()

# photon
# the isolation has to be reprocessed, cf. https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPFBasedIsolation#The_25th_May_update
# which require the EGammaAnalysisTools photonIsoProducer from:
# cvs co -r V00-00-21 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
# cvs up -r 1.13 EGamma/EGammaAnalysisTools/interface/PFIsolationEstimator.h
# cvs up -r 1.20 EGamma/EGammaAnalysisTools/src/PFIsolationEstimator.cc 
process.load('EGamma.EGammaAnalysisTools.photonIsoProducer_cfi')
process.phoPFIso.verbose = False
IsoValPhotonPF = cms.VInputTag(cms.InputTag('phoPFIso:chIsoForGsfEle'),
                               cms.InputTag('phoPFIso:phIsoForGsfEle'),
                               cms.InputTag('phoPFIso:nhIsoForGsfEle'))
#it also requires to add phoPFIso in the path



################################
###                          ###
###  Analysis configuration  ###
###                          ###
################################


### Definition of all tags here
elecTag         = cms.InputTag("patElectrons")
pfelecTag      = cms.InputTag("patElectronsPFlow")
gsfelecTag         = cms.InputTag("gsfElectrons")
photonTag         = cms.InputTag("patPhotons")
pfjetTag        = cms.InputTag("patJetsPFlow")
muonTag      = cms.InputTag("patMuons")
PFmuonTag  = cms.InputTag("selectedPatMuonsPFlow")
tauTag         = cms.InputTag("patTaus")
metTag        = cms.InputTag("patMETs")
metTagTC    = cms.InputTag("patMETsTC")
metTagPF    = cms.InputTag("patMETsPFlow")
metTagPFnoPU=cms.InputTag("pfMETType0")
metTagJPFnoPUType1 =cms.InputTag("pfType1CorrectedMet")
metTagcorMetGlobalMuons     = cms.InputTag("pfMETType1")
#these two are ignored for now:
metTagHO    = cms.InputTag("metHO")
metTagNoHF= cms.InputTag("metNoHF")
genTag        = cms.InputTag("genParticles")
genJetTag    = cms.InputTag("ak5GenJets")
vtxTag         = cms.InputTag("offlinePrimaryVertices")
reducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB")
reducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE")
#ebhitsTag  = cms.InputTag("ecalRecHit", "EcalRecHitsEB");  # RECO
ebhitsTag     = cms.InputTag("reducedEcalRecHitsEB")   # AOD
HLTInputTag = cms.InputTag('TriggerResults','','HLT')
TriggerSummaryTag = cms.InputTag('hltTriggerSummaryAOD',"","HLT")

# For Particle Based Isolation for Electrons & Photons, following latest EGamma Recipie https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPFBasedIsolation

IsoDepElectron = cms.VInputTag(cms.InputTag('elPFIsoDepositChargedPFIso'),
	cms.InputTag('elPFIsoDepositGammaPFIso'),
	cms.InputTag('elPFIsoDepositNeutralPFIso'))
IsoValElectronPF = cms.VInputTag(cms.InputTag('elPFIsoValueCharged03PFIdPFIso'),
	cms.InputTag('elPFIsoValueGamma03PFIdPFIso'),
	cms.InputTag('elPFIsoValueNeutral03PFIdPFIso'))
IsoValElectronNoPF = cms.VInputTag(cms.InputTag('elPFIsoValueCharged03NoPFIdPFIso'),
	cms.InputTag('elPFIsoValueGamma03NoPFIdPFIso'),
	cms.InputTag('elPFIsoValueNeutral03NoPFIdPFIso'))
IsoDepPhoton = cms.VInputTag(cms.InputTag('phPFIsoDepositChargedPFIso'),
	cms.InputTag('phPFIsoDepositGammaPFIso'),
	cms.InputTag('phPFIsoDepositNeutralPFIso'))
#IsoValPhotonPF = cms.VInputTag(cms.InputTag('phPFIsoValueCharged03PFIdPFIso'),
#	cms.InputTag('phPFIsoValueGamma03PFIdPFIso'),
#	cms.InputTag('phPFIsoValueNeutral03PFIdPFIso'))
IsoValPhotonNoPF = cms.VInputTag(cms.InputTag('phPFIsoValueCharged03NoPFIdPFIso'),
	cms.InputTag('phPFIsoValueGamma03NoPFIdPFIso'),
	cms.InputTag('phPFIsoValueNeutral03NoPFIdPFIso'))


#~ inputTagIsoValElectronsPFId = cms.InputTag("IsoValElectronPF")

### Cuts and switches ###
process.ACSkimAnalysis = cms.EDFilter(
    "SusyACSkimAnalysis",

    is_MC      = cms.bool(not isData),  # set to 'False' for real Data !
    is_PYTHIA8 = cms.bool(Pythia8Switch),  # set to 'True' if running on PYTHIA8
    is_SHERPA  = cms.bool(SherpaSwitch),  # set to 'True' if running on SHERPA
    matchAll   = cms.bool(MatchAllSwitch),  # if True all truth leptons are matched else only ele and mu
    susyPar    = cms.bool(SusyParSwith),
    doTaus     = cms.bool(tauSwitch),
    doPFele    = cms.bool(pfeleSwitch),

    # This is used to access the results of all filters that ran.
    #
    filters = cms.PSet(
        AllFilters = cms.PSet(
            process = cms.string( 'PAT' ),
            results = cms.string( 'TriggerResults' ),
            paths = cms.vstring()
            )
        ),

    pfjetTag   = pfjetTag,
    elecTag    = elecTag,
    gsfelecTag    = gsfelecTag,
    photonTag  = photonTag,
    pfelecTag  = pfelecTag,
    muonTag    = muonTag,
    PFmuonTag  = PFmuonTag,
    tauTag     = tauTag,
    metTag     = metTag,
    metTagTC   = metTagTC,
    metTagPF   = metTagPF,
    metTagPFnoPU   =metTagPFnoPU,
    metTagJPFnoPUType1= metTagJPFnoPUType1,
    metTagcorMetGlobalMuons =metTagcorMetGlobalMuons,
    metTagHO = metTagHO,
    metTagNoHF = metTagNoHF,
    genTag     = genTag,
    genJetTag  = genJetTag,
    vtxTag     = vtxTag,
    ebhitsTag  = ebhitsTag,
    reducedBarrelRecHitCollection = reducedBarrelRecHitCollection,
    reducedEndcapRecHitCollection = reducedEndcapRecHitCollection,
    HLTInputTag = HLTInputTag,
    TriggerSummaryTag = TriggerSummaryTag,

	IsoDepElectron = IsoDepElectron,
	IsoValElectronPF = IsoValElectronPF,
	IsoDepPhoton = IsoDepPhoton,
	IsoValPhotonPF = IsoValPhotonPF,


    qscale_low  = cms.double(qscalelow),
    qscale_high = cms.double(qscalehigh),
    muoptfirst = cms.double(@MUOPTFIRST@),
    muoptother = cms.double(@MUOPTOTHER@),
    muoeta     = cms.double(@MUOETA@),
    elept      = cms.double(@ELEPT@),
    eleeta     = cms.double(@ELEETA@),
    phopt      = cms.double(@PHOPT@),
    phoeta     = cms.double(@PHOETA@),
    pfelept    = cms.double(@PFELEPT@),
    pfeleeta   = cms.double(@PFELEETA@),
    pfjetpt    = cms.double(@PFJETPT@),
    pfjeteta   = cms.double(@PFJETETA@),
    taupt      = cms.double(@TAUPT@),
    taueta     = cms.double(@TAUETA@),
    metcalo    = cms.double(@METCALO@),
    metpf      = cms.double(@METPF@),
    mettc      = cms.double(@METTC@),
    nele       = cms.int32(@NELE@),
    npho       = cms.int32(@NPHO@),
    npfele     = cms.int32(@NPFELE@),
    nmuo       = cms.int32(@NMUO@),
    npfjet     = cms.int32(@NPFJET@),
    ntau       = cms.int32(@NTAU@),
    htc        = cms.double(@HTC@),
    PFhtc      = cms.double(@PFHTC@),
    triggerContains=cms.string(@TRIGGERCONTAINS@),
    muoMinv    = cms.double(@MUOMINV@),
    muoDMinv   = cms.double(@MUODMINV@),

    btag       = cms.string('trackCountingHighEffBJetTags'),

    # Calo Jet ID
    jetselvers = cms.string("PURE09"),
    jetselqual = cms.string("LOOSE")



)


### Define the paths
process.p = cms.Path(
    filtersequence*
    #process.gsfElectronsHEEPCorr*
    process.eIdSequence*
    process.goodOfflinePrimaryVertices*
    tausequence*
    process.patDefaultSequence*
    getattr(process,"patPF2PATSequence"+postfix)*
    process.pfParticleSelectionSequence*
    process.eleIsoSequence*
    process.phoIsoSequence*
    process.phoPFIso*
    process.kt6PFJetsForIsolation*
    process.producePFMETCorrections*
    process.pfMETType0*
    process.pfMETType1
    )



    # The skimmer is in the endpath because then the results of all preceding paths
    # are available. This is used to access the outcome of filters that ran.
    #
process.ACSkimAnalysis.filterlist = cms.vstring()
addScrapingFilter( process )
addCSCHaloFilter( process )
addHCALLaserFilter( process )
addECALDeadCellFilterTP( process )
addECALDeadCellFilterBE( process )
addMuonFailureFilter( process )
addBadSuperCrystalFilter( process )
addTrackingFailureFilter( process )
addHBHENoiseFilter( process )

if IsPythiaShowered:
    addKinematicsFilter( process )

process.ACSkimAnalysis.filters.AllFilters.paths = process.ACSkimAnalysis.filterlist
process.ACSkimAnalysis.filters.AllFilters.process = process.name_()
#~ process.outpath = cms.EndPath(process.out2)
process.e = cms.EndPath(process.ACSkimAnalysis )
