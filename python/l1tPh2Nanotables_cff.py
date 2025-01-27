import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.l1trig_cff import *

#### GTT Vertex
vtxTable = cms.EDProducer(
    "SimpleL1VtxWordCandidateFlatTableProducer", ## note the use of a dedicated table producer which is defined in the plugins/L1TableProducer.cc
    src = cms.InputTag('l1tVertexFinderEmulator','L1VerticesEmulation'),
    cut = cms.string(""),
    name = cms.string("L1Vertex"),
    doc = cms.string("GTT Vertices"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        z0 = Var("z0()",float, doc = "primary vertex position z coordinate"),
        sumPt = Var("pt()",float, doc = "sum pt of tracks"),
        hwValid = Var("validBits()",bool, doc = "hardware vertex valid bit"),
        hwZ0 = Var("z0Bits()",int, doc = "hardware z0 vertex position"),
        # hwNTracksIn = Var("multiplicityBits()",int, doc = "hardware track multiplicity in the vertex"), # Currently not filled in emulation or firmware
        hwPt = Var("ptBits()",int,doc="hardware pt"), # This value seems to be essentially (uint)pt(), but there should be 2 float bits (0.25GeV granularity) represented here... is to_uint() truncating the float bits?
        # hwQual = Var("qualityBits()",int,doc="hardware qual"), # Currently not filled in emulation or firmware
        # hwNTracksOut = Var("inverseMultiplicityBits()",int, doc = "hardware track multiplicity out of the vertex"), # Currently not filled in emulation or firmware
     )
 )

gttTrackJetsTable = cms.EDProducer(
    "SimpleL1TkJetWordCandidateFlatTableProducer",
    src = cms.InputTag("l1tTrackJetsEmulation","L1TrackJets"),
    name = cms.string("L1TrackJet"),
    doc = cms.string("GTT Track Jets"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        pt = Var("pt()", float, doc="pt"),
        eta = Var("glbeta()", float, doc="eta"),
        phi = Var("glbphi()", float, doc="phi"),
        z0 = Var("z0()", float, doc="z0"), #Jet z0 is now always 0, however?
        hwPt = Var("ptBits()", int, doc="hardware pt"),
        hwEta = Var("glbPhiBits()", int, doc="hardware eta"),
        hwPhi = Var("glbEtaBits()", int, doc="hardware eta"),
        hwZ0 = Var("z0Bits()", int, doc="hardware z0"), #Jet z0 is now always 0, however?
        hwNTracks = Var("ntBits()", int, doc="hardware number of tracks"),
        hwNDisplacedTracks = Var("ntBits()", int, doc="hardware number of tracks"),
    )
)

gttExtTrackJetsTable = gttTrackJetsTable.clone(
    src = cms.InputTag("l1tTrackJetsExtendedEmulation", "L1TrackJetsExtended"),
    name = cms.string("L1ExtTrackJet"),
    doc = cms.string("GTT Extended Track Jets"),
)

gttEtSumTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tTrackerEmuEtMiss", "L1TrackerEmuEtMiss"),
    name = cms.string("L1TrackMET"),
    doc = cms.string("GTT Track MET"),
    singleton = cms.bool(True), # the number of entries is variable
    variables = cms.PSet(
        # pt = Var("pt", float, doc="MET pt"),
        pt = Var("hwPt() * 0.03125", float, doc = "Track MET"), # as in https://github.com/cms-l1t-offline/cmssw/blob/phase2-l1t-integration-14_0_0_pre3/L1Trigger/L1TTrackMatch/interface/L1TkEtMissEmuAlgo.h#L50
        hwPt = Var("hwPt()", int, doc = "hardware Pt Track MET"),
        # phi = Var("phi", float, doc="MET phi"),
        # hwValid = Var("hwQual() > 0",int, doc = "hardware Missing Et valid bit"),
        hwValid = Var("hwQual()",bool, doc = "hardware Missing Et valid bit"),
        # hwVectorSumPt = Var("Et().range()", int, doc = "hardware Missing Et vector sum"),
        hwPhi = Var("hwPhi", int, doc = "hardware Missing Et phi"),
    )
)

gttHtSumTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tTrackerEmuHTMiss", "L1TrackerEmuHTMiss"),
    name = cms.string("L1TrackHT"),
    doc = cms.string("GTT Track Missing HT"),
    singleton = cms.bool(True), # the number of entries is variable
    variables = cms.PSet(
        hwValid = Var("hwQual()",bool, doc = "hardware Track MHT valid bit"),
        hwPhi = Var("hwPhi()", int, doc = "hardware Track MHT phi"),
        hwPt = Var("hwPt()", int, doc = "hardware Track HT"),
        # mht = Var("pt", float, doc="MHT pt"),
        # mhtPhi = Var("phi", float, doc="MHT phi"),
        mht = Var(f"p4().energy() * 0.03125", float, doc="MHT"), # as in https://github.com/artlbv/cmssw/blob/from-CMSSW_12_5_2_patch1/L1Trigger/L1TNtuples/src/L1AnalysisPhaseIIStep1.cc#L623
        ht = Var("hwPt() * 0.03125", float, doc = "Track HT"), # as in https://github.com/cms-l1t-offline/cmssw/blob/phase2-l1t-integration-14_0_0_pre3/L1Trigger/L1TTrackMatch/interface/L1TkHTMissEmulatorProducer.h#L65
    )
)

### Store Primary Vertex only (first vertex)
pvtxTable = vtxTable.clone(
    maxLen = cms.uint32(1),
    name = cms.string("L1PV"),
    doc = cms.string("GTT Leading Primary Vertex"),
)

#### EG
tkPhotonTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag('l1tLayer2EG','L1CtTkEm'),
    cut = cms.string("pt > 5"),
    name = cms.string("L1tkPhoton"),
    doc = cms.string("Tk Photons (EM)"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1ObjVars,
        relIso = Var("trkIsol", float, doc = "relative Isolation based on trkIsol variable"),
        # tkIso   = Var("trkIsol", float), ## use above instead to be consistent with the GT and with the tkEle
        # tkIsoPV  = Var("trkIsolPV", float),
        # pfIso   = Var("pfIsol", float),
        # puppiIso  = Var("puppiIsol", float),
        ## quality WPs, see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePhysicsCutParser#Suppported_operators_and_functio
        saId  = Var("test_bit(hwQual(),0)", bool, doc = "standalone ID, bit 0 of hwQual"),
        eleId = Var("test_bit(hwQual(),1)", bool, doc = "electron ID, bit 1 of hwQual"),
        phoId = Var("test_bit(hwQual(),2)", bool, doc = "photon ID, bit 2 of hwQual"),
    )
)

tkEleTable = tkPhotonTable.clone(
    src = cms.InputTag('l1tLayer2EG','L1CtTkElectron'),
    name = cms.string("L1tkElectron"),
    doc = cms.string("Tk Electrons"),
)
tkEleTable.variables.z0     = Var("trkzVtx", float, "track vertex z0")
tkEleTable.variables.charge = Var("charge", int, doc="charge")
## additional variables that are not used in the menu/GT
## from https://github.com/p2l1pfp/FastPUPPI/blob/12_5_X/NtupleProducer/python/runPerformanceNTuple.py#L499C8-L501C83
# tkEleTable.variables.tkEta = Var("trkPtr.eta", float,precision=8)
# tkEleTable.variables.tkPhi = Var("trkPtr.phi", float,precision=8)
# tkEleTable.variables.tkPt = Var("trkPtr.momentum.perp", float,precision=8)

# merge EG
staEGmerged = cms.EDProducer("CandViewMerger",
       src = cms.VInputTag(
           cms.InputTag('l1tPhase2L1CaloEGammaEmulator','GCTEGammas'),
           cms.InputTag('l1tLayer2EG','L1CtEgEE'),
  )
)

# #staEGTable = tkPhotonTable.clone(
#     src = cms.InputTag("staEGmerged"),
#     name = cms.string("L1EG"),
#     doc = cms.string("standalone EG merged endcap and barrel"),
#     variables = cms.PSet(
#         l1P3Vars,
#     )
# )

staEGTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("staEGmerged"),
    cut = cms.string("pt > 5"),
    name = cms.string("L1EG"),
    doc = cms.string("standalone EG merged endcap and barrel"),
    # singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1P3Vars,
        ### FIXME
        ### NOTE THE BELOW DOES NOT WORK FOR NOW
        ### This only works when using each collection barrel/endcap separately with the SimpleTriggerL1EGFlatTableProducer -> Need to fix this !
        # hwQual = Var("hwQual",int,doc="hardware qual"),
        ## quality WPs, see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePhysicsCutParser#Suppported_operators_and_functio
        # saId  = Var("test_bit(hwQual(),0)", bool),
        # eleId = Var("test_bit(hwQual(),1)", bool),
        # phoId = Var("test_bit(hwQual(),2)", bool),
    )
)

staEGebTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag('l1tPhase2L1CaloEGammaEmulator','GCTEGammas'),
    cut = cms.string("pt > 5"),
    name = cms.string("L1EGbarrel"),
    doc = cms.string("standalone EG barrel"),
    # singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1P3Vars,
        ### FIXME
        ### This only works when using each collection barrel/endcap separately with the SimpleTriggerL1EGFlatTableProducer -> Need to fix this !
        hwQual = Var("hwQual",int,doc="hardware qual"),
        # quality WPs, see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePhysicsCutParser#Suppported_operators_and_functio
        saId  = Var("test_bit(hwQual(),0)", bool, doc = "standalone ID, bit 0 of hwQual"),
        eleId = Var("test_bit(hwQual(),1)", bool, doc = "electron ID, bit 1 of hwQual"),
        phoId = Var("test_bit(hwQual(),2)", bool, doc = "photon ID, bit 2 of hwQual"),
    )
)

staEGeeTable =  staEGebTable.clone(
    src = cms.InputTag('l1tLayer2EG','L1CtEgEE'),
    name = cms.string("L1EGendcap"),
    doc = cms.string("standalone EG endcap"),
)

### Muons

staMuTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag('l1tSAMuonsGmt','promptSAMuons'),
    name = cms.string("L1gmtMuon"),
    doc = cms.string("GMT standalone Muons"),
    cut = cms.string(""),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        # l1ObjVars,
        ### WARNING : the pt/eta/phi/vz methods give rounded results -> use the "physical" accessors
        # vz = Var("vz",float),
        chargeNoPh = Var("charge", int, doc="charge id"),

        ## physical values
        #phPt = Var("phPt()",float),
        pt  = Var("phPt()",float),
        eta = Var("phEta()",float),
        phi = Var("phPhi()",float),
        z0 = Var("phZ0()",float),
        d0 = Var("phD0()",float),
        charge  = Var("phCharge", int, doc="charge id"),

        ## hw Values
        hwPt = Var("hwPt()",int,doc="hardware pt"),
        hwEta = Var("hwEta()",int,doc="hardware eta"),
        hwPhi = Var("hwPhi()",int,doc="hardware phi"),
        hwQual = Var("hwQual()",int,doc="hardware qual"),
        hwIso = Var("hwIso()",int,doc="hardware iso"),
        hwBeta = Var("hwBeta()",int,doc="hardware beta"),

        # ## more info
        # nStubs = Var("stubs().size()",int,doc="number of stubs"),
    )
)

gmtTkMuTable = staMuTable.clone(
    src = cms.InputTag('l1tTkMuonsGmtLowPtFix','l1tTkMuonsGmtLowPtFix'),
    name = cms.string("L1gmtTkMuon"),
    doc = cms.string("GMT Tk Muons"),
)
# gmtTkMuTable.variables.nStubs = Var("stubs().size()",int,doc="number of stubs")

### Jets
sc4JetTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag('l1tSC4PFL1PuppiCorrectedEmulator'),
    cut = cms.string(""),
    name = cms.string("L1puppiJetSC4"),
    doc = cms.string("SeededCone 0.4 Puppi jet,  origin: Correlator"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1P3Vars,
        et = Var("et",float),
        # z0 = Var("vz", float, "vertex z0"), ## empty
    )
)

sc8JetTable = sc4JetTable.clone(
    src = 'l1tSC8PFL1PuppiCorrectedEmulator',
    name = "L1puppiJetSC8",
    doc = "SeededCone 0.8 Puppi jet,  origin: Correlator"
)

sc4ExtJetTable = sc4JetTable.clone(
    src = cms.InputTag('l1tSC4PFL1PuppiExtendedCorrectedEmulator'),
    name = cms.string("L1puppiExtJetSC4"),
    doc = cms.string("SeededCone 0.4 Puppi jet from extended Puppi,  origin: Correlator"),
    externalVariables = cms.PSet(
        btagScore = ExtVar(cms.InputTag("l1tBJetProducerPuppiCorrectedEmulator", "L1PFBJets"),float, doc="NNBtag score"),
    ),
)

histoJetTable = sc4JetTable.clone(
    src = cms.InputTag("l1tPhase1JetCalibrator9x9trimmed" ,   "Phase1L1TJetFromPfCandidates"),
    name = cms.string("L1puppiJetHisto"),
    doc = cms.string("Puppi Jets histogrammed 9x9, trimmed, origin: Correlator"),
)


caloJetTable = sc4JetTable.clone(
    src = cms.InputTag("l1tPhase2CaloJetEmulator","GCTJet"),
    name = cms.string("L1caloJet"),
    doc = cms.string("Calo Jets, origin: GCT"),
    cut = cms.string("pt > 5"), ## increase this to save space
)

### SUMS

puppiMetTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tMETPFProducer",""),
    name = cms.string("L1puppiMET"),
    doc = cms.string("Puppi MET, origin: Correlator"),
    singleton = cms.bool(True), # the number of entries is variable
    variables = cms.PSet(
        l1PtVars,
        et = Var("et",float)
    )
)

puppiMLMetTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tMETMLProducer",""),
    name = cms.string("L1puppiMLMET"),
    doc = cms.string("Puppi ML MET, origin: Correlator"),
    singleton = cms.bool(True), # the number of entries is variable
    variables = cms.PSet(
        l1PtVars,
        et = Var("et",float)
    )
)

sc4SumsTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tSC4PFL1PuppiCorrectedEmulatorMHT",""),
    name = cms.string("L1puppiJetSC4sums"),
    doc = cms.string("HT and MHT from SeededCone Radius 0.8 jets; idx 0 is HT, idx 1 is MHT, origin: Correlator"),
    singleton = cms.bool(False), # the number of entries is not variable
    cut = cms.string(""),
    variables = cms.PSet(
        l1PtVars,
        #ht = Var("pt[0]", float)
    )
)

histoSumsTable = sc4SumsTable.clone(
    src = cms.InputTag("l1tPhase1JetSumsProducer9x9trimmed","Sums"),
    name = cms.string("L1puppiHistoJetSums"),
    doc = cms.string("HT and MHT from histogrammed 9x9 jets, origin: Correlator"),
    )


### Taus
caloTauTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tPhase2CaloJetEmulator","GCTJet"),
    cut = cms.string("pt > 5"),
    name = cms.string("L1caloTau"),
    doc = cms.string("Calo Taus"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        pt  = Var("tauEt",  float, precision=l1_float_precision_), # Define as pt in nano, as required by menu tools downstream
        phi = Var("phi", float, precision=l1_float_precision_),
        eta = Var("eta", float, precision=l1_float_precision_),
    )
)


nnCaloTauTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tNNCaloTauEmulator","L1NNCaloTauCollectionBXV"),
    cut = cms.string("pt > 5"),
    name = cms.string("L1nnCaloTau"),
    doc = cms.string("NN Calo Taus"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1P3Vars,
        hwQual = Var("hwQual",int,doc="Tau ID working point, 90% --> 3, 95% --> 2, 99% --> 1, anything else --> 0"),
        hwIso = Var("hwIso",int,doc="Tau ID * 10E4")
    )
)

nnPuppiTauTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tNNTauProducerPuppi","L1PFTausNN"),
    cut = cms.string(""),
    name = cms.string("L1nnPuppiTau"),
    doc = cms.string("NN Puppi Taus"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1P3Vars,
        charge = Var("charge", int),
        z0 = Var("z0", float, "vertex z0"),                
        ## copy paste from old menu ntuple https://github.com/artlbv/cmssw/blob/from-CMSSW_12_5_2_patch1/L1Trigger/L1TNtuples/src/L1AnalysisPhaseIIStep1.cc#L543C1-L555C1
        chargedIso = Var("chargedIso", float),
        fullIso = Var("fullIso", float),
        id = Var("id", int),
        passLooseNN = Var("passLooseNN", int),
        passLoosePF = Var("passLoosePF", int),
        passTightPF = Var("passTightPF", int),
        passTightNN = Var("passTightNN", int),
        passLooseNNMass = Var("passLooseNNMass", int),
        passTightNNMass = Var("passTightNNMass", int),
        passMass = Var("passMass", int),
        dXY = Var("dxy", float),
    )
)

hpsTauTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1HPSPFTauEmuProducer","HPSTaus"),
    cut = cms.string(""),
    name = cms.string("L1hpsTau"),
    doc = cms.string("HPS Taus"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1P3Vars
    )
)

## L1 Objects
p2L1TablesTask = cms.Task(
    ## Muons
    gmtTkMuTable,
    staMuTable,
    ## EG
    tkEleTable,
    tkPhotonTable,
    staEGmerged, staEGTable, ## Need to run merger before Table task! Stanalone EG – not in GT yet
    staEGebTable, staEGeeTable,
    # ## jets
    sc4JetTable,
    sc8JetTable,
    sc4ExtJetTable, 
    histoJetTable,
    caloJetTable,
    # ## sums
    puppiMetTable,
    puppiMLMetTable,
    sc4SumsTable,
    histoSumsTable,
    # taus
    caloTauTable,
    nnCaloTauTable,
    nnPuppiTauTable,
    hpsTauTable,
    # GTT
    vtxTable,
    pvtxTable,
    gttTrackJetsTable,
    gttExtTrackJetsTable,
    gttEtSumTable,
    gttHtSumTable,
)

