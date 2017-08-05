PPATH:=".."
MKFILE_PATH:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
OUTPUT?=$(MKFILE_PATH)/output
MODELS:=tmPw tmCoul sqedPw sqedCoul

.PHONY: all clean $(MODELS) $(addprefix clean_,$(MODELS)) $(addprefix debug_,$(MODELS))

.SECONDEXPANSION:

all: $(MODELS)

$(addprefix clean_,$(MODELS)):
	rm -rf $(OUTPUT)/$(subst clean_,,$@)

$(MODELS): clean_$$@
	PYTHONPATH=$(PPATH) OUTPUT=$(OUTPUT)/$@ nice python $@/test.py
	
$(addprefix debug_,$(MODELS)): $$(subst debug_,clean_,$@)
	PYTHONPATH=$(PPATH) OUTPUT=$(OUTPUT)/$(subst debug_,,$@) nice python -m ipdb $(subst debug_,,$@)/test.py

clean:
	rm -rf $(OUTPUT)
