// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Tools/ParticleIdUtils.hh"
#include <algorithm> 

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
      //
      _anaTypes.push_back("InclusiveBasic");
      _anaTypes.push_back("InclusiveAsym");
      _anaTypes.push_back("InclusiveWindow");
      _anaTypes.push_back("MNBasic");
      _anaTypes.push_back("MNAsym");
      _anaTypes.push_back("MNWindow");
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const double weight = event.weight();

      //std::vector<const Jet *> jets; for some reasone gives me pure virtual calls...
      std::vector<Jet> jets;
      foreach (const Jet& j, applyProjection<FastJets>(event, "Jets").jetsByPt(35*GeV)) {
            const double eta = std::abs(j.momentum().eta());
            if (eta > 4.7) continue;
            const double pt = j.momentum().pt();
            if (pt < 35) continue; // just in case...
            jets.push_back(Jet(j));
      }

      for (size_t iAna = 0; iAna < _anaTypes.size(); ++iAna){
          std::vector<Jet> jetsCopy;
          std::string aType = _anaTypes.at(iAna);
          if (aType == "InclusiveWindow" || aType == "MNWindow") {
            //std::copy_if (jets.begin(), jets.end(), jetsCopy.begin(), [](  Jet  j){ return j.momentum().pt() < 55.;} );
          } else {
            jetsCopy.insert(jetsCopy.begin(), jets.begin(), jets.end());
          }

          //*  
          std::vector<float> dEtas; 
          for (size_t iJet = 0; iJet < jetsCopy.size(); ++iJet){
              for (size_t jJet = iJet+1; jJet < jetsCopy.size(); ++jJet){
                    if (iJet == jJet) continue;
                    float etaI = jetsCopy.at(iJet).momentum().eta();
                    float etaJ = jetsCopy.at(jJet).momentum().eta();
                    float deta = std::fabs(etaI-etaJ);
                    float ptI = jetsCopy.at(iJet).momentum().pt();
                    float ptJ = jetsCopy.at(jJet).momentum().pt();
                    // note: for the window category we have allready filtered all above 55.
                    if (aType == "InclusiveWindow" || aType == "InclusiveBasic" 
                        || (aType == "InclusiveAsym" && std::max(ptI,ptJ)>45.) ) {
                        dEtas.push_back(deta);
                    } 
                    else if (aType == "MNWindow" || aType == "MNBasic"  
                             || (aType == "MNAsym" && std::max(ptI,ptJ)>45. )) {
                        if (dEtas.size() == 0) {
                            dEtas.push_back(deta);
                        } else if (dEtas.at(0) < deta){
                            dEtas.at(0) = deta;
                        }
                    } 
                    // error msg flood should be enough to catch attention..
                    else {
                        std::cout << "Warning: not known analysis type " << aType << std::endl;
                    }

              }
          }
          for (size_t ideta = 0; ideta < dEtas.size(); ++ideta){
                // Fill(dEtas.at(ideta),  weight)
                std::cout << aType << " " << dEtas.at(ideta) << " " << weight << std::endl;
          }
          // */
      }  
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

    std::vector<std::string> _anaTypes;
    //@}


  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(CMS_2015_FWD071);

}
