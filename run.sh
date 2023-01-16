pushd frontend
npm run build
popd
./run.py --host --testing --clean
