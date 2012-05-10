from pyramid.security import Authenticated
from pyramid.security import Everyone

class FamosoAuthenticationPolicy(object):
    def effective_principals(self, request):
        effective_principals = [Everyone]
        if request.user:
            effective_principals.append(Authenticated)
            # add admin principal if true
            if request.user.admin:
                effective_principals.append('admin')
            # add the user as principal
            effective_principals.append('user:%s' % request.user.username)
            # iterate users report groups and add principals for them
            for group in request.user.report_groups:
                effective_principals.append('reportgroup:%s' % group.name)
        return effective_principals

