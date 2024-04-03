# run checks on all files for the repo
quality:
	@echo "Running helm lint on charts...";
	bin/lint-charts
	@echo ""
	@echo "Validating charts/nm-vllm yaml produced from default values..."
	helm template charts/nm-vllm | yamllint -
