cd bin
source activate
cd ..
pipenv run python fetch_csv.py
pipenv run python process_data.py
echo "pipenv run python process_data.py"