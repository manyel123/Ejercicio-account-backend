from django.conf                                    import settings
from rest_framework                                 import generics, status
from rest_framework.response                        import Response
from rest_framework.permissions                     import IsAuthenticated
from rest_framework_simplejwt.backends              import TokenBackend

from authBankApp.models.account                     import Account
from authBankApp.models.transaction                 import Transaction
from authBankApp.serializers.transactionSerializer  import TransactionSerializer

class TransactionsAccountView(generics.ListAPIView):
    serializer_class   = TransactionSerializer 
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

        queryset = Transaction.objects.filter(account_origin_id=self.kwargs['account'])
        return queryset


class TransactionsDetailView(generics.RetrieveAPIView):
    serializer_class   = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    queryset           = Transaction.objects.all()

    def get(self, request, *args, **kwargs):
        print("Request:", request)
        print("Args:", args)
        print("KWArgs:", kwargs)

        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)


class TransactionCreateView(generics.CreateAPIView):
    serializer_class   = TransactionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        print("Request:", request)
        print("Args:", args)
        print("KWArgs:", kwargs)

        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != request.data['user_id']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        account_origin = Account.objects.get(id=request.data['transaction_data']['account_origin'])
        if account_origin.balance < request.data['transaction_data']['amount']:
            stringResponse = {'detail':'saldo insuficiente'}
            return Response(stringResponse, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = TransactionSerializer(data=request.data['transaction_data'])
        serializer.is_valid(raise_exception=True)
        serializer.save()

        account_origin.balance -= request.data['transaction_data']['amount']
        account_origin.save()

        account_destiny = Account.objects.get(id=request.data['transaction_data']['account_destiny'])
        account_destiny.balance += request.data['transaction_data']['amount']
        account_destiny.save()

        return Response("Transacción exitosa", status=status.HTTP_201_CREATED)


class TransactionUpdateView(generics.UpdateAPIView):
    serializer_class   = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    queryset           = Transaction.objects.all()

    def get(self, request, *args, **kwargs):
        print("Request:", request)
        print("Args:", args)
        print("KWArgs:", kwargs)

        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        return super().update(request, *args,  **kwargs)


class TransactionsDeleteView(generics.DestroyAPIView):
    serializer_class   = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    queryset           = Transaction.objects.all()

    def get(self, request, *args, **kwargs):
        print("Request:", request)
        print("Args:", args)
        print("KWArgs:", kwargs)

        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        return super().destroy(request, *args,  **kwargs)