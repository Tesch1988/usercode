//
// Package:    UserCode/aachen3a/ACSusyAnalysis
// Class:      SusyACSkimAnalysis
// 
// Description: Skeleton analysis for SUSY search with Lepton + Jets + MET
//
// Original Author:  Carsten Magass
//         Created:  November 2008
//

// System include files
#include <memory>
#include <vector>
#include <string>
#include <sstream>
#include <iostream>
#include <iomanip>

// ROOT includes
#include <TNtuple.h>
#include <TH1F.h>

// Framework include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "RecoEcal/EgammaCoreTools/interface/EcalClusterTools.h"
#include "RecoEgamma/EgammaTools/interface/ConversionFinder.h"

#include "Geometry/CaloTopology/interface/CaloTopology.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloEventSetup/interface/CaloTopologyRecord.h"

#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "DataFormats/Luminosity/interface/LumiSummary.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Lepton.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/HepMCCandidate/interface/PdfInfo.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/Provenance/interface/EventAuxiliary.h"
#include "DataFormats/METReco/interface/HcalNoiseSummary.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "DataFormats/MuonReco/interface/MuonCocktails.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"

#include "PhysicsTools/PatUtils/interface/JetIDSelectionFunctor.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/PtComparator.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "MagneticField/Engine/interface/MagneticField.h"

#include "aachen3a/ACSusyAnalysis/interface/TriggerTools.h"

using namespace std;
using namespace pat;
using namespace ACSusyAnalysis;

////////////////////////////////
//
// Class declaration
//
class SusyACSkimAnalysis : public edm::EDFilter {
public:
  explicit SusyACSkimAnalysis(const edm::ParameterSet&);
  ~SusyACSkimAnalysis();
  
private:
  //*** CMSSW interface
  /// Called once per job, at start
  virtual void beginJob();
  /// Called once per run, at start
  virtual void beginMyRun(const edm::Run&, const edm::EventSetup&);
  /// Called for each event
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  /// Called once per job, at end
  virtual void endJob();
  
  /// Helpers
  virtual bool isStable(int pdgid);
  virtual bool isDecaying(int pdgid);
  virtual bool isSUSY(int pdgid);

  /// Print a summary of counts for all selectors
  virtual void printSummary(void);

  //*** Plotting
  /// Define all plots
  virtual void initPlots();

  double DeltaPhi(double a, double b);
  double DeltaR(double a, double b, double c, double d);

private:

  // Plots
  TTree * mAllData; // Will contain the SUSY-AC specific data

  TH1F* h_counters;

  HLTConfigProvider hltConfig_;
  bool hltConfigInit_;

  // Data tags
  edm::InputTag calojetTag_;
  edm::InputTag pfjetTag_;
  edm::InputTag metTag_;
  edm::InputTag metTagPF_;
  edm::InputTag metTagTC_;
  edm::InputTag elecTag_;
  edm::InputTag muonTag_;
  edm::InputTag genTag_;
  edm::InputTag genJetTag_;
  edm::InputTag vertexTag_;
  edm::InputTag ebhitsTag_;

  bool is_MC;
  bool is_SHERPA;
  bool do_fatjets;

  std::string btag_;
  std::string processName_; 

  GreaterByPt<pat::Muon>      ptcomp_muo;
  GreaterByPt<pat::Electron>  ptcomp_ele;
  GreaterByPt<pat::Jet>       ptcomp_jet;
  GreaterByPt<reco::GenJet>   ptcomp_genjet;

  typedef std::pair<std::string,float> IdPair;

  JetIDSelectionFunctor jetId;
  std::string vers_;
  std::string qual_;
  JetIDSelectionFunctor::Version_t vers;
  JetIDSelectionFunctor::Quality_t qual;

  TString ACmuonID[24];

  double _jeta[100];
  double _jphi[100];

  double bfield;

  int nele_;
  int nmuo_;
  int ncalojet_;
  int npfjet_;
  double muopt_;
  double muoeta_;
  double elept_;
  double eleeta_;
  double calojetpt_;
  double calojeteta_;
  double pfjetpt_;
  double pfjeteta_;
  double met_;

  double pthat_low_;
  double pthat_high_;

  // Counters
  unsigned int nrEventTotalRaw_;
  unsigned int nrEventPassedPthatRaw_;
  unsigned int nrEventPassedRaw_;

  int cele_;
  int cmuo_;
  int ccalojet_;
  int cpfjet_;

  double localPi;
  
  int pre1;
  int pre2;

  // Tree variables
  int mTreerun;
  int mTreeevent;
  int mTreestore;
  int mTreebx;
  int mTreeorbit;
  int mTreeexp;
  int mTreedata;

  int mTreelumiblk;
  double mTreedellumi;
  double mTreereclumi;
  double mTreedellumierr;
  double mTreereclumierr;

  int mTreenoisel;
  int mTreenoiset;
  int mTreenoiseh;

