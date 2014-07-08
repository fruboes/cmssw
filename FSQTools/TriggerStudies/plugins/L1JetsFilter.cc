// -*- C++ -*-
//
// Package:    FSQTools/L1JetsFilter
// Class:      L1JetsFilter
// 
/**\class L1JetsFilter L1JetsFilter.cc FSQTools/L1JetsFilter/plugins/L1JetsFilter.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Tomasz Fruboes
//         Created:  Tue, 08 Jul 2014 07:57:36 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

//
// class declaration
//

class L1JetsFilter : public edm::EDFilter {
   public:
      explicit L1JetsFilter(const edm::ParameterSet&);
      ~L1JetsFilter();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual bool filter(edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      
};

L1JetsFilter::L1JetsFilter(const edm::ParameterSet& iConfig)
{

}


L1JetsFilter::~L1JetsFilter()
{
 

}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
L1JetsFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   return true;
}

// ------------ method called once each job just before starting event loop  ------------
void 
L1JetsFilter::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
L1JetsFilter::endJob() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
L1JetsFilter::beginRun(edm::Run const&, edm::EventSetup const&)
{ 
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
L1JetsFilter::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
L1JetsFilter::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
L1JetsFilter::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1JetsFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(L1JetsFilter);
