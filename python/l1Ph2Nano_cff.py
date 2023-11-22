import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.common_cff import *

## Import GT scales for HW to physical value conversion
from L1Trigger.Phase2L1GT.l1tGTScales import scale_parameter

## Inspired by:
## FastPUPPI ntupler https://github.com/p2l1pfp/FastPUPPI/blob/12_5_X/NtupleProducer/python/runPerformanceNTuple.py
## https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCandidateModules#Merging_Candidate_Collections

##################################################################
### This part can be taken from l1trig_cff starting from 13X
## from PhysicsTools.NanoAOD.l1trig_cff import *

l1_float_precision_=16

l1PtVars = cms.PSet(
    pt  = Var("pt",  float, precision=l1_float_precision_),
    phi = Var("phi", float, precision=l1_float_precision_),
)
l1P3Vars = cms.PSet(
    l1PtVars,
    eta = Var("eta", float, precision=l1_float_precision_),
)

l1ObjVars = cms.PSet(
    l1P3Vars,
    hwPt = Var("hwPt()",int,doc="hardware pt"),
    hwEta = Var("hwEta()",int,doc="hardware eta"),
    hwPhi = Var("hwPhi()",int,doc="hardware phi"),
    hwQual = Var("hwQual()",int,doc="hardware qual"),
    hwIso = Var("hwIso()",int,doc="hardware iso")
)

l1GTObjVars = cms.PSet(
    l1P3Vars,
)
### This above part can be taken from l1trig_cff starting from 13X
##################################################################

### Tables definitions

### Vertex

gtVtxTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag('l1tGTProducer','GTTPrimaryVert'),
    cut = cms.string(""),
    name = cms.string("L1GTVertex"),
    doc = cms.string("GT GTT Vertices"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        z0 = Var("vz",float, doc = "primary vertex position z coordinate"),
        # sumPt = Var("hwSum_pT_pv_toInt()*0.25",float, doc = "sum pt of tracks"),
        ## hw vars
        hwZ0 = Var("hwZ0_toInt()",int, doc = "HW primary vertex position z coordinate"),
        # hwSum_pT_pv = Var("hwSum_pT_pv_toInt()",int, doc = "HW sum pt of tracks"),
    )
)

### Store Primary Vertex only (first vertex)
gtPvTable = gtVtxTable.clone(
    name = cms.string("L1GTPV"),
    doc = cms.string("GT GTT Leading Primary Vertex"),
    maxLen = cms.uint32(1),
)

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
    # "SimpleCandidateFlatTableProducer",
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

gttEtSumTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tTrackerEmuEtMiss", "L1TrackerEmuEtMiss"),
    name = cms.string("L1TrackMET"),
    doc = cms.string("GTT Track MET"),
    singleton = cms.bool(True), # the number of entries is variable
    variables = cms.PSet(
        # pt = Var("pt", float, doc="MET pt"),
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
        ht = Var(f"p4().energy()", float, doc="HT"),
    )
)

### Store Primary Vertex only (first vertex)
pvtxTable = vtxTable.clone(
    maxLen = cms.uint32(1),
    name = cms.string("L1PV"),
    doc = cms.string("GTT Leading Primary Vertex"),
)

### GT
gtTkPhoTable =cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag('l1tGTProducer','CL2Photons'),
    name = cms.string("L1GTtkPhoton"),
    doc = cms.string("GT tkPhotons"),
    cut = cms.string(""),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1GTObjVars,
        ## hw values
        # hwPt = Var("hwPT_toInt()",int,doc="hardware pt"),
        hwQual = Var("hwQual_toInt()",int),
        hwIso = Var("hwIso_toInt()",int),
        ## more physical values
        ## using the GT scales for HW to physicsal vonversion, see scales in https://github.com/cms-sw/cmssw/blob/master/L1Trigger/Phase2L1GT/python/l1tGTScales.py
        iso = Var(f"hwIso_toInt()*{scale_parameter.isolation_lsb.value()}",float, doc = "absolute isolation"),
        relIso = Var(f"hwIso_toInt()*{scale_parameter.isolation_lsb.value()} / pt",float, doc = "relative isolation")
    )
)

