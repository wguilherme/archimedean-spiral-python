PYTHON     = python
PYTHONPATH = src

.PHONY: test plot help

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s %s\n", $$1, $$2}'

test: ## Run unit tests
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests -v

plot: ## Render spiral with matplotlib
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/plot.py
