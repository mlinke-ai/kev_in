#! /bin/bash
# -*- coding: utf-8 -*-

pushd frontend
npm install
popd
code .
pushd frontend
npm run dev -- --open