gtTkEleTable = gtTkPhoTable.clone(
    src = cms.InputTag('l1tGTProducer','CL2Electrons'),
    name = cms.string("L1GTtkElectron"),
    doc = cms.string("GT tkElectrons"),
)

### FIXME
# gtTkEleTable.variables.z0 = Var("vz",float) ## this is the correct line
gtTkEleTable.variables.z0 = Var("vz / 2.",float) ### FIXME -> change done due to ap_fix type mismatch
### FIXME

gtTkEleTable.variables.charge = Var("charge", int, doc="charge id")
gtTkEleTable.variables.hwZ0 = Var("hwZ0_toInt()",int)

gtTkMuTable = gtTkEleTable.clone(
    src = cms.InputTag('l1tGTProducer','GMTTkMuons'),
    name = cms.string("L1GTgmtTkMuon"),
    doc = cms.string("GT GMT tkMuon"),
)
gtTkMuTable.variables.z0 = Var("vz",float)
# ### FIXME GMT uses the opposite definition of charge than GT and CTL2
gtTkMuTable.variables.charge = Var("-charge", int, doc="charge id")
# ### FIXME

gtSCJetsTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag('l1tGTProducer','CL2Jets'),
    cut = cms.string(""),
    name = cms.string("L1GTscJet"),
    doc = cms.string("GT CL2Jets: seededCone Puppi Jets"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1GTObjVars,
        z0 = Var("vz",float),
    )
)

gtNNTauTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag('l1tGTProducer','CL2Taus'),
    cut = cms.string(""),
    name = cms.string("L1GTnnTau"),
    doc = cms.string("GT CL2Taus: NN puppi Taus"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1GTObjVars,
        #z0 = Var(f"hwSeed_z0_toInt()*{scale_parameter.seed_z0_lsb.value()}",float, doc = "z0"),
        ### FIXME
        ### MANUAL HACK to fix the GT tau z0 scale and also the factor 2 due to wrong ap_type -> FIXME
        z0 = Var("hwSeed_z0_toInt() * (1/40.)",float, doc = "z0"),
        ### FIXME
        hwZ0 = Var(f"hwSeed_z0_toInt()",int, doc = "hwZ0"),
    )
)

gtEtSumTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag('l1tGTProducer','CL2EtSum'),
    name = cms.string("L1GTpuppiMET"),
    doc = cms.string("GT CL2EtSum"),
    singleton = cms.bool(True), # the number of entries is variable
    variables = cms.PSet(
        pt = Var("pt", float, doc="MET pt"),
        phi = Var("phi", float, doc="MET phi"),
    )
)

gtHtSumTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag('l1tGTProducer','CL2HtSum'),
    name = cms.string("L1GTscJetSum"),
    doc = cms.string("GT CL2HtSum"),
    singleton = cms.bool(True), # the number of entries is variable
    variables = cms.PSet(
        # l1GTObjVars,
        mht = Var("pt", float, doc="MHT pt"),
        mhtPhi = Var("phi", float, doc="MHT phi"),
        ht = Var(f"hwSca_sum_toInt()*{scale_parameter.sca_sum_lsb.value()}", float, doc="HT"), ## HACK via hw value!
    )
)

#### EG
tkPhotonTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag('l1tLayer2EG','L1CtTkEm'),
    cut = cms.string(""),
    name = cms.string("L1tkPhoton"),
    doc = cms.string("Tk Photons (EM)"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1ObjVars,
        charge = Var("charge", int, doc="charge"),
        ## FIXME GT uses the PV iso in 133pre2
        relIso = Var("trkIsolPV", float, doc = "relative Isolation"),
        ## FIXME
        tkIso   = Var("trkIsol", float),
        tkIsoPV  = Var("trkIsolPV", float),
        pfIso   = Var("pfIsol", float),
        puppiIso  = Var("puppiIsol", float),
        ## quality WPs, see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePhysicsCutParser#Suppported_operators_and_functio
        saId  = Var("test_bit(hwQual(),0)", bool),
        eleId = Var("test_bit(hwQual(),1)", bool),
        phoId = Var("test_bit(hwQual(),2)", bool),
    )
)

