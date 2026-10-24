.PHONY: report clean demo demo-test

report:
	mkdir -p build
	latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build report/main.tex
	cp -f build/main.pdf report/main.pdf 2>/dev/null || true
	cp -f build/main.pdf main.pdf 2>/dev/null || true

clean:
	latexmk -C -outdir=build report/main.tex
	rm -rf build

demo:
	bash demo/scripts/setup_lab.sh

demo-test: demo
	bash demo/scripts/run_tests.sh
