all: build

.PHONY: build 
build:
	python3 setup.py sdist bdist_wheel

.PHONY: test
test:
	@python3 ./test/crypto_test.py
	@python3 ./test/colonies_test.py

.PHONY: github_test
github_test:
	wget https://github.com/colonyos/colonies/releases/download/v1.7.1/colonies_1.7.1_linux_amd64.tar.gz
	tar -xzf colonies_1.7.1_linux_amd64.tar.gz
	env
	./colonies database create
	./colonies colony add --spec ./colony.json --colonyprvkey ${COLONIES_COLONY_PRVKEY}
	./colonies executor add --spec ./cli_executor.json --executorprvkey ${COLONIES_EXECUTOR_PRVKEY}
	./colonies executor approve --executorid ${COLONIES_EXECUTOR_ID}
	@pip3 install -r requirements.txt
	@python3 ./test/crypto_test.py
	@python3 ./test/colonies_test.py

.PHONY: install
install:
	pip3 install dist/pycolonies-1.0.11-py3-none-any.whl --force-reinstall 

publish:
	python3 -m twine upload dist/pycolonies-1.0.11-py3-none-any.whl 
