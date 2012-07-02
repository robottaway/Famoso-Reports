Hi there ${user.displayName()},

There are new reports for you to view, please sign in at ${request.route_url('home')} to view them.

% if new_reports:
% for report in new_reports:
${report.name} - ${request.route_url('report', name=report.report_group.name, reportname=report.name)}
% endfor
% endif

Thank you,
The Famoso Team
