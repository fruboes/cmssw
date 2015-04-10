// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"

/// @todo Include more projections as required, e.g. ChargedFinalState, FastJets, ZFinder...

namespace Rivet {

  using namespace Cuts;

  class CMS_2015_FWD071 : public Analysis {
  public:

    /// Constructor
    CMS_2015_FWD071()
      : Analysis("CMS_2015_FWD071")
    {    }


    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {
        FinalState fs;
        addProjection(fs, "FS");
        addProjection(FastJets(fs, FastJets::ANTIKT, 0.5),"Jets");

      /// @todo Initialise and register projections here

      /// @todo Book histograms here, e.g.:
      // _h_XXXX = bookProfile1D(1, 1, 1);
      // _h_YYYY = bookHisto1D(2, 1, 1);

    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();
      std::cout << "W "<< weight << std::endl;
      foreach (const Jet& j, applyProjection<FastJets>(event, "Jets").jetsByPt(35*GeV)) {
            const double eta = std::abs(j.momentum().eta());
            if (eta > 4.7) continue;
            const double pt = j.momentum().pt();
            std::cout << "jet " << eta << " " << pt << std::endl;
      }


      /// @todo Do the event by event analysis here

    }


    /// Normalise histograms etc., after the run
    void finalize() {

      /// @todo Normalise, scale and otherwise manipulate histograms here

      // scale(_h_YYYY, crossSection()/sumOfWeights()); // norm to cross section
      // normalize(_h_YYYY); // normalize to unity

    }

    //@}


  private:

    // Data members like post-cuts event weight counters go here


    /// @name Histograms
    //@{
    Profile1DPtr _h_XXXX;
    Histo1DPtr _h_YYYY;
    //@}


  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(CMS_2015_FWD071);

}
