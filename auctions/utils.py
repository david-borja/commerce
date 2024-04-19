from .models import Bid

def process_bid(bid, listing, request):
    bid = float(bid)
    highest_bid = (
        listing.highest_bid.price if listing.highest_bid else listing.starting_bid
    )
    is_new_highest = bid > highest_bid
    if is_new_highest:
        bid = Bid.objects.create(
            listing=listing,
            user=request.user,
            price=bid,
        )
        listing.highest_bid = bid
        listing.save()
