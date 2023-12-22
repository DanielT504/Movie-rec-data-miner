.PHONY: run install clean

VENV_DIR := venv

run: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/python recommender.py

install: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/pip install -r requirements.txt

$(VENV_DIR)/bin/activate: requirements.txt
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install --upgrade pip
	touch $(VENV_DIR)/bin/activate

clean:
	rm -rf $(VENV_DIR)

# Add more targets/rules as needed

