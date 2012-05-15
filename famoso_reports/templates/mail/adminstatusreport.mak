Hello admin user ${user.displayName()},

This is an admin status report for the Famoso reporting application.

% if new_reports:
Here are new reports:
% for report in new_reports:
${request.route_url('report', name=report.report_group.name, reportname=report.name)} - ${report.name}
% endfor
% endif 

% if new_groups:
Here are new report groups, you will need to add users to these:
% for group in new_groups:
${request.route_url('reportgroup', name=group.name)} - ${group.name}
% endfor 
% endif 

% if csv_files_missing_pdf:
There are csv files witch no corressponding pdf file:
% for file in csv_files_missing_pdf:
${file}
% endfor
% endif \

Thank you,
The Famoso Team
