MAKEFLAGS += --no-print-directory

.PHONY:docs
all:tags docs test

tags:
	@find . -name "*.py" | grep -v "\.\#" | etags --output TAGS -
	@echo [dev]: regenerated tags

modsrc = buildergen
.PHONY:embedded testpy2 testpy3 testpypy
test:test2
test2:testpy2
	@echo -----
	@echo "[dtf]: running dtf serial - python 2"
	@python2 dtf/dtf.py
	@echo -----
	@echo "[dtf]: running dtf event - python 2"
	@python2 dtf/dtf.py --multi event
	@echo -----
	@echo "[dtf]: running dtf thread - python 2"
	@python2 dtf/dtf.py --multi thread
	@echo -----
	@echo "[dtf]: running dtf process - python 2"
	@python2 dtf/dtf.py --multi process

test3:testpy3
	@echo -----
	@echo "[dtf]: running dtf serial - python 3"
	@python3 dtf/dtf.py
	@echo -----
	@echo "[dtf]: running dtf event - python 3"
	@python3 dtf/dtf.py --multi event
	@echo -----
	@echo "[dtf]: running dtf thread - python 3"
	@python3 dtf/dtf.py --multi thread
	@echo -----
	@echo "[dtf]: running dtf process - python 3"
	@python3 dtf/dtf.py --multi process

testpy2:$(wildcard $(modsrc)*.py)
	@/usr/bin/python2 test.py
	@echo [test]: Python 2 tests complete.
testpy3:$(wildcard $(modsrc)*.py)
	@/usr/bin/python3 test.py
	@echo [test]: Python 3 tests complete.
testpypy:$(wildcard $(modsrc)*.py)
	@. /usr/bin/virtualenvwrapper.sh; workon pypy; pypy test.py
	@echo [test]: PyPy tests complete.

docs:
	@$(MAKE) -C docs/ html

release:all gitpush
	python setup.py sdist upload
	@$(MAKE) -C ../institute/ stage push

gitpush:
	git push cyborg master
	git push github master
