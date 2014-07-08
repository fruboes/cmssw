import FWCore.ParameterSet.Config as cms

def l1menuworkaround(process, path, l1filter):
    import FWCore.ParameterSet.SequenceTypes as st
    if not hasattr(process, "dummyFilter"):
        dummy = cms.EDFilter("L1DummyFilter")
        setattr(process, "dummyFilter", dummy)

    for a in dir(process):
        if a != path: continue
        path = getattr(process, a)
        if type(path) == st.Path:
            moduleNames = path._seq.__str__().split("+")
            replacementsDone = 0
            for m in moduleNames:
                m = m.replace("cms.ignore(","").replace(")", "").replace("~","")
                module = getattr(process, m)
                if module.type_() == "HLTLevel1GTSeed":
                    if replacementsDone == 0:
                        path.replace(module, l1filter)
                    else:
                        path.replace(module, getattr(process, "dummyFilter"))
                    replacementsDone += 1

    return process

