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

#include "DataFormats/L1Trigger/interface/L1JetParticleFwd.h"
#include "DataFormats/L1Trigger/interface/L1JetParticle.h"
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
      float m_maxEta;
      float m_minEta;
      float m_minPt;
      int m_minNum;
      
};

L1JetsFilter::L1JetsFilter(const edm::ParameterSet& iConfig)
{
        m_maxEta = iConfig.getParameter<double>("maxEta");
        m_minEta = iConfig.getParameter<double>("minEta");
        m_minPt = iConfig.getParameter<double>("minPt");
        m_minNum = iConfig.getParameter<int>("minNum");

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
    std::vector<edm::InputTag> todo;
    todo.push_back(edm::InputTag("l1extraParticles", "Central"));
    todo.push_back(edm::InputTag("l1extraParticles", "Forward"));
    todo.push_back(edm::InputTag("l1extraParticles", "Tau"));

    //std::vector<reco::Candidate::LorentzVector> momenta;
    int cnt = 0;
    for (unsigned int i = 0; i < todo.size();++i){
        edm::Handle<std::vector<l1extra::L1JetParticle> > hL1;
        iEvent.getByLabel(todo.at(i), hL1);
        for (unsigned iL1 = 0; iL1< hL1->size();++iL1){
            if (hL1->at(iL1).bx()!=0) continue;
            //momenta.push_back(hL1->at(iL1).p4());
            float pt = std::abs(hL1->at(iL1).pt());
            if (pt < m_minPt) continue;
            float eta = hL1->at(iL1).eta();
            if (eta > m_maxEta) continue;
            if (eta < m_minEta) continue;
            ++cnt;
        }
    }
    if (cnt < m_minNum) return false;
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
