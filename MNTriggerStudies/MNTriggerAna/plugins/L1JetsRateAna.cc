// -*- C++ -*-
//
// Package:    L1JetsRateAna
// Class:      L1JetsRateAna
// 
/**\class L1JetsRateAna L1JetsRateAna.cc MNTriggerStudies/L1JetsRateAna/plugins/L1JetsRateAna.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Tomasz Fruboes
//         Created:  Thu, 17 Apr 2014 16:06:29 GMT
// $Id$
//
//




// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TTree.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include <DataFormats/PatCandidates/interface/TriggerEvent.h>

#include "MNTriggerStudies/MNTriggerAna/interface/EventIdData.h"
#include "MNTriggerStudies/MNTriggerAna/interface/L1JetsView.h"

//
// class declaration
//

class L1JetsRateAna : public edm::EDAnalyzer {
   public:
      explicit L1JetsRateAna(const edm::ParameterSet&);
      ~L1JetsRateAna();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob();
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob();

      TTree *m_tree;
      std::vector<EventViewBase *> m_views;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
L1JetsRateAna::L1JetsRateAna(const edm::ParameterSet& iConfig)

{
    edm::Service<TFileService> tFileService;
    m_tree = tFileService->make<TTree>("data", "data");
    m_views.push_back(new EventIdData(iConfig.getParameter< edm::ParameterSet >("EventData"), m_tree));
    m_views.push_back(new GenTrackView(iConfig.getParameter< edm::ParameterSet >("L1JetsView"), m_tree));
}

L1JetsRateAna::~L1JetsRateAna() {}

void
L1JetsRateAna::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

    using namespace edm;
    for (unsigned int i = 0; i < m_views.size(); ++i){
        m_views[i]->fill(iEvent, iSetup);
    }
    m_tree->Fill();

}


// ------------ method called once each job just before starting event loop  ------------
void 
L1JetsRateAna::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
L1JetsRateAna::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
L1JetsRateAna::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
L1JetsRateAna::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
L1JetsRateAna::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
L1JetsRateAna::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1JetsRateAna::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}




//define this as a plug-in
DEFINE_FWK_MODULE(L1JetsRateAna);
