# bash completion for azuresshconfig
#
# In order to load this, do either
# put this file under /etc/bash_completion.d, /usr/local/etc/bash_completion.d, or ~/bash_completion.d
# or
# append 'source /path/to/azuresshconfig_completion.bash' to .bashrc

_azuresshconfig() {
    local cmd cur prev
    cmd=$1
    cur=$2
    prev=$3
    subcmds="-h --help --init --profile --user --identityfile --private --resourcegroups --params"
    # contextual completion
    case $prev in
        azuresshconfig)
            case $cur in
            --p*)
                COMPREPLY=( $(compgen -W "--profile --private --params") )
                ;;
            --i*)
                COMPREPLY=( $(compgen -W "--init --identityfile") )
                ;;
            --r*)
                COMPREPLY=( $(compgen -W "--resourcegroups") )
                ;;
            --u*)
                COMPREPLY=( $(compgen -W "--user") )
                ;;
            *)
                COMPREPLY=( $(compgen -W "$subcmds") )
                ;;
            esac
            return 0
            ;;
        --identityfile)
            COMPREPLY=("<ssh_identity_file>")
            return 0
            ;;
        --profile)
            COMPREPLY=("<azuresshconfig_profile>")
            return 0
            ;;
        --user)
            COMPREPLY=("<ssh_user>")
            return 0
            ;;
        --resourcegroups)
            COMPREPLY=("<azure_resource_groups>")
            return 0
            ;;
        --params)
            COMPREPLY=("<additional_ssh-config_params>")
            return 0
            ;;
    esac

    case $cur in
        --p*)
            COMPREPLY=( $(compgen -W "--profile --private --params") )
            ;;
        --i*)
            COMPREPLY=( $(compgen -W "--init --identityfile") )
            ;;
        --r*)
            COMPREPLY=( $(compgen -W "--resourcegroups") )
            ;;
        --u*)
            COMPREPLY=( $(compgen -W "--user") )
            ;;
        *)
            COMPREPLY=( $(compgen -W "$subcmds") )
            ;;
    esac
    return 0
}

complete -F _azuresshconfig azuresshconfig
