from functools import wraps

import pynvim

from ruamel.yaml.scanner import ScannerError

from .highlight import Highlighter


def feature_enabled(feature, compare_func):
    def wrap(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            if self.check_feature(feature, compare_func):
                return f(self, *args, **kwargs)
            return
        return wrapper
    return wrap


@pynvim.plugin
class Plugin:

    SIGN_ID = 2958134

    def __init__(self, nvim):
        self._nvim = nvim
        self._highlighter = Highlighter()
        self._error = None
        self._src_id = None
        self._input_mode = False
        self._buffer = None

    @pynvim.function('_yaml_init', sync=True)
    def init_with_nvim(self, args):
        if self._src_id is None:
            self._src_id = self._nvim.new_highlight_source()
        self._nvim.vars['yaml#_channel_id'] = self._nvim.channel_id

    @pynvim.rpc_export('yaml_get_error', sync=True)
    def write_error(self):
        if self._error is not None:
            return self._error
        else:
            return 'No error\'s been discovered so far.'

    @pynvim.rpc_export('yaml_highlight', sync=False)
    def highlight(self, start, end, imode, full):
        self._input_mode = bool(imode)
        self._buffer = self._nvim.current.buffer
        full = bool(full)
        if full:
            self._highlighter.start = 1
            self._highlighter.end = len(self._buffer)
        else:
            self._highlighter.start = start - 1
            self._highlighter.end = end - 1
        highlights = []
        try:
            lines = [line for line in self._buffer]
            for highlight in self._highlighter.highlight(
                    '\n'.join(lines)):
                highlights.append(highlight)
        except ScannerError as e:
            self.sign_error(e)
        else:
            self.clear_errors()
        if len(highlights) > 0:
            hl_start = highlights[0][1]
            hl_end = highlights[-1][1]
        else:
            hl_start = start
            hl_end = end
        self._buffer.update_highlights(
            self._src_id,
            highlights,
            clear_start=hl_start,
            clear_end=hl_end,
            async_=True)

    def check_feature(self, feature, func):
        return func(self._nvim.vars['yaml#' + feature])

    @feature_enabled('error_signs', lambda x: x == 1)
    def sign_error(self, error):
        if self._input_mode:
            return
        self._error = str(error)
        self._nvim.command('sign place %s line=%s name=%s file=%s' % (
            self.SIGN_ID,
            error.problem_mark.line,
            'yamlError',
            self._buffer.name))

    @feature_enabled('error_signs', lambda x: x == 1)
    def clear_errors(self):
        self._error = None
        self._nvim.command('sign unplace %s' % (self.SIGN_ID))
