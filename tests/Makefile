PPATH:=".."
MKFILE_PATH:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
OUTPUT:=$(MKFILE_PATH)/output
MODELS:=tmPw tmCoul

.PHONY: all clean $(MODELS)

all: $(MODELS)

$(MODELS):
	PYTHONPATH=$(PPATH) OUTPUT=$(OUTPUT)/$@ python $@/test.py
	
$(addprefix debug_,$(MODELS)):
	PYTHONPATH=$(PPATH) OUTPUT=$(OUTPUT)/$(subst debug_,,$@) python -m ipdb $(subst debug_,,$@)/test.py

clean:
	rm -rf $(OUTPUT)
