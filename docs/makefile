MAKEFILEARGS += -j 

#
# Publication system
#

DEFAULT_GOAL:all


clean: 
	-rm -rf build/*

setup: 
	@true

include makefile.docs
include bin/makefile.compatibility 

all:intersphinx publish

dirhtml:intersphinx
publish: $(BUILDDIR)/publish
$(BUILDDIR)/dirhtml:dirhtml
$(BUILDDIR)/publish:$(BUILDDIR)/dirhtml
	@mkdir -p $@
	@rsync -ra $</ $@/
	@touch $@
	@echo "[build]: migrated '$<' to '$@'"

-include $(BUILDDIR)/makefile.intersphinx
$(BUILDDIR)/makefile.intersphinx:bin/intersphinx.py bin/makefile_builder.py $(BUILDDIR) conf.py
	@$(PYTHONBIN) $< $@
