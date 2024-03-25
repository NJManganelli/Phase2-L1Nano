import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.l1trig_cff import *

#### GTT Converted Tracks
gttTracksTable = cms.EDProducer(
    # "SimpleCandidateFlatTableProducer",
    "SimpleL1TTTrackCandidateFlatTableProducer", ## note the use of a dedicated table producer which is defined in the plugins/L1TableProducer.cc
    src = cms.InputTag('l1tGTTInputProducer','Level1TTTracksConverted'),
    cut = cms.string(""),
    name = cms.string("L1GTTTrack"),
    doc = cms.string("GTT Converted Tracks storing pt and eta in place of Rinv and tanL"),
    singleton = cms.bool(False), # the number of entries is variable
    variables = cms.PSet(
        rInv = Var("rInv()", float, doc="rInv"),
        pt = Var("momentum().perp()", float, doc="pt"),
        eta = Var("eta()", float, doc="eta"),
        phi = Var("phi()", float, doc="phi"),
        localPhi = Var("localPhi()", float, doc="local phi"),
        tanL = Var("tanL()", float, doc="tanL"),
        z0 = Var("z0()", float, doc="z0"),
        d0 = Var("d0()", float, doc="d0"),
        trkMVA1 = Var("trkMVA1()", float, doc="track MVA1"),
        trkMVA2 = Var("trkMVA2()", float, doc="track MVA2"),
        trkMVA3 = Var("trkMVA3()", float, doc="track MVA3"),
        hitPattern = Var("hitPattern()", "uint", doc="hit pattern"),
        chi2XYRed = Var("chi2XYRed()", float, doc="chi2XYRed"),
        chi2ZRed = Var("chi2ZRed()", float, doc="chi2ZRed"),
        # chi2BendRed = Var("chi2BendRed()", float, doc="chi2BendRed"),
        phiSector = Var("phiSector()", "uint", doc = "phi sector number"),
        etaSector = Var("etaSector()", "uint", doc = "eta sector number"),
        hwValid = Var("getValidBits()", "uint", doc = "hardware vertex valid bit"),
        hwPt = Var("getRinvBits()", "uint", doc = "hardware pt after GTT conversion"),
        hwEta = Var("getTanlBits()", "uint", doc = "hardware eta after GTT conversion"),
        hwPhi = Var("getPhiBits()", "uint", doc = "hardware phi"),
        hwZ0 = Var("getZ0Bits()", "uint", doc = "hardware z0"),
        hwD0 = Var("getD0Bits()", "uint", doc = "hardware d0"),
        hwChi2RPhi = Var("getChi2RPhiBits()", "uint", doc = "hardware Chi2RPhi"),
        hwChi2RZ = Var("getChi2RZBits()", "uint", doc = "hardware Chi2RZ"),
        hwBendChi2 = Var("getBendChi2Bits()", "uint", doc = "hardware BendChi2"),
        hwHitPattern = Var("getHitPatternBits()", "uint", doc = "hardware HitPattern"),
        hwMVAQuality = Var("getMVAQualityBits()", "uint", doc = "hardware MVA Quality, corresponding to trkMVA1"),
        hwMVAOther = Var("getMVAOtherBits()", "uint", doc = "hardware MVA Other, reserved for trkMVA2 and trkMVA3"),
     )
 )

gttExtTracksTable = gttTracksTable.clone(
    src = cms.InputTag('l1tGTTInputProducerExtended','Level1TTTracksExtendedConverted'),
    name = cms.string("L1GTTExtTrack"),
    doc = cms.string("GTT Extended Tracks storing pt and eta in place of Rinv and tanL"),
)

# gttTrackJetsTable = cms.EDProducer(
#     "SimpleL1TkJetWordCandidateFlatTableProducer",
#     src = cms.InputTag("l1tGTTInputProducer","L1TrackJets"),
#     name = cms.string("L1TrackJet"),
#     doc = cms.string("GTT Track Jets"),
#     singleton = cms.bool(False), # the number of entries is variable
#     variables = cms.PSet(
#         pt = Var("pt()", float, doc="pt"),
#         eta = Var("glbeta()", float, doc="eta"),
#         phi = Var("glbphi()", float, doc="phi"),
#         z0 = Var("z0()", float, doc="z0"), 
#         hwPt = Var("ptBits()", "uint", doc="hardware pt"),
#         hwEta = Var("glbEtaBits()", "uint", doc="hardware eta"),
#         hwPhi = Var("glbPhiBits()", "uint", doc="hardware eta"),
#         hwZ0 = Var("z0Bits()", "uint", doc="hardware z0"),
#         hwNTracks = Var("ntBits()", "uint", doc="hardware number of tracks"),
#         hwNDisplacedTracks = Var("xtBits()", "uint", doc="hardware number of tracks"),
#         hwDisplacedFlagBits = Var("dispFlagBits()", "uint", doc="hardware displaced flag bits"),
#         # hwWordA = Var("tkJetWord().range(31, 0).to_uint()", "uint", doc = "hardware track jet word first 32 bits"),
#         # hwWordB = Var("tkJetWord().range(63, 32).to_uint()", "uint", doc = "hardware track jet word second 32 bits"),
#         # hwWordC = Var("tkJetWord().range(95, 64).to_uint()", "uint", doc = "hardware track jet word third 32 bits"),
#         # hwWordD = Var("tkJetWord().range(127, 96).to_uint()", "uint", doc = "hardware track jet word fourth 32 bits"),
#     )
# )


p2L1GTTTkTpTask = cms.Task(
    gttTracksTable,
)

