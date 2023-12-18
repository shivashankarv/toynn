# Script that sets up the project

PROJECTNAME=$1

cd ../

sed -i 's/pytemplate/${PROJECTNAME}/g' environment.yml
sed -i 's/pytemplate/${PROJECTNAME}/g' pyproject.toml
mv pytemplate $PROJECTNAME

conda env create -f environment.yml
eval "$(conda shell.bash hook)"
conda activate $PROJECTNAME
pip install -e .

git init
git commit -am "Setting up the project"
git push
