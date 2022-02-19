from django.conf                                    import settings
from rest_framework                                 import generics, status
from rest_framework.response                        import Response
from rest_framework.permissions                     import IsAuthenticated
from rest_framework_simplejwt.backends              import TokenBackend

from authBankApp.models.account                     import Account
from authBankApp.serializers.comboBoxSerializer     import ComboBoxSerializer

class ListAccounts(generics.ListAPIView):#Esta_clase_llena_el_combobox
    serializer_class   = ComboBoxSerializer 
    permission_classes = (IsAuthenticated,)    

    def get_queryset(self):
        print("Request:", self.request)
        print("Args:", self.args)
        print("KWArgs:", self.kwargs)

        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        queryset = Account.objects.exclude(user_id = self.kwargs['user'])
        return queryset