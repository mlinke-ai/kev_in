@echo off
pushd frontend
call npm run build
popd
python run.py --host --clean --testing
