syntax clear

" This rule gets overwritten by remote plugin, where appropriate
syn region yamlComment start="\#" end="$"

hi link yamlComment Comment
