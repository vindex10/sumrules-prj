PPATH:=".."
MKFILE_PATH:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
OUTPUT?=$(MKFILE_PATH)/output
MODELS:=tmPw tmCoul sqedPw sqedRepCoul sqedAttrCoul

.PHONY: all clean $(MODELS) $(addprefix clean_,$(MODELS)) $(addprefix debug_,$(MODELS))

.SECONDEXPANSION:

all: $(MODELS)

$(addprefix clean_,$(MODELS)):
	rm -rf $(OUTPUT)/$(subst clean_,,$@)

$(MODELS): clean_$$@
	PYTHONPATH=$(PPATH) TEST_outputPath=$(OUTPUT)/$(subst clean_,,$@) python $@/test.py $(ARGS)

$(addprefix batch_,$(MODELS)): $$(subst batch_,clean_,$@)
	PYTHONPATH=$(PPATH) python $(PPATH)/scripts/batcher.py run $(subst batch_,,$@) $(ARGS) -o $(OUTPUT) -s $(subst batch_,,$@)

$(addprefix reduce_,$(MODELS)): $$(subst reduce_,clean_,$@)
	PYTHONPATH=$(PPATH) python $(PPATH)/scripts/batcher.py reduce $(OUTPUT)/$(subst reduce_,,$@)/output -o $(OUTPUT)/$(subst reduce_,,$@)/output/reduced
	
$(addprefix nice_,$(MODELS)): $$(subst nice_,clean_,$@)
	PYTHONPATH=$(PPATH) TEST_outputPath=$(OUTPUT)/$(subst nice_,,$@) nice python $(subst nice_,,$@)/test.py $(ARGS)

$(addprefix debug_,$(MODELS)): $$(subst debug_,clean_,$@)
	PYTHONPATH=$(PPATH) TEST_outputPath=$(OUTPUT)/$(subst debug_,,$@) nice python -m ipdb $(subst debug_,,$@)/test.py $(ARGS)

clean:
	rm -rf $(OUTPUT)
