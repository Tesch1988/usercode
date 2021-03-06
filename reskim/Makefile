######################################################################
# quite generic Makefile for ROOT-based programs with automatic
# dependency scanning
#
# (C) Martin Weber 2011-2012

# Name of the executable
PROGRAM       = reskim


CMSSW_RELEASE_BASE_NOPATCH:=$(shell echo $(CMSSW_RELEASE_BASE) | sed -e 's/-patch//' -e 's/_patch.//')
CMSSW_INC:=-I$(CMSSW_RELEASE_BASE)/src -I$(CMSSW_BASE)/src
CMSSW_LIBS:=-L$(CMSSW_BASE)/lib/$(SCRAM_ARCH) -L$(CMSSW_RELEASE_BASE)/lib/$(SCRAM_ARCH) -L$(CMSSW_RELEASE_BASE)/external/$(SCRAM_ARCH)/lib -L$(CMSSW_RELEASE_BASE_NOPATCH)/lib/$(SCRAM_ARCH)
 
LHAPDF_PATH = /net/scratch_cms/institut_3a/padeken/lhapdfLib/
 
EXTLIBS     = $(CMSSW_LIBS) -L$(LHAPDF_PATH)/lib -lLHAPDF 
EXTINCDIR   = $(CMSSW_INC) -I$(LHAPDF_PATH)/include

# external includes / libraries
#CLHEP_VERSION = 2.0.2.1
#EXTINCDIR     = -I/usr/local/include/ # external header files should be here, leading slash is mandatory!
#EXTLIBS       = -L/usr/local/lib -lCLHEP-Matrix-$(CLHEP_VERSION) -lCLHEP-Vector-$(CLHEP_VERSION)

######################################################################
# You should not modify the lines below here
#

# Setup for ROOT libraries
#   @echo $(LHAPDF_PATH)
ROOTCFLAGS   := $(shell root-config --cflags)
ROOTLIBS     := $(shell root-config --libs)
ROOTGLIBS    := $(shell root-config --glibs)
# ROOTGLIBS   += -lX3d -L/net/data_cms/institut_3a/SusyWG/LHAPDF/lib
ROOTGLIBS   += -lX3d -L$(LHAPDF_PATH)/lib

# Linux with gcc / g++ / g77
FC            = g77
FCFLAGS       = -I/cern/pro/include -fPIC -fno-automatic -fdollar-ok -fno-backslash \
		-finit-local-zero -fno-second-underscore -fugly-logint -ftypeless-boz
# -pg for gprof

# top_builddir = /home/home1/institut_3a/erdweg/Desktop/Software/pdf_uncertainties/lhapdf-5.8.8/

CXX           = g++
CXXFLAGS      = -O2 -Wall -fPIC -fsignaling-nans -g # -DNDEBUG#  -pg for gprof
CXXFLAGS     += $(EXTINCDIR)   # external header files should be here
CXXFLAGS     += $(ROOTCFLAGS)

LD            = g++
LDFLAGS       = -O2 -fsignaling-nans -g -lz # -pg for gprof
LDFLAGS      += $(ROOTGLIBS)
LDFLAGS      += $(EXTLIBS)

SOURCES       = $(wildcard *.cxx)
HEADERS       = $(SOURCES:.cxx=.h)
OBJECTS       = $(SOURCES:.cxx=.o)
DEPENDS       = $(SOURCES:.cxx=.d)

DICT	      = Dict

DATE	     := $(shell date "+%F")

######################################################################
# default targets

all:            $(PROGRAM)

clean:
		@rm -f $(OBJECTS) $(PROGRAM) $(DICT).* $(DEPENDS)

distclean:      clean
		@rm -f *~ core *.def *.exp *.root *.ps .def gmon.out

tarball:
		tar cvjf $(PROGRAM)-$(DATE).tar.bz2 Makefile *.h *.cxx

######################################################################
# rules

.SUFFIXES: .cxx .$(ExeSrcSuf) .C .f .o .so .d

.cxx.o:
	$(CXX) $(CXXFLAGS) -c $<

.cpp.o:
	$(CXX) $(CXXFLAGS) -c $<

.cc.o:
	$(CXX) $(CXXFLAGS) -c $<

.C.o:
	$(CXX) $(CXXFLAGS) -c $<

.f.o:
	$(FC) $(FCFLAGS) -c $< -o $@

.cpp.d:
	$(SHELL) -ec '$(CXX) -M $(CXXFLAGS) $< > $@'

.cxx.d:
	$(SHELL) -ec '$(CXX) -M $(CXXFLAGS) $< > $@'

.cc.d:
	$(SHELL) -ec '$(CXX) -M $(CXXFLAGS) $< > $@'

include $(DEPENDS)

######################################################################
# ROOT dictionary

$(DICT).C: $(HEADERS) LinkDef.h
	@echo "Generating dictionary $(DICT)..."
	@echo rootcint -f $@ -c $(EXTINCDIR) $+
	@rootcint -f $@ -c $(EXTINCDIR) $+

######################################################################
# targets

$(PROGRAM):  $(OBJECTS) $(DICT).o
	$(LD) $(LDFLAGS) $+ -o $@
		@echo "$@ done"