  double mTreeecalr9;
  double mTreeecale;
  double mTreeecalpt;
  double mTreeecalpx;
  double mTreeecalpy;
  double mTreeecalpz;
  double mTreeecaleta;
  double mTreeecalphi;
  double mTreeecaltime;
  double mTreeecalchi;
  int    mTreeecalieta;
  int    mTreeecaliphi;
  int    mTreeecalflag;

  int mTreetrighltname[20];
  
  int mTreeNtrig;
  int mTreetrigL1pre[1000];
  int mTreetrigHLTpre[1000];
  int mTreetrigname[1000][20];
  int mTreefiltname[1000][20];
  double mTreetrigpt[1000];
  double mTreetrigeta[1000];
  double mTreetrigphi[1000];
  
  double mTreeMET[5];
  double mTreeMEX[5];
  double mTreeMEY[5];
  double mTreeMETphi[5];
  double mTreeMETeta[5];
  double mTreeSumET[5];
  double mTreeSumETSignif[5];

  int    mTreeNtracks;
  double mTreetrackshqf;

  int mTreeNtruth;
  int mTreetruthpdgid[100];
  int mTreetruthbvtxid[100];
  int mTreetruthevtxid[100];
  double mTreetruthE[100];
  double mTreetruthEt[100];
  double mTreetruthp[100];
  double mTreetruthpt[100];
  double mTreetruthpx[100];
  double mTreetruthpy[100];
  double mTreetruthpz[100];
  double mTreetrutheta[100];
  double mTreetruthphi[100];
  double mTreetruthm[100];

  int mTreeNtruthl;
  int mTreetruthlpdgid[100];
  int mTreetruthlori[100];
  double mTreetruthlE[100];
  double mTreetruthlEt[100];
  double mTreetruthlp[100];
  double mTreetruthlpt[100];
  double mTreetruthlpx[100];
  double mTreetruthlpy[100];
  double mTreetruthlpz[100];
  double mTreetruthleta[100];
  double mTreetruthlphi[100];

  int mTreepdfid1;
  int mTreepdfid2;
  float mTreepdfx1;
  float mTreepdfx2;
  float mTreepdff1;
  float mTreepdff2;
  float mTreepdfscale;

  int    mTreeNCalojet;
  int    mTreeCaloJetTruth[100];
  int    mTreeCaloJetPart[100];
  int    mTreeCaloJetConst[100];
  int    mTreeCaloJetn90[100];
  int    mTreeCaloJetn90hits[100];
  int    mTreeCaloJetID[100];
  double mTreeCaloJetEt[100];
  double mTreeCaloJetPt[100];
  double mTreeCaloJetPtRaw[100];
  double mTreeCaloJetP[100];
  double mTreeCaloJetPx[100];
  double mTreeCaloJetPy[100];
  double mTreeCaloJetPz[100];
  double mTreeCaloJetE[100];
  double mTreeCaloJetEta[100];
  double mTreeCaloJetPhi[100];
  double mTreeCaloJetFem[100];
  double mTreeCaloJetFhad[100];
  double mTreeCaloJetBtag[100];
  double mTreeCaloJetCharge[100];
  double mTreeCaloJetfhpd[100];
  double mTreeCaloJetfrbx[100];

  int    mTreeNPFjet;
  int    mTreePFJetTruth[100];
  int    mTreePFJetPart[100];
  int    mTreePFJetConst[100];
  int    mTreePFJetN[100][7];
  int    mTreePFJetn90[100];
  double mTreePFJetEt[100];
  double mTreePFJetPt[100];
  double mTreePFJetPtRaw[100];
  double mTreePFJetP[100];
  double mTreePFJetPx[100];
  double mTreePFJetPy[100];
  double mTreePFJetPz[100];
  double mTreePFJetE[100];
  double mTreePFJetEta[100];
  double mTreePFJetPhi[100];
  double mTreePFJetBtag[100];
  double mTreePFJetCharge[100];
  double mTreePFJetF[100][7];

  int    mTreeNtruthjet;
  double mTreetruthJetEt[100];
  double mTreetruthJetPt[100];
  double mTreetruthJetP[100];
  double mTreetruthJetPx[100];
  double mTreetruthJetPy[100];
  double mTreetruthJetPz[100];
  double mTreetruthJetE[100];
  double mTreetruthJetEta[100];
  double mTreetruthJetPhi[100];

  int    mTreeNfatjet;
  int    mTreefatjetnsub[100];
  double mTreefatjetpt[100];
  double mTreefatjetpx[100];
  double mTreefatjetpy[100];
  double mTreefatjetpz[100];
  double mTreefatjete[100];
  double mTreefatjeteta[100];
  double mTreefatjetphi[100];
  double mTreefatjetsubpt[100][10];
  double mTreefatjetsubpx[100][10];
  double mTreefatjetsubpy[100][10];
  double mTreefatjetsubpz[100][10];
  double mTreefatjetsube[100][10];
  double mTreefatjetsubeta[100][10];
  double mTreefatjetsubphi[100][10];
  double mTreefatjetsubfem[100][10];
  double mTreefatjetsubfhad[100][10];
  double mTreefatjetsubbtag[100][10];
  double mTreefatjetsubn90[100][10];
  double mTreefatjetsubfhpd[100][10];
  double mTreefatjetsubfrbx[100][10];

