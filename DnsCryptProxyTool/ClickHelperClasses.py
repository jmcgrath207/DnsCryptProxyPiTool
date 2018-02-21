

import click
from click.formatting import join_options


import ast

class ListArgs(click.Option):


    def type_cast_value(self, ctx, value):

        """
        Used to Convert String to a List
        example "['d0wn-random-ns1','d0wn-random-ns2']"
        """
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)


    def get_help_record(self, ctx):
        """
        Used to Correct --help to appear like this [default: "['d0wn-random-ns1','d0wn-random-ns2']" ]
        to accurately reflect the commands
        :param ctx:
        :return:
        """


        #if self.hidden:
        #    return
        any_prefix_is_slash = []

        def _write_opts(opts):
            rv, any_slashes = join_options(opts)
            if any_slashes:
                any_prefix_is_slash[:] = [True]
            if not self.is_flag and not self.count:
                rv += ' ' + self.make_metavar()
            return rv

        rv = [_write_opts(self.opts)]
        if self.secondary_opts:
            rv.append(_write_opts(self.secondary_opts))

        help = self.help or ''
        extra = []
        if self.default is not None and self.show_default:
            extra.append('default: \"%s' % (
                         ', '.join('%s' % d for d in self.default)
                         if isinstance(self.default, (list, tuple))
                         else self.default, ))
        if self.required:
            extra.append('required')
        if extra:
            help = '%s[%s\" ]' % (help and help + '  ' or '', '; '.join(extra))


        return ((any_prefix_is_slash and '; ' or ' / ').join(rv), help)








class ShowDefaultSingleQuote(click.Option):


    def get_help_record(self, ctx):
        """
        Used to Correct --help to appear like this  [default: '*/1 * * * *' ]
        to accurately reflect the commands
        :param ctx:
        :return:
        """


        #if self.hidden:
        #    return
        any_prefix_is_slash = []

        def _write_opts(opts):
            rv, any_slashes = join_options(opts)
            if any_slashes:
                any_prefix_is_slash[:] = [True]
            if not self.is_flag and not self.count:
                rv += ' ' + self.make_metavar()
            return rv

        rv = [_write_opts(self.opts)]
        if self.secondary_opts:
            rv.append(_write_opts(self.secondary_opts))

        help = self.help or ''
        extra = []
        if self.default is not None and self.show_default:
            extra.append('default: \'%s' % (
                         ', '.join('%s' % d for d in self.default)
                         if isinstance(self.default, (list, tuple))
                         else self.default, ))
        if self.required:
            extra.append('required')
        if extra:
            help = '%s[%s\' ]' % (help and help + '  ' or '', '; '.join(extra))


        return ((any_prefix_is_slash and '; ' or ' / ').join(rv), help)






