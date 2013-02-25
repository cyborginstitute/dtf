MAKEFLAGS += --no-print-directory

.PHONY:docs
all:tags docs test

tags:
	@find . -name "*.py" | etags --output TAGS -
	@echo [dev]: regenerated tags

docs:
	@$(MAKE) -C docs/ html

test:
	@python2 dtf/dtf.py

release:all gitpush
	python setup.py sdist upload
	@$(MAKE) -C ../institute/ stage push

gitpush:
	git push cyborg master
	git push github master
