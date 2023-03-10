pushd frontend
npm install
npm run build
popd
./run.py --host --testing --clean
