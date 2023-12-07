# This file is used to generate a code
# using packages from this monorepo and split repositories in the
# googleapis organization on Github.

SCRIPT_ROOT=$(realpath $(dirname "${BASH_SOURCE[0]}"))

output="import proto\n"
output+="from google.auth import credentials\n"
output+="creds = credentials.AnonymousCredentials()\n"
# Get test code for all packages this monorepo
for package in $SCRIPT_ROOT/../../packages/*/ ; do
    package_dir=$(basename $package)
    top_namespace="${package_dir%%-*}"
    for d in `find $package$top_namespace -name '__init__.py'`; do
        init_relative_path=${d#$package}
        module_path=$(echo $init_relative_path | sed -e "s/\/__init__.py//")
        import_path="$(echo $module_path | sed -E 's/\//./g')"
        modules=($(awk -v RS='"' '!(NR%2)' $d))
        for module_name in "${modules[@]}"; do 
            if [[ ${#module_name} -ge 8 ]] && [[ $module_name = *Client* ]] && [[ ! $module_name = *:class:* ]]; then
                # For google.cloud.alloydb*, see https://github.com/googleapis/google-cloud-python/issues/12094
                # For google.cloud.billing*, see https://github.com/googleapis/google-cloud-python/issues/12095
                # For google.cloud.dialogflowcx_v3*.services.generators*, see https://github.com/googleapis/google-cloud-python/pull/12065
                # For google.monitoring**, see https://github.com/googleapis/google-cloud-python/issues/11858
                # For google.cloud.securitycentermanagement*, see https://github.com/googleapis/google-cloud-python/pull/12091
                # See https://github.com/googleapis/python-vision/blob/4ed30260420a240700d10b32b4cb611d01ed31c7/google/cloud/vision_helpers/__init__.py#L33
                if [[ ! $import_path = @(google.cloud.alloydb*|google.cloud.billing*|google.cloud.dialogflowcx_v3*.services.generators*|google.monitoring*|google.cloud.securitycentermanagement*|google.cloud.vision_helper*) ]]; then
                    output+="from $import_path import $module_name\n"
                    # Grafeas client does not support credentials argument, use transport instead
                    # See https://github.com/googleapis/google-cloud-python/pull/8186
                    if [[ $import_path = @(grafeas*) ]]; then
                        output+="from grafeas.grafeas_v1.services.grafeas.transports.base import GrafeasTransport\n"
                        output+="transport=GrafeasTransport(credentials=creds)\n"
                        arguments="transport=transport"
                    else
                        arguments="credentials=creds"
                    fi
                    output+="not issubclass($module_name, proto.Enum) and not issubclass($module_name, proto.Message) and $module_name($arguments)\n"
                    output+="import $import_path\n"
                    output+="not issubclass($module_name, proto.Enum) and not issubclass($module_name, proto.Message) and $import_path.$module_name($arguments)\n"
                    break
                fi
            fi
        done
    done
done

echo -e $output > test_modules.py