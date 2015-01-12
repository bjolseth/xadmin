# Source this file to get xadmin shell support
# Allows you to easily create named shortcuts to endpoints
# and acces them with shell completion for all endpoints defined
# in endpoints.txt

function xlist() {
    ./xadmin.py --list
}

function xadmin() {
    ./xadmin.py --admin $1
}

function xroot() {
    ./xadmin.py --root $1
}

function xanswer() {
    ./xadmin.py --answer $1
}

function xdial() {
    ./xadmin.py --dial $1 $2
}

function xdisconnect() {
    ./xadmin.py --disconnect $1
}

function xweb() {
    ./xadmin.py --web $1
}

_xadminendpoints()
{
    local cur=${COMP_WORDS[COMP_CWORD]}
    COMPREPLY=( $(compgen -W "$(xlist)" -- $cur) )
}

complete -F _xadminendpoints xadmin
complete -F _xadminendpoints xroot
complete -F _xadminendpoints xanswer
complete -F _xadminendpoints xdial
complete -F _xadminendpoints xweb


