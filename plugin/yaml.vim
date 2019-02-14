" Vim YAML plugin for YAML syntax highlighting
" Author: Jakub Pieńkowski <jakub@jakski.name>
" Home: https://github.com/Jakski/vim-yaml
" License: MIT

if exists("g:loaded_yaml") || !has('signs')
	finish
endif

let s:save_cpo = &cpo
set cpo&vim

if !exists("g:yaml#patterns")
	let g:yaml#patterns = '*.yml,*.yaml'
endif

augroup Yaml
	execute 'autocmd BufEnter ' . g:yaml#patterns . ' call <SID>Init()'
	execute 'autocmd BufEnter ' . g:yaml#patterns . ' call <SID>Highlight()'
	execute 'autocmd CursorMoved ' . g:yaml#patterns . ' call <SID>Highlight()'
	execute 'autocmd CursorMovedI ' . g:yaml#patterns . ' call <SID>Highlight()'
	execute 'autocmd TextChanged ' . g:yaml#patterns . ' call <SID>Highlight()'
	execute 'autocmd TextChangedI ' . g:yaml#patterns . ' call <SID>Highlight()'
augroup END

sign define yamlError text=E> texthl=ErrorMsg

command YamlError call <SID>GetError()

function s:Init() abort
	call _yaml_init()
endfunction

function s:GetError() abort
	echo rpcrequest(g:yaml#_channel_id, 'yaml_get_error')
endfunction

function s:Highlight() abort
	call rpcnotify(g:yaml#_channel_id, 'yaml_highlight', line('w0'), line('w$'))
endfunction

let g:loaded_yaml = 1
let &cpo = s:save_cpo
unlet s:save_cpo
