test:
	PYTHONPATH=. python3 -m pytest ./tests/test_diversity.py

release:
	bumpversion build --tag --verbose
	git push --tags
	git push

nexus: test release
	rm -rf build dist
	docker run -v $$(pwd):/code -e CI_PROJECT_DIR=/code -it gitlab.beno.ai:4567/ai/hypgen/baidocs/pydocs:0.0.16 /opt/bin/push_to_nexus