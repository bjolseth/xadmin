# Source this file to get xadmin shell support
# Allows you to easily create named shortcuts to endpoints
# and acces them with shell completion

function xadmin() {
    ./xadmin.py $1
}

function xroot() {
    ./xadmin.py --root $1
}

_xadminendpoints()
{
    local cur=${COMP_WORDS[COMP_CWORD]}
    COMPREPLY=( $(compgen -W "$(xadmin)" -- $cur) )
}

complete -F _xadminendpoints xadmin
complete -F _xadminendpoints xroot