tkEleTable = tkPhotonTable.clone(
    src = cms.InputTag('l1tLayer2EG','L1CtTkElectron'),
    name = cms.string("L1tkElectron"),
    doc = cms.string("Tk Electrons"),
)
tkEleTable.variables.z0     = Var("trkzVtx", float, "track vertex z0")
tkEleTable.variables.charge = Var("charge", int, doc="charge")
tkEleTable.variables.relIso = Var("trkIsol", float, doc = "relative Isolation") ### FIXME overwriting the relIso variable for now as the GT photon uses the wrong one

## from https://github.com/p2l1pfp/FastPUPPI/blob/12_5_X/NtupleProducer/python/runPerformanceNTuple.py#L499C8-L501C83
tkEleTable.variables.tkEta = Var("trkPtr.eta", float,precision=8)
tkEleTable.variables.tkPhi = Var("trkPtr.phi", float,precision=8)
tkEleTable.variables.tkPt = Var("trkPtr.momentum.perp", float,precision=8)

# tkEleTable.variables.charge3 = Var("charge()", int, doc="charge")
# tkEleTable.variables.charge0 = Var("? trackCurvature() > 0 ? 1 : -1", int, doc="charge")
# tkEleTable.variables.charge1 = Var("? trackCurvature() ? 1 : -1", int, doc="charge")
# tkEleTable.variables.charge2 = Var("pow(-1,trackCurvature())", int, doc="charge2")
# tkEleTable.variables.trackCurvature = Var("trackCurvature()", int, doc="trackCurvature")
# tkEleTable.variables.trackCurvature2 = Var("trackCurvature", int, doc="trackCurvature")

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
    cut = cms.string(""),
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
    cut = cms.string(""),
    name = cms.string("L1EGbarrel"),
    doc = cms.string("standalone EG barrel"),
    # singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1P3Vars,

        ### FIXME
        ### This only works when using each collection barrel/endcap separately with the SimpleTriggerL1EGFlatTableProducer -> Need to fix this !
        hwQual = Var("hwQual",int,doc="hardware qual"),
        # quality WPs, see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePhysicsCutParser#Suppported_operators_and_functio
        saId  = Var("test_bit(hwQual(),0)", bool),
        eleId = Var("test_bit(hwQual(),1)", bool),
        phoId = Var("test_bit(hwQual(),2)", bool),
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
    name = cms.string("L1StaMu"),
    doc = cms.string("GMT STA Muons"),
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
scJetTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag('l1tSCPFL1PuppiCorrectedEmulator'),
    cut = cms.string(""),
    name = cms.string("L1scJet"),
    doc = cms.string("SeededCone 0.4 Puppi jet"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1P3Vars,
        et = Var("et",float),
        z0 = Var("vz", float, "vertex z0"), ## empty
    )
)

scExtJetTable = scJetTable.clone(
    src = cms.InputTag('l1tSCPFL1PuppiExtendedCorrectedEmulator'),
    name = cms.string("L1scExtJet"),
    doc = cms.string("SeededCone 0.4 Puppi jet from extended Puppi"),
    externalVariables = cms.PSet(
        btagScore = ExtVar(cms.InputTag("l1tBJetProducerPuppiCorrectedEmulator", "L1PFBJets"),float, doc="NNBtag score"),
    ),
)

histoJetTable = scJetTable.clone(
    src = cms.InputTag("l1tPhase1JetCalibrator9x9trimmed" ,   "Phase1L1TJetFromPfCandidates"),
    name = cms.string("L1histoJet"),
    doc = cms.string("Puppi Jets 9x9"),
)


caloJetTable = scJetTable.clone(
    src = cms.InputTag("l1tCaloJet","L1CaloJetCollectionBXV"),
    name = cms.string("L1caloJet"),
    doc = cms.string("Calo Jets"),
    cut = cms.string("pt > 30"), ## increase this to save space
)

### SUMS

puppiMetTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tMETPFProducer",""),
    name = cms.string("L1puppiMET"),
    doc = cms.string("Puppi MET"),
    variables = cms.PSet(
        l1PtVars,
        et = Var("et",float)
    )
)

seededConeSumsTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tSCPFL1PuppiCorrectedEmulatorMHT",""),
    name = cms.string("L1scJetSum"),
    doc = cms.string("HT and MHT from SeededCone jets; idx 0 is HT, idx 1 is MHT"),
    singleton = cms.bool(False), # the number of entries is variable
    cut = cms.string(""),
    variables = cms.PSet(
        l1PtVars,
        #ht = Var("pt[0]", float)
    )
)

histoSumsTable = seededConeSumsTable.clone(
    src = cms.InputTag("l1tPhase1JetSumsProducer9x9trimmed","Sums"),
    name = cms.string("L1histoHTMHT"),
    doc = cms.string("HT and MHT from histogrammed jets"),
    )


### Taus
caloTauTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tCaloJet","L1CaloTauCollectionBXV"),
    cut = cms.string("pt > 20"),
    name = cms.string("L1caloTau"),
    doc = cms.string("Calo Taus"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1P3Vars,
    )
)

nnTauTable = cms.EDProducer(
    "SimpleCandidateFlatTableProducer",
    src = cms.InputTag("l1tNNTauProducerPuppi","L1PFTausNN"),
    cut = cms.string(""),
    name = cms.string("L1nnTau"),
    doc = cms.string("NN Taus"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        l1P3Vars,
        charge = Var("charge", int),
        z0 = Var("z0", float, "vertex z0"),                
        ## copy paste from old menu ntuple https://github.com/artlbv/cmssw/blob/from-CMSSW_12_5_2_patch1/L1Trigger/L1TNtuples/src/L1AnalysisPhaseIIStep1.cc#L543C1-L555C1
        chargedIso = Var("chargedIso", int),
        fullIso = Var("fullIso", int),
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

## GTT Track Objects (except Vertices)
p2GTTL1TablesTask = cms.Task(
    gttEtSumTable,
    gttHtSumTable,
    gttTrackJetsTable,
)

## GT objects
p2GTL1TablesTask = cms.Task(
    gtTkPhoTable,
    gtTkEleTable,
    gtTkMuTable,
    gtSCJetsTable,
    gtNNTauTable,
    gtEtSumTable,
    gtHtSumTable,
    gtVtxTable,
    gtPvTable,
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
    scJetTable,
    scExtJetTable, 
    histoJetTable,
    caloJetTable,
    # ## sums
    puppiMetTable,
    seededConeSumsTable,
    histoSumsTable,
    # taus
    caloTauTable,
    nnTauTable,
    # GTT
    vtxTable,
    pvtxTable,
)

# ## Add GT ntuple to L1Task
p2L1TablesTask.add(p2GTL1TablesTask)
p2L1TablesTask.add(p2GTTL1TablesTask)

# ## FOR GT vs L1 COMPARISON we order the tables like below
# p2L1TablesTask = cms.Task(
#     gtTkPhoTable,tkPhotonTable,
#     gtTkEleTable,tkEleTable,
#     gtTkMuTable, gmtTkMuTable,
#     gtSCJetsTable,scJetTable,
#     gtNNTauTable,nnTauTable,
#     gtEtSumTable,puppiMetTable,
#     gtHtSumTable,seededConeSumsTable,
#     gtVtxTable,vtxTable,
#     gtPvTable,pvtxTable,
# )

#### GENERATOR INFO
from PhysicsTools.NanoAOD.genparticles_cff import *
from PhysicsTools.NanoAOD.jetMC_cff import *
from PhysicsTools.NanoAOD.met_cff import metMCTable
## PU
from PhysicsTools.NanoAOD.globals_cff import puTable
## Gen taus?
from PhysicsTools.NanoAOD.taus_cff import *

## based on https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/nanogen_cff.py#L2-L36

p2L1TablesTask.add(
    genParticleTask,
    genParticleTablesTask,
    genJetTable,
    patJetPartonsNano,
    genJetFlavourAssociation,
    genJetFlavourTable,
    metMCTable,
    puTable,
    genTauTask,
)
