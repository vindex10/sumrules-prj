PPATH:=".."
MKFILE_PATH:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
OUTPUT:=$(MKFILE_PATH)/output

.PHONY: all tmPw 

all: tmPw
tmPw:
	PYTHONPATH=$(PPATH) OUTPUT=$(OUTPUT)/tmPw python tmPw/test.py
clean:
	rm -rf $(OUTPUT)
