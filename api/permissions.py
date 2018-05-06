from rest_framework.permissions import BasePermission

class IsAuthorOrStaff(BasePermission):
	message = "haahaaa you can't do this!"
	def has_object_permission(self, request, view, obj):
		if request.user.is_staff or (obj.author == request.user):
			return True
		else:
			return False
