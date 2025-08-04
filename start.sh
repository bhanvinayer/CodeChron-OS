#!/bin/bash
reflex run --env prod --backend-port ${PORT:-3000} --backend-host 0.0.0.0
