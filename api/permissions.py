from rest_framework.permissions import BasePermission

class IsAuthorOrStaff(BasePermission):
	message = "You are not permitted to perform this!"
	def has_object_permission(self, request, view, obj):
		if request.user.is_staff or (obj.author == request.user):
			return True
		else:
			return False
