
from DnsCryptPiHoleSetup.DefaultConfig import host,  password, user,dnscryptdownloadlink,\
dnscryptexractdir,dnscryptresolvercsvlink, dnscryptresolverdir,\
    dnscryptresolvernames, loopbackstartaddress, cronjobmessage, \
    cronjobminutes

import click
from click_help_colors import HelpColorsCommand
from DnsCryptPiHoleSetup.FabricService.FabricExecute import FabricExecuteClass
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













@click.command(context_settings=dict(max_content_width=500),
               cls=HelpColorsCommand,help_options_color='blue',help_headers_color='yellow')
@click.option('--host','-h', default=host, help='Host or IP address that the Dnscrypt proxy script will ran against',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--user', '-u',default=user, help='Username for host that the Dnscrypt proxy script will ran against',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--password','-p', default=password, help='Password for host that the Dnscrypt proxy script will ran against',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--dnscryptexractdir', '-e', default=dnscryptexractdir, help='Directory for where the DnsCrypt Proxy is going to be downloaded and extracted at during Install',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--dnscryptdownloadlink', '-d', default=dnscryptdownloadlink, help='HTTP address of DNScrypt.tar.gz',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--dnscryptresolvercsvlink','-c', default=dnscryptresolvercsvlink, help='HTTP address of the Csv for  DnsCrypt Resolvers',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--dnscryptresolverdir', '-r',default=dnscryptresolverdir, help='Directory location of where the Csv resolver files are stored',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--dnscryptresolvernames','-n', default=dnscryptresolvernames, help='Name of resolvers to be installed',show_default=True,type=list,cls=ListArgs)
@click.option('--loopbackstartaddress', '-l', default=loopbackstartaddress, help='IPV4 Loopback Address you want to use for the socket unit file. The address will increment by the last octet when multiple proxies are installed',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--cronjobminutes','-t', default=cronjobminutes, help=' How often in minutes do you want the Cron Job use for check if there is errors and restarting the individual dnscrypt proxy ex. 10 = */10 * * * *',show_default=True,cls=ShowDefaultSingleQuote)
@click.option('--cronjobmessage','-m', default=cronjobmessage, help='The Message you want to match on the DnsCrypt Proxy System Log to Trigger a Restart Event',show_default=True,cls=ShowDefaultSingleQuote)
def cli(host, password, user,dnscryptexractdir,dnscryptdownloadlink,
        dnscryptresolvercsvlink,dnscryptresolverdir,dnscryptresolvernames,
        loopbackstartaddress,cronjobminutes,cronjobmessage
        ):
    Fec = FabricExecuteClass(user, password, host)
    Fec.ExecuteSystemPackages()
    Fec.ExecuteBuildDNSCrypt(dnscryptexractdir,dnscryptdownloadlink)
    Fec.ExecuteAddDnsCryptUser()
    Fec.ExecuteDownloadDnsCryptResolvers(dnscryptresolvercsvlink,dnscryptresolverdir)
    Fec.ExecuteCreateDNSCryptProxies(dnscryptresolverdir,dnscryptresolvernames,dnscryptresolvercsvlink,
                                     loopbackstartaddress, dnscryptexractdir)
    Fec.ExecuteChangeDnsMasq(dnscryptresolvernames)
    Fec.ExecuteCreateCronJob(cronjobminutes,cronjobmessage)



