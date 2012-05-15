Hi there ${user.displayName()},

% if user_new_reports:
% for report in user_new_reports:
report.name - ${request.route_path('report', name=report.report_group.name, reportname=report.name)}
% endfor
% endif

Thank you,
The Famoso Team
