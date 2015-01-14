# Source this file to get xadmin shell support
# Allows you to easily create named shortcuts to endpoints
# and acces them with shell completion for all endpoints defined
# in endpoints.txt

export X_ADMIN=~/mybash/xadmin/xadmin.py

function xlist() {
    $X_ADMIN --list
}

function xnames() {
    $X_ADMIN --listnames
}

function xadmin() {
    $X_ADMIN --admin $1
}

function xroot() {
    $X_ADMIN --root $1
}

function xanswer() {
    $X_ADMIN --answer $1
}

function xdial() {
    $X_ADMIN --dial $1 $2
}

function xdisconnect() {
    $X_ADMIN --disconnect $1
}

function xweb() {
    $X_ADMIN --web $1
}

function xsearch() {
    $X_ADMIN --search $1 $2
}

_xadminendpoints()
{
    local cur=${COMP_WORDS[COMP_CWORD]}
    COMPREPLY=( $(compgen -W "$(xnames)" -- $cur) )
}

complete -F _xadminendpoints xadmin
complete -F _xadminendpoints xroot
complete -F _xadminendpoints xanswer
complete -F _xadminendpoints xdial
complete -F _xadminendpoints xweb
complete -F _xadminendpoints xsearch

