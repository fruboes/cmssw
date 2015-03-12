# here you can write down the draw functions/sequence/stuff you want to be executed with the main DrawTool.py program.

# Set the wanted input file and load all available histograms in this file in the memory:
setInput("../test/CSA14/plotsCSA14_dndeta.root")
getAllHistos()

# define nice legend names for the samples that you are plotting:
setLegend("MinBias_TuneMonash13_13TeV-pythia8","Pythia8 Monash13")
setLegend("data_MinBias_TuneCUETP8S1-HERAPDF_13TeV-pythia8","data (CUETP8S1)")

# this will plot ALL histograms found the in the file:
#draw()
# this will plot all histograms containing the string "RecoTrack" in their names normalised to their integral:
draw(["RecoTrack"],"int")
# this will plot a combination of histograms containing either of the two strings in their names:
#draw(["ptRecoTracks_central_minbias","etaRecoTracks_central_minbias"])

# by default all histograms are not normalised
# you can optionally normalise them to their integrals (int) or to their maxima (max):
#draw(["RecoTrack"],"max")

# with this command you can perform an update action to all the ROOT canvases currently open:
#updateCanvas()


# after drawing one can save the plots as files
# by default the PDF format is chosen to save a plot
# by default they are saved in the current directory
# save all open canvases to pdf files:
saveCanvas()

# save all canvases with the string "etaRecoTrack" in their names:
#saveCanvas("./",["etaRecoTrack"])
# to save in another directory, change the path of the first argument in the above command,
# the directory needs to be an existing one

# in addition, other file formats are supported:
#saveCanvas("./",["etaRecoTrack"],["pdf","eps","png","C"])

# when you are done and you want to close the open canvases to plot other histograms
# delete all canvases from the memory (not needed when running script in batch mode):
#resetCanvas()
# you can off course also just click on a particular canvas to close it, the above function is just usefull when you have 10+ plots open or so

# when done with this file, you can reset the memory and go to another one:
# this is probably only useful when running a complicated script in batch mode
#resetHisto()
#setInput("../test/CSA14/plotsCSA14_UEAna.root")
#getAllHistos()
#draw(["RecoTrack"])
