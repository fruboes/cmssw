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
    {    
        //setBeams(PROTON, PROTON);
        setNeedsCrossSection(true);
    }


    /// @name Analysis methods
    //@{

    /// Book histograms and initialise projections before the run
    void init() {
       FinalState fs;
       addProjection(fs, "FS");
       addProjection(FastJets(fs, FastJets::ANTIKT, 0.5),"Jets");

       std::vector<double> bins;
       bins.push_back(0.0);
       bins.push_back(0.5);
       bins.push_back(1.0);
       bins.push_back(1.5);
       bins.push_back(2.0);
       bins.push_back(2.5);
       bins.push_back(3.0);
       bins.push_back(3.5);
       bins.push_back(4.0);
       bins.push_back(4.5);
       bins.push_back(5.0);
       bins.push_back(5.5);
       bins.push_back(6.0);
       bins.push_back(7.0);
       bins.push_back(8.0);
       bins.push_back(9.4);

      // note: order defined in do.py
      //  todoCatAll = ["InclusiveBasic", "InclusiveAsym", "InclusiveWindow", "MNBasic", "MNAsym", "MNWindow"]
      _anaTypes.push_back("InclusiveBasic");
      _anaTypes.push_back("InclusiveAsym");
      _anaTypes.push_back("InclusiveWindow");
      _anaTypes.push_back("MNBasic");
      _anaTypes.push_back("MNAsym");
      _anaTypes.push_back("MNWindow");
      for (size_t iAna = 0; iAna < _anaTypes.size(); ++iAna){
          std::string aType = _anaTypes.at(iAna);
          _histos[aType] = bookHisto1D(iAna+1, 1, 1);
          _histos[aType+"Unit"] = bookHisto1D(iAna+11,1,1);
          //_histos[aType] = bookHisto1D(aType, bins);
          //_histos[aType+"Unit"] = bookHisto1D(aType+"Unit", bins);
          //
      }
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
            // why crash?
            //std::copy_if (jets.begin(), jets.end(), jetsCopy.begin(), [](  Jet  j){ return j.momentum().pt() < 55.;} );
            for (size_t iJet = 0; iJet < jets.size();++iJet){
                if (jets.at(iJet).momentum().pt() < 55) jetsCopy.push_back(jets.at(iJet));
            }
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
                        //std::cout << "Warning: not known analysis type " << aType << std::endl;
                    }

              }
          }
          for (size_t ideta = 0; ideta < dEtas.size(); ++ideta){
                _histos[aType]->fill(dEtas.at(ideta),  weight);
                _histos[aType+"Unit"]->fill(dEtas.at(ideta),  weight);
                //std::cout << aType << " " << dEtas.at(ideta) << " " << weight << std::endl;
          }
          // */
      }  
    }

    /// Normalise histograms etc., after the run
    void finalize() {

      std::cout << "Got xs: " << crossSection() << std::endl;
      for (size_t iAna = 0; iAna < _anaTypes.size(); ++iAna){
          std::string aType = _anaTypes.at(iAna);
          scale(_histos[aType], crossSection()/sumOfWeights());
          normalize(_histos[aType+"Unit"]);
      }
    }

    //@}


  private:

    // Data members like post-cuts event weight counters go here


    /// @name Histograms
    //@{
    std::map<std::string, Histo1DPtr> _histos;

    std::vector<std::string> _anaTypes;
    //@}


  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(CMS_2015_FWD071);

}
