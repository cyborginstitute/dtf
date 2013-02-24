MAKEFLAGS += --no-print-directory

all:
	@$(MAKE) -C docs/ html
	@echo [test]: --- Starting test \'dtf\' run ---
	@python2 dtf/dtf.py
