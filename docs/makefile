#
# Publication system
#

include makefile.docs

publish: $(BUILDDIR)/publish
$(BUILDDIR)/dirhtml:dirhtml
$(BUILDDIR)/publish:$(BUILDDIR)/dirhtml
	@mkdir -p $@
	@rsync -ra $</ $@/
	@touch $@
	@echo "[build]: migrated '$<' to '$@'"
