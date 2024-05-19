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
        if listing.highest_bid:
            listing.winner = listing.highest_bid.user
        listing.save()
        return False
    
def get_current_highest(listing):
    return listing.highest_bid.price if listing.highest_bid else listing.starting_bid

def get_footer(listing, feed=""):
    if feed == "published":
        if listing.is_active and listing.highest_bid:
            string =  f"Highest bid by {listing.highest_bid.user.username}"
            pic = listing.highest_bid.user.profile_pic
            alt = "Profile picture of the highest bidder"
            return { "string": string, "pic": pic, "alt": alt }
        if listing.is_active and not listing.highest_bid:
            return { "string": "No bids yet", "pic": None, "alt": None }
        if not listing.is_active and listing.highest_bid:
            string = f"Won by {listing.winner.username}"
            pic = listing.winner.profile_pic
            alt = "Profile picture of the winner"
            return { "string": string, "pic": pic, "alt": alt }
        if not listing.is_active and not listing.highest_bid:
            return { "string": "Closed with no bids", "pic": None, "alt": None }
    else:
        string = f"Posted by {listing.author.username}"
        pic = listing.author.profile_pic
        alt = "Profile picture of the author"
        return { "string": string, "pic": pic, "alt": alt }
