#!/bin/bash

set -e

source $PWD/test/kwok/config.sh

apply_kwok_deployment "fake-pod" 100 "default"

apply_kwok_deployment "fake-pod-spot" 100 "spot"
