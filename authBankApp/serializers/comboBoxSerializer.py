from rest_framework                         import serializers
from authBankApp.models.account             import Account
from authBankApp.models.user                import User

class ComboBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'balance', 'lastChangeDate', 'isActive', 'user',]

    def to_representation(self, obj):
        user    = User.objects.get(id=obj.user_id)
        account = Account.objects.get(id=obj.id)
        return {
            'id'             : account.id,
            'balance'        : account.balance,
            'lastChangeDate' : account.lastChangeDate,
            'isActive'       : account.isActive,
            'user' : {
                'id'    : user.id,
                'name'  : user.name,
                'email' : user.email,
            },
        }