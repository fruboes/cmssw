// -*- C++ -*-

#include "Rivet/Analysis.hh"
#include "Rivet/RivetAIDA.hh"
#include "Rivet/Tools/Logging.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/InvMassFinalState.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"


namespace Rivet {
  
  
  class CMS_TMF_14_123 : public Analysis {
  public:
    
    CMS_TMF_14_123()
      : Analysis("CMS_TMF_14_123")
    {
      setBeams(PROTON, PROTON);
      setNeedsCrossSection(true);
    }
    
    
    /// Book histograms and initialise projections before the run
    void init() override {
      
        FinalState fs;
        addProjection(fs, "FS");
        addProjection(FastJets(fs, FastJets::ANTIKT, 0.5),"Jets");
      
      _hHasJet3  = bookHistogram1D("hasJet3", 1, -0.5, 0.5);
      _hHasJet4  = bookHistogram1D("hasJet4", 1, -0.5, 0.5);
      _hHasJet8  = bookHistogram1D("hasJet8", 1, -0.5, 0.5);
      _hHasJet14  = bookHistogram1D("hasJet14", 1, -0.5, 0.5);
      _hHasDJet30  = bookHistogram1D("hasDJet30", 1, -0.5, 0.5);
      _hHasDJet40  = bookHistogram1D("hasDJet40", 1, -0.5, 0.5);
      _hHasDJet80  = bookHistogram1D("hasDJet80", 1, -0.5, 0.5);
      _hHasDJet140  = bookHistogram1D("hasDJet140", 1, -0.5, 0.5);

    } 



    void analyze(const Event& event) override {
      const double weight = event.weight();
      //Obtain the jets.
      float hardestJet = 0;
      float hardestTag = -1;
      float hardestProbe = -1;
      foreach (const Jet& j, applyProjection<FastJets>(event, "Jets").jetsByPt(3.0*GeV, -5, 5, RAPIDITY)) {
            const double jpt = j.momentum().pT();
            if (jpt > hardestJet) hardestJet = jpt;
            const double eta = std::abs(j.momentum().eta());
            if (eta< 1.4 && jpt > hardestTag) hardestTag = jpt;
            if (eta > 2.8 && eta <  5 && jpt > hardestProbe) hardestProbe = jpt;
      }
      if (hardestTag >0 && hardestProbe >0){
        float ptAve = (hardestTag+hardestProbe)/2;
        if (ptAve > 30) _hHasDJet30->fill(0, weight);
        if (ptAve > 40) _hHasDJet40->fill(0, weight);
        if (ptAve > 80) _hHasDJet80->fill(0, weight);
        if (ptAve > 140) _hHasDJet140->fill(0, weight);
      }

      if (hardestJet>3) _hHasJet3->fill(0, weight);
      if (hardestJet>4) _hHasJet4->fill(0, weight);
      if (hardestJet>8) _hHasJet8->fill(0, weight);
      if (hardestJet>14) _hHasJet14->fill(0, weight);

    }
    
    
    /// Normalise histograms etc., after the run
    void finalize() override {
        scale(_hHasJet3, crossSection()/sumOfWeights()); //# norm to cross section
        scale(_hHasJet4, crossSection()/sumOfWeights()); //# norm to cross section
        scale(_hHasJet8, crossSection()/sumOfWeights()); //# norm to cross section
        scale(_hHasJet14, crossSection()/sumOfWeights()); //# norm to cross section
        scale(_hHasDJet30, crossSection()/sumOfWeights()); //# norm to cross section
        scale(_hHasDJet40, crossSection()/sumOfWeights()); //# norm to cross section
        scale(_hHasDJet80, crossSection()/sumOfWeights()); //# norm to cross section
        scale(_hHasDJet140, crossSection()/sumOfWeights()); //# norm to cross section



    }

  private:

    AIDA::IHistogram1D*  _hHasJet3;
    AIDA::IHistogram1D*  _hHasJet4;
    AIDA::IHistogram1D*  _hHasJet8;
    AIDA::IHistogram1D*  _hHasJet14;
    AIDA::IHistogram1D* _hHasDJet30;
    AIDA::IHistogram1D* _hHasDJet40;
    AIDA::IHistogram1D* _hHasDJet80;
    AIDA::IHistogram1D* _hHasDJet140;
  };
  
  AnalysisBuilder<CMS_TMF_14_123> plugin_CMS_TMF_14_123;
  
}

