Hello ${user.displayName()},
% if gone_groups and new_groups:
${self.show_new_groups()} \
${self.show_gone_groups()}
% elif new_groups:
${self.show_new_groups()}
% elif gone_groups:
${self.show_gone_groups()}
% endif
To view your reports sign in here: ${request.route_url('signin')}

Thank You,
The Famoso Team

<%def name="show_new_groups()">
% if len(new_groups) > 1:
You have been added to these report groups:
% elif len(new_groups) == 1:
You have been added to a report group:
% endif

% for group in new_groups:
${group.displayname}
% endfor
</%def>

<%def name="show_gone_groups()">
% if len(gone_groups) > 1:
You have been removed from these report groups:
% elif len(gone_groups) == 1:
You have been removed from a report group:
% endif

% for group in gone_groups:
${group.displayname}
% endfor
</%def>
