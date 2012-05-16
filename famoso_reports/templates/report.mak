${self.flash()}

<div>
	<a href="${request.route_path('reportgroup', name=reportgroup.name)}">Back to reports for <strong>${reportgroup.displayname}</strong></a>
</div>

<form class="readonly">
<fieldset>
<legend>${report.name}</legend>
<ul>
	<li><label>USDAID</label><div>${report.usdaid}</div></li>
	<li><label>Grower</label><div>${report.grower}</div></li>
	<li><label>Block</label><div>${report.block}</div></li>
	<li><label>Variety</label><div>${report.variety}</div></li>
	<li><label>County</label><div>${report.county}</div></li>
	<li><label>Lot</label><div>${report.lot}</div></li>
	<li><label>Commodity</label><div>${report.commodity}</div></li>
	<li><label>Handler</label><div>${report.handler}</div></li>
	<li><label>Certificate</label><div>${report.certificate}</div></li>
	<li><label>Date Certified</label><div>${report.date_certified}</div></li>
	<li><label>Gross Weight</label><div>${report.gross_weight}</div></li>
	<li><label>Edible Kernal Wt</label><div>${report.edible_kernal_weight}</div></li>
	<li><label>Inedible Kernal Wt</label><div>${report.inedible_kernal_weight}</div></li>
	<li><label>Foreign Material Wt</label><div>${report.foreign_material_weight}</div></li>
	<li><label>Shell Out Loss</label><div>${report.shell_out_loss}</div></li>
	<li><label>Excess Moisture</label><div>${report.excess_moisture}</div></li>
	<li><label>Crop Year</label><div>${report.crop_year}</div></li>
	<li><label>Acres</label><div>${report.acres}</div></li>
</ul>
</fieldset>
</form>

% if request.user.admin and reportgroup.users:
<form action="${request.route_path('email_report', name=reportgroup.name, reportname=report.name)}" method="POST">
<fieldset>
<legend>Email report to users</legend>
<ul>
% for user in reportgroup.users:
<li><label>${user.displayName()}</label><input type="checkbox" name="mailto" value="${user.username}" />
% endfor
<li><button>Send Report</button></li>
</ul>
</fieldset>
</form>
% endif

<%inherit file="layout.mak" />
