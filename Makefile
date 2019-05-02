SUBDIRS=doug_inverted_index

server_django:
	python manage.py runserver

server_inverted_index:
	$(MAKE) -C doug_inverted_index all
	
run: 
	for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir hidden; \
	done
	
	python manage.py runserver