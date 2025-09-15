build:
	uv build .

clean:
	rm -r dist mrql.egg-info

publish: build
	uv publish
	make clean

fmt:
	ruff format .

lint:
	ruff check .
	ty check .

fix:
	ruff check --fix .
