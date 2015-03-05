%rebase('_dashboard_section')

%# Translators, used as section heading on dashboard above disk space and similar information
<p class="total">
%# Translators, %s is the amount of free space in bytes, KB, MB, etc.
% include('diskspace/_space_info', label=_('total space (%s free)'), space=(free, total))
</p>

% if needed:
<p class="warning">
%# Translators, this is a warning message appearing when disk space is below 10%
{{ _('You are running low on disk space.') }}
%# Translators, this is a button label that leads to page for library cleanup
<a href="{{ i18n_path(url('plugins:diskspace:cleanup')) }}">{{ _('Free some space now') }}</a>
</p>
% end

<div class="content-archive">
    <div class="stat count">
    <span class="number">{{ count }}</span>
    %# Translators, used as a label in content library stats section on dashboard, preceded by count of items in the library
    <span class="label">{{ ngettext('item in the library', 'items in the library', count) }}</span>
    </div>

    <div class="stat space">
    <span class="number">{{ h.hsize(used) }}</span>
    %# Translators, used as a label in content library stats section on dashboard, preceded by library size in bytes, KB, MB, etc
    <span class="label">{{ _('used space') }}</span>
    </div>
</div>
