.PHONY: report clean demo demo-test

report:
	mkdir -p build
	latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build report/main.tex

clean:
	latexmk -C -outdir=build report/main.tex
	rm -rf build

demo:
	bash demo/scripts/setup_lab.sh

demo-test: demo
	bash demo/scripts/run_tests.sh
