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
    else:
        return "Bid is not higher than current highest bid."
    
def toggle_bookmark(is_saved_by_user, listing, user):
    if is_saved_by_user:
        listing.saved_by.remove(user)
        return False
    else:
        listing.saved_by.add(user)
        return True
    
def close_listing(listing):
    if listing.is_active:
        listing.is_active = False
        listing.save()
        return False