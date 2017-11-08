PPATH:=".."
MKFILE_PATH:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
OUTPUT?=$(MKFILE_PATH)/output
MODELS:=tmPw tmCoul sqedPw sqedRepCoul sqedAttrCoul prec

.PHONY: all fast_all clean $(MODELS) $(addprefix clean_,$(MODELS)) $(addprefix debug_,$(MODELS))  $(addprefix fast_,$(MODELS)) $(addprefix batch_,$(MODELS)) $(addprefix reduce_,$(MODELS))

.SECONDEXPANSION:

all: $(MODELS)
fast_all: $(addprefix fast_,$(MODELS))

$(addprefix clean_,$(MODELS)):
	rm -rf $(OUTPUT)/$(subst clean_,,$@)

$(MODELS):
	PYTHONPATH=$(PPATH) TEST_outputPath=$(OUTPUT)/$(subst clean_,,$@) python $@/test.py $(ARGS)

$(addprefix fast_,$(MODELS)):
	PYTHONPATH=$(PPATH) TEST_outputPath=$(OUTPUT)/$(subst fast_,,$@) python $(subst fast_,,$@)/test.py -c configs/fast.conf $(ARGS)

$(addprefix batch_,$(MODELS)):
	PYTHONPATH=$(PPATH) python $(PPATH)/scripts/batcher.py run $(subst batch_,,$@) $(ARGS) -o $(OUTPUT)/$(subst batch_,,$@) -p $(PPATH)

$(addprefix reduce_,$(MODELS)):
	PYTHONPATH=$(PPATH) python $(PPATH)/scripts/batcher.py reduce $(OUTPUT)/$(subst reduce_,,$@)/output -o $(OUTPUT)/$(subst reduce_,,$@)/reduced
	
$(addprefix debug_,$(MODELS)):
	PYTHONPATH=$(PPATH) TEST_outputPath=$(OUTPUT)/$(subst debug_,,$@) nice python -m ipdb $(subst debug_,,$@)/test.py $(ARGS)

clean:
	rm -rf $(OUTPUT)
