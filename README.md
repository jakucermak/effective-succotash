Run instructions:
  1. create virtual environment `python3 -m venv venv`
  2. activate virtual environment `source venv/bin/activate/`
  3. install dependencies with pip `pip install -r requirements.txt`
  4. run program as follows `python3 main.py -a {{Specify_Arcitecture}} -f {{relative_path_to_older_rpms.json}} {{relative_path_to_newer_rpms.json}}` or with build selection `python3 main.py -a {{Specify_Arcitecture}}`
  5. available architectures are:
     - X86_64
     - AARCH64
     - PPC64LE
     - S390X
