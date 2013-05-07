MAKEFLAGS += --no-print-directory

.PHONY:docs
all:tags docs test

tags:
	@find . -name "*.py" | grep -v "\.\#" | etags --output TAGS -
	@echo [dev]: regenerated tags

modsrc = buildergen
.PHONY:embedded testpy test
test:testpy
	@echo -----
	@echo "[dtf]: running dtf serial -- `python --version`"
	@dtf
	@echo -----
	@echo "[dtf]: running dtf event -- `python --version`"
	@dtf --multi event
	@echo -----
	@echo "[dtf]: running dtf thread -- `python --version`"
	@dtf --multi thread
	@echo -----
	@echo "[dtf]: running dtf process -- `python --version`"
	@dtf --multi process
testpy:
	@echo "[unittest]: running unittests -- `python --version`"
	@python test.py

docs:
	@$(MAKE) -C docs/ html
stage-docs:
	@$(MAKE) -C ../institute/ stage push

release:all gitpush
	python setup.py sdist upload
	@$(MAKE) -C ../institute/ stage push

gitpush:
	git push cyborg master
	git push github master
