# run checks on all files for the repo
quality:
	@echo "Running helm lint on charts...";
	bin/lint-charts
	@echo ""
	@echo "Validating charts/nm-vllm yaml produced from default values..."
	helm template charts/nm-vllm | yamllint -

# style the code according to accepted standards for the repo
style:
	pre-commit run --all-files -c .pre-commit-config.yaml

.PHONY: docs
docs: ## Build helm chart documentation
	@docker pull jnorwood/helm-docs:latest
	@docker run --rm --volume "$$(pwd):/helm-docs" -u $$(id -u) jnorwood/helm-docs:latest --document-dependency-values
