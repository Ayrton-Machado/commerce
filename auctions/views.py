
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  # Substitui IsAuthenticated

# Banco de dados
from django.db import IntegrityError
from .models import *
from .serializers import *  # Novo: substitui forms

class indexAPI(APIView):
    def get(self, request):
        auctions = AuctionListing.objects.all()
        return Response({'auctions': list(auctions.values())})

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Attempt to sign user in
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return Response({
                    "message": "Login Successful.",
                    "user": {
                        "username": user.username
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Invalid username and/or password."
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPI(APIView):      
    def post(self, request):
        confirmation = request.data.get("confirmation")

        if request.data.get("password") != confirmation:
            return Response({
                "error": "Passwords must match."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                login(request, user)

                return Response({
                    "message": "Register Successful.",
                    "user": {
                        "username": user.username
                    }
                }, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({
                    "message": "Username already taken."
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPI(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({
                "message": "Log Out Successful"
            }, status=status.HTTP_200_OK)

class CreateListingAPI(APIView):

    def post(self, request):
        #serializer
        serializer = CreateListingSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            try:
                serializer.save()
                return Response({
                    "message": "Create Listing Successful.",
                    "listing": serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": "Error saving to the database."})
        print(serializer.errors)
        return Response({
            "message": "Invalid data. Please correct the errors and try again.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ListingPageAPI(APIView):

    def get(self, request, listing_id):
        try:
            listingItem = AuctionListing.objects.get(id=listing_id)
        except AuctionListing.DoesNotExist:
            return Response({"error": "Listing not found"}, status=status.HTTP_404_NOT_FOUND)

        allComments = Comments.objects.filter(item=listingItem)
        bidsItem = Bids.objects.filter(bidItem=listingItem)
        lastBid = bidsItem.last()
        isOwner = request.user == listingItem.createdBy

        # Apenas define "win" se o leilão estiver fechado e houver um último lance
        win = False
        if listingItem.closed and lastBid is not None:
            win = request.user == lastBid.bidUser


        #data
        allCommentsData = CommentsSerializer(allComments, many=True).data
        bidsItemData = BidSerializer(bidsItem, many=True).data
        listingItemData = AuctionSerializer(listingItem).data
        bidAmount = bidsItem.count()


        return Response({
            'listing': listingItemData,
            'bidList': bidsItemData,
            'bidAmount': bidAmount,
            'win': win,
            'isOwner': isOwner,
            'comments': allCommentsData
        }, status=status.HTTP_200_OK)

class WatchlistAddAuctionAPI(APIView):
    def post(self, request, listing_id):
        user = request.user
        print("aaaaaaaaaaaaaaaa")
        print((listing_id, user))
        item = AuctionListing.objects.get(id=listing_id)
        watchlist = Watchlist(user=user, item=item)
        watchlist.save()

        return Response({
            'message': 'Successfully added to watchlist'
        }, status=status.HTTP_200_OK)


class WatchlistAuctionAPI(APIView):

    def get(self, request):
        user = request.user.id
        userWatchlist = Watchlist.objects.filter(user=user)
        userWatchlistData = WatchlistSerializer(userWatchlist, many=True).data

        return Response({
            'watchlist': userWatchlistData
        }, status=status.HTTP_200_OK)

class WatchlistRemoveAPI(APIView):

    def post(self, request):
        listing_id = request.POST.get('removeWatchlist')
        item = Watchlist.objects.get(id=listing_id)
        item.delete()
        return Response({"message": "Auction successfully removed from watchlist."}, status=status.HTTP_200_OK)

class PlaceBidAPI(APIView):

    def post(self, request, listing_id):
        listingItem = AuctionListing.objects.get(id=listing_id)
        bidstart = listingItem.bidstart
        bid = int(request.POST.get('placebid'))
        bidUser = request.user
        if bid > bidstart:
            listingItem.bidstart = bid
            Bids(bidUser=bidUser, bid=bid, bidItem=listingItem).save()
            listingItem.save()
            return Response({"message": "Bid placed successfully."}, status=status.HTTP_200_OK)
        else:
            Response({
                "error": "Bid must be higher than current bid.",
                "current_bid": bidstart
            }, status=status.HTTP_400_BAD_REQUEST)

class CloseAuctionAPI(APIView):

    def post(self, request, listing_id):
        listingItem = AuctionListing.objects.get(id=listing_id)
        lastBid = Bids.objects.filter(bidItem=listingItem).last()
        listingItem.closed = True
        listingItem.save()
        close = listingItem.closed
        if close == True:
            if close == True and request.user == lastBid.bidUser:
                winner = True
            elif close == True and request.user != lastBid.bidUser:
                winner = False
            return Response({
                "winner": winner
            })
        else:
            return Response({"message": "Auction closed successfully."}, status=status.HTTP_200_OK)
    
class AddCommentAPI(APIView):

    def post(self, request, listing_id):
        item = get_object_or_404(AuctionListing, id=listing_id)

        serializer = AddCommentSerializer(
            data=request.data,
            context={'request': request, "item": item}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Comment send successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowCategoriesAPI(APIView):   
    def get(self, request):
        categories = Category.objects.all()
        return Response({
            "categories" : categories
        }, status=status.HTTP_200_OK)

class CategoriesAuctionsAPI(APIView):
    def get(self, request, selectedCategory):
        category = Category.objects.get(categories = selectedCategory)
        categoriesAuctions = AuctionListing.objects.filter(category=category)
        allAuctions = AuctionListing.objects.all()
        return Response({
            'categoriesAuctions': categoriesAuctions,
            'auctions': allAuctions,
            'selectedCategory': selectedCategory
        }, status=status.HTTP_200_OK)
