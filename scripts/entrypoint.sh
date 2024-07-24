#!/bin/bash

# If any command fails, exit immediately with that command's exit status
set -eo pipefail

# -------------------------------------------------------------------------------------

# Function to replace argument value with environment variable if set
unset_env_var_if_arg() {
    local arg_name="$1"
    local env_var_name="$2"
    local env_var_value="${!env_var_name}"

    shift 2

    # Check if the environment variable is set
    if [[ -z "${env_var_value}" ]]; then
        echo "${env_var_name} is not set"
        return
    fi

    # Loop through the rest of the arguments to find the matching arg_name and non-null value
    while [[ $# -gt 0 ]]; do
        if [[ "$1" == "${arg_name}" ]]; then
            if [[ -n "$2" && "$2" != "-"* ]]; then
                unset "${env_var_name}"
                break
            fi
        fi
        shift
    done
}

# -------------------------------------------------------------------------------------

# Unset environment variables if the equivalent argument is passed
# unset_env_var_if_arg "--csrf-token" "CSRF_TOKEN" "$@"

# -------------------------------------------------------------------------------------

poetry run python main.py "$@"
