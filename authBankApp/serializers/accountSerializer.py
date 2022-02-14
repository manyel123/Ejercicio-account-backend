from dataclasses import fields
from statistics import mode
from authBankApp.models.account import Account
from rest_framework             import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['balance', 'lastChangeDate', 'isActive']