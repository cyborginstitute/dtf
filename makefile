MAKEFLAGS += --no-print-directory

all:
	@$(MAKE) -C docs/ html
	@python2 dtf/dtf.py