  int    mTreeNSC;
  int    mTreeSCTruth[200];
  double mTreeSCE[200];
  double mTreeSCPhi[200];
  double mTreeSCEta[200];

  int    mTreeNele;
  int    mTreeNeletrign[100];
  int    mTreeEletrig[100][100];
  int    mTreeEleID[100][5];
  int    mTreeEleTruth[100];
  int    mTreeEleSC[100];
  int    mTreeEleHits[100];
  int    mTreeEleValidHitFirstPxlB[100];
  int    mTreeEleTrkExpHitsInner[100];
  int    mTreeEleisECal[100];
  int    mTreeEleisTracker[100];
  double mTreeEleEt[100];
  double mTreeEleP[100];
  double mTreeElePt[100];
  double mTreeElePx[100];
  double mTreeElePy[100];
  double mTreeElePz[100];
  double mTreeEleE[100];
  double mTreeEleEta[100];
  double mTreeElePhi[100];
  double mTreeEleHCalOverEm[100];
  double mTreeEleDr03TkSumPt[100];
  double mTreeEleDr04HCalTowerSumEt[100];
  double mTreeEleDr03HCalTowerSumEt[100];
  double mTreeEleDr04ECalRecHitSumEt[100];
  double mTreeEleDr03ECalRecHitSumEt[100];
  double mTreeEleSigmaIetaIeta[100];
  double mTreeEleDeltaEtaSuperClusterTrackAtVtx[100];
  double mTreeEleDeltaPhiSuperClusterTrackAtVtx[100];
  double mTreeEleTrkChiNorm[100];
  double mTreeEleCharge[100];
  double mTreeEled0vtx[100];
  double mTreeEled0bs[100];
  double mTreeElesd0[100];
  double mTreeEleConvdist[100];
  double mTreeEleConvdcot[100];
  double mTreeEleConvr[100];
  double mTreeElefbrem[100];
  double mTreeEledr03HcalDepth1[100];
  double mTreeEledr03HcalDepth2[100];
  double mTreeElee2x5Max[100];
  double mTreeElee5x5[100];

  int    mTreeNmuo;
  int    mTreeNmuotrign[100];
  int    mTreeMuotrig[100][500];
  int    mTreeMuoTruth[100];
  int    mTreeMuoHitsCm[100];
  int    mTreeMuoHitsTk[100];
  int    mTreeMuoGood[100];
  int    mTreeMuoValidMuonHitsCm[100];
  int    mTreeMuoValidTrackerHitsCm[100];
  int    mTreeMuoValidPixelHitsCm[100];
  int    mTreeMuoChambersMatched[100];
  int    mTreeMuoTrackerLayersMeasCm[100];
  int    mTreeMuoTrackerLayersNotMeasCm[100];
  int    mTreeMuoID[100][24];
  double mTreeMuoEt[100];
  double mTreeMuoP[100];
  double mTreeMuoPt[100];
  double mTreeMuoPx[100];
  double mTreeMuoPy[100];
  double mTreeMuoPz[100];
  double mTreeMuoE[100];
  double mTreeMuoEta[100];
  double mTreeMuoPhi[100];
  double mTreeMuoTrkIso[100];
  double mTreeMuoRelTrkIso[100];
  double mTreeMuoECalIso[100];
  double mTreeMuoHCalIso[100];
  double mTreeMuoAllIso[100];
  double mTreeMuoECalIsoDep[100];
  double mTreeMuoHCalIsoDep[100];
  double mTreeMuoTrkIsoDep[100];
  double mTreeMuoTrkChiNormCm[100];
  double mTreeMuoTrkChiNormTk[100];
  double mTreeMuoCharge[100];
  double mTreeMuod0Cm[100];
  double mTreeMuod0Tk[100];
  double mTreeMuosd0Cm[100];
  double mTreeMuosd0Tk[100];
  double mTreeMuocalocomp[100];
  double mTreeMuocaltowe[100];
  double mTreeMuod0bsCm[100];
  double mTreeMuod0OriginCm[100];

  double mTreeMuoCocktailPt[100];
  double mTreeMuoCocktailPhi[100];
  double mTreeMuoCocktailEta[100];

  int    mTreeNvtx;
  int    mTreeVtxntr[100];
  int    mTreeVtxfake[100];
  double mTreeVtxndf[100];
  double mTreeVtxx[100];
  double mTreeVtxy[100];
  double mTreeVtxz[100];
  double mTreeVtxchi[100];

  double mTreebspX;
  double mTreebspY;
  double mTreebspZ;

  double mTreeEventWeight;
  int    mTreeProcID;
  double mTreePthat;
  double mTreebfield;

};
